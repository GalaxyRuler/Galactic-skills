#!/usr/bin/env python3
"""Minimal REST client for the Gemini Notebook Enterprise (Discovery Engine) API.

Deliberately hits the REST surface directly rather than a generated SDK: the v1alpha
Notebook API is a preview surface, and this keeps the supported/unsupported boundary
visible in the code instead of hidden behind whatever a client library version wraps.

    python -m pip install google-auth requests

    gcloud auth application-default login
    python notebook_client.py inventory --project-number 123456789012

    python notebook_client.py --selftest     # offline checks, no credentials needed
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from dataclasses import dataclass
from typing import Any, Iterator, Sequence

DISCOVERY_SCOPE = "https://www.googleapis.com/auth/discoveryengine.readwrite"

RETRYABLE_HTTP = {429, 500, 502, 503, 504}


class NotebookAPIError(RuntimeError):
    """Google Notebook API request failed."""


class PublicQueryEndpointUnavailable(NotImplementedError):
    """No supported public Notebook Q&A REST method is currently published."""


@dataclass(frozen=True)
class NotebookConfig:
    project_number: str
    location: str = "global"
    endpoint_location: str = "global"

    @property
    def parent(self) -> str:
        return f"projects/{self.project_number}/locations/{self.location}"

    @property
    def base_url(self) -> str:
        # Enterprise guides use location-aware Discovery Engine endpoints.
        return f"https://{self.endpoint_location}-discoveryengine.googleapis.com/v1alpha"


class NotebookEnterpriseClient:
    def __init__(self, config: NotebookConfig, session: Any | None = None) -> None:
        self.config = config

        if session is not None:  # injected for tests
            self.http = session
            return

        import google.auth  # imported lazily so --selftest runs without the dependency
        from google.auth.transport.requests import AuthorizedSession

        credentials, _ = google.auth.default(scopes=[DISCOVERY_SCOPE])
        self.http = AuthorizedSession(credentials)

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json_body: dict[str, Any] | None = None,
        idempotent: bool = False,
        timeout: float = 60.0,
        max_attempts: int = 5,
    ) -> dict[str, Any]:
        url = f"{self.config.base_url}/{path.lstrip('/')}"

        for attempt in range(max_attempts):
            response = self.http.request(
                method, url, params=params, json=json_body, timeout=timeout
            )

            if 200 <= response.status_code < 300:
                return response.json() if response.content else {}

            can_retry = (
                idempotent
                and response.status_code in RETRYABLE_HTTP
                and attempt + 1 < max_attempts
            )

            if can_retry:
                retry_after = response.headers.get("Retry-After")
                if retry_after and retry_after.isdigit():
                    delay = float(retry_after)
                else:
                    # Truncated exponential backoff + jitter.
                    delay = min(32.0, (2**attempt) + random.random())
                time.sleep(delay)
                continue

            try:
                error = response.json()
            except ValueError:
                error = {"status": response.status_code, "reason": response.reason}

            raise NotebookAPIError(
                f"{method} {path} failed with HTTP {response.status_code}: {error}"
            )

        raise NotebookAPIError("Retry loop exhausted unexpectedly.")

    def iter_notebooks(self, *, page_size: int = 500) -> Iterator[dict[str, Any]]:
        """Iterate every page returned by listRecentlyViewed.

        This is the calling user's recently-viewed feed, NOT an org-wide listing.
        """
        if not 1 <= page_size <= 500:
            raise ValueError("page_size must be between 1 and 500.")

        token: str | None = None

        while True:
            params: dict[str, Any] = {"pageSize": page_size}
            if token:
                params["pageToken"] = token

            result = self._request(
                "GET",
                f"{self.config.parent}/notebooks:listRecentlyViewed",
                params=params,
                idempotent=True,
            )

            yield from result.get("notebooks", [])

            token = result.get("nextPageToken")
            if not token:
                break

    def get_notebook(self, notebook_id: str) -> dict[str, Any]:
        return self._request(
            "GET", f"{self.config.parent}/notebooks/{notebook_id}", idempotent=True
        )

    def list_sources(self, notebook_id: str) -> list[dict[str, Any]]:
        """No public sources.list method exists; GetNotebook carries sources[]."""
        return list(self.get_notebook(notebook_id).get("sources", []))

    def get_source(self, notebook_id: str, source_id: str) -> dict[str, Any]:
        return self._request(
            "GET",
            f"{self.config.parent}/notebooks/{notebook_id}/sources/{source_id}",
            idempotent=True,
        )

    def add_sources(
        self, notebook_id: str, user_contents: Sequence[dict[str, Any]]
    ) -> dict[str, Any]:
        """Create sources.

        NOT auto-retried: no public idempotency key is assumed here, so a replayed
        create can duplicate sources. Reconcile inventory before replaying by hand.
        """
        if not user_contents:
            raise ValueError("At least one source is required.")

        return self._request(
            "POST",
            f"{self.config.parent}/notebooks/{notebook_id}/sources:batchCreate",
            json_body={"userContents": list(user_contents)},
            idempotent=False,
        )

    def add_text_source(self, notebook_id: str, *, title: str, text: str) -> dict[str, Any]:
        return self.add_sources(
            notebook_id, [{"textContent": {"sourceName": title, "content": text}}]
        )

    def add_web_source(self, notebook_id: str, *, title: str, url: str) -> dict[str, Any]:
        return self.add_sources(
            notebook_id, [{"webContent": {"sourceName": title, "url": url}}]
        )

    def remove_sources(
        self, notebook_id: str, source_ids: Sequence[str]
    ) -> dict[str, Any]:
        if not source_ids:
            raise ValueError("At least one source ID is required.")

        parent = f"{self.config.parent}/notebooks/{notebook_id}"
        names = [f"{parent}/sources/{source_id}" for source_id in source_ids]

        # Batch delete is safe to reconcile/replay; success response is {}.
        return self._request(
            "POST",
            f"{parent}/sources:batchDelete",
            json_body={"names": names},
            idempotent=True,
        )

    def capabilities(self) -> dict[str, Any]:
        return {
            "provider": "google-gemini-notebook-enterprise",
            "capabilities": {
                "notebooks.list": True,
                "notebooks.get": True,
                "sources.list": True,
                "sources.add": True,
                "sources.delete": True,
                "notebooks.query": False,
            },
            "queryStatus": {
                "reason": "unsupported_public_api",
                "note": (
                    "Internal query service paths appear in audit-logging docs, but no "
                    "public Notebook REST/RPC query method is published."
                ),
            },
        }

    def query_notebook(
        self,
        notebook_id: str,
        question: str,
        *,
        source_ids: Sequence[str] | None = None,
    ) -> dict[str, Any]:
        """Intentionally unimplemented — do not guess an undocumented endpoint.

        Kept so a future supported Google query API, or an explicitly approved and
        clearly labeled adapter, can implement the same interface later.
        """
        raise PublicQueryEndpointUnavailable(
            "No public v1alpha Notebook Q&A method is published. Report the capability "
            "gap; do not substitute another retrieval engine and call it NotebookLM."
        )


def build_inventory(client: NotebookEnterpriseClient) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []

    for summary in client.iter_notebooks():
        full = client.get_notebook(summary["notebookId"])
        inventory.append(
            {
                "name": full["name"],
                "id": summary["notebookId"],
                "title": full.get("title"),
                "emoji": full.get("emoji"),
                "metadata": full.get("metadata", {}),
                "sources": [
                    {
                        "name": s["name"],
                        "id": s.get("sourceId", {}).get("id"),
                        "title": s.get("title"),
                        "metadata": s.get("metadata", {}),
                        "settings": s.get("settings", {}),
                    }
                    for s in full.get("sources", [])
                ],
            }
        )

    return inventory


def _selftest() -> None:
    """Offline checks: URL/name construction, pagination, retry policy, query gate."""

    class FakeResponse:
        def __init__(self, status_code: int, payload: dict[str, Any]) -> None:
            self.status_code = status_code
            self._payload = payload
            self.content = b"{}"
            self.headers: dict[str, str] = {}
            self.reason = "fake"

        def json(self) -> dict[str, Any]:
            return self._payload

    class FakeSession:
        def __init__(self, responses: list[FakeResponse]) -> None:
            self.responses = responses
            self.calls: list[tuple[str, str, dict[str, Any] | None, dict[str, Any] | None]] = []

        def request(self, method, url, params=None, json=None, timeout=None):
            self.calls.append((method, url, params, json))
            return self.responses.pop(0)

    cfg = NotebookConfig(project_number="123456789012")
    assert cfg.parent == "projects/123456789012/locations/global"
    assert cfg.base_url.startswith("https://global-discoveryengine.googleapis.com/v1alpha")

    # Pagination follows nextPageToken and stops when it is absent.
    session = FakeSession(
        [
            FakeResponse(200, {"notebooks": [{"notebookId": "nb_1"}], "nextPageToken": "t2"}),
            FakeResponse(200, {"notebooks": [{"notebookId": "nb_2"}]}),
        ]
    )
    client = NotebookEnterpriseClient(cfg, session=session)
    ids = [n["notebookId"] for n in client.iter_notebooks(page_size=1)]
    assert ids == ["nb_1", "nb_2"], ids
    assert session.calls[1][2]["pageToken"] == "t2"

    try:
        next(client.iter_notebooks(page_size=501))
    except ValueError:
        pass
    else:  # pragma: no cover
        raise AssertionError("page_size 501 must be rejected")

    # batchDelete builds full resource names, not bare IDs.
    session = FakeSession([FakeResponse(200, {})])
    client = NotebookEnterpriseClient(cfg, session=session)
    client.remove_sources("nb_1", ["src_1"])
    assert session.calls[0][3] == {
        "names": ["projects/123456789012/locations/global/notebooks/nb_1/sources/src_1"]
    }

    # Non-idempotent create is NOT retried on 500 — it raises so the caller reconciles.
    session = FakeSession([FakeResponse(500, {"error": "boom"})])
    client = NotebookEnterpriseClient(cfg, session=session)
    try:
        client.add_text_source("nb_1", title="t", text="x")
    except NotebookAPIError:
        pass
    else:  # pragma: no cover
        raise AssertionError("failed create must not be silently retried/swallowed")
    assert len(session.calls) == 1

    # Query stays gated.
    assert client.capabilities()["capabilities"]["notebooks.query"] is False
    try:
        client.query_notebook("nb_1", "anything?")
    except PublicQueryEndpointUnavailable:
        pass
    else:  # pragma: no cover
        raise AssertionError("query_notebook must not pretend to work")

    print("selftest ok")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("command", nargs="?", choices=["inventory", "capabilities"])
    parser.add_argument("--project-number")
    parser.add_argument("--location", default="global")
    parser.add_argument("--endpoint-location", default="global")
    parser.add_argument("--selftest", action="store_true", help="run offline checks and exit")
    args = parser.parse_args(argv)

    if args.selftest:
        _selftest()
        return 0

    if not args.command or not args.project_number:
        parser.error("command and --project-number are required (or pass --selftest)")

    client = NotebookEnterpriseClient(
        NotebookConfig(
            project_number=args.project_number,
            location=args.location,
            endpoint_location=args.endpoint_location,
        )
    )

    payload = (
        client.capabilities()
        if args.command == "capabilities"
        else build_inventory(client)
    )
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
