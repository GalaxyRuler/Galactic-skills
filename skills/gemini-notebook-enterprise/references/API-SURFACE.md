# API surface — Discovery Engine Notebook API

> **Snapshot, not gospel.** This file records the shape of the published `v1alpha` Notebook
> surface at the time the skill was written. It is a preview API. Re-check the live REST/RPC
> reference for any method you are about to call before quoting availability, scopes, or limits
> to a user. See the `research-grounding` skill.

Canonical docs (note the host — `cloud.google.com` 301-redirects to `docs.cloud.google.com`):

```text
docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks
docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks-sources
docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-audio-overview
docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/overview
docs.cloud.google.com/gemini/enterprise/docs/reference/rest/v1alpha/projects.locations.notebooks
```

Rows below marked **[verified]** were checked against those how-to pages. Rows marked
**[unverified]** come from the RPC/IAM reference pages, which render as JavaScript navigation
shells to most fetchers — confirm them in a browser before relying on them.

## Endpoint and resource names

Enterprise examples use a location-aware Discovery Engine endpoint keyed to the notebook
multi-region (`global`, `us`, `eu`):

```text
https://{endpoint_location}-discoveryengine.googleapis.com/v1alpha
```

```text
projects/{project}/locations/{location}/notebooks/{notebook_id}
projects/{project}/locations/{location}/notebooks/{notebook_id}/sources/{source_id}
```

## Method map

| Task | REST operation | Accepted OAuth scope | Key IAM permission |
|---|---|---|---|
| Create notebook **[verified]** | `POST .../notebooks` | `cloud-platform`; RPC ref also lists `discoveryengine.readwrite` / `serving.readwrite` **[unverified]** | `discoveryengine.notebooks.create` |
| Get notebook + its sources **[verified]** | `GET .../notebooks/{id}` | same | `discoveryengine.notebooks.get` |
| Enumerate notebooks **[verified]** | `GET .../notebooks:listRecentlyViewed` | same | `discoveryengine.notebooks.list` |
| Delete notebooks **[verified]** | `POST .../notebooks:batchDelete` | same | `discoveryengine.notebooks.delete` |
| Share notebook **[verified]** | `POST .../notebooks/{id}:share` | same | `notebooks.getIamPolicy` + `notebooks.setIamPolicy` **[unverified]** |
| Add sources **[verified]** | `POST .../notebooks/{id}/sources:batchCreate` | above, plus `discoveryengine.assist.readwrite` **[unverified]** | `discoveryengine.sources.create` |
| Upload a file **[verified]** | `POST` to the **`/upload/v1alpha/`** host path, `.../sources:uploadFile` | Google OAuth/IAM | `discoveryengine.sources.create` |
| Get source **[verified]** | `GET .../sources/{source}` | `cloud-platform` (+ the two above **[unverified]**) | `discoveryengine.sources.get` |
| Remove sources **[verified]** | `POST .../sources:batchDelete` | same | `discoveryengine.sources.delete` |
| Create audio overview **[verified]** | `POST .../notebooks/{id}/audioOverviews` | `cloud-platform` | — |
| Delete audio overview **[verified]** | `DELETE .../notebooks/{id}/audioOverviews/default` | `cloud-platform` | — |
| **Query selected sources** | **no published public method** | — | IAM catalog reportedly contains `discoveryengine.notebooks.interactSources` **[unverified]**, but no public transport is documented **[verified]** |

Scope strings:

```text
https://www.googleapis.com/auth/discoveryengine.readwrite
https://www.googleapis.com/auth/discoveryengine.serving.readwrite
https://www.googleapis.com/auth/cloud-platform
https://www.googleapis.com/auth/discoveryengine.assist.readwrite   # BatchCreateSources
```

**There is no public `sources.list`.** `GetNotebook` returns the notebook's output-only
`sources[]` array — that is the inventory route.

## Generation surface — real, and not the same thing as Q&A

The notebook API is **not** purely management. `notebooks.audioOverviews.create` generates an
audio overview from the notebook, and it accepts exactly the two things a query API would need:

```json
{
  "sourceIds": ["src_001", "src_007"],
  "episodeFocus": "topics or content to highlight",
  "languageCode": "en"
}
```

`sourceIds` is optional — omit it and every source in the notebook is used. Delete uses the fixed
resource id `default`, so a notebook holds one audio overview at a time.

So "selected sources + an instruction, processed by the notebook's own model" **is** exposed —
just as a generated artifact, not as an answer with citations you can parse. The product also
advertises video overviews, mind maps, reports, slide decks, and infographics, each with its own
daily quota. Only the audio-overview API how-to was confirmed; **check the docs section for newer
generation endpoints before telling a user something is not automatable.**

Practical consequence: when a user asks for "notebook Q&A", ask what they need the answer *for*.
If it is a briefing or a digest, a generated artifact over selected sources may already do the
job through a documented API. If they need structured answer text plus citations, that is the
gap below.

## The query asymmetry

Google's IAM catalog exposes `discoveryengine.notebooks.interactSources`, and Enterprise
usage-audit documentation describes internal service methods (`NotebookService.InteractSources`,
`NotebookService.GenerateFreeFormStreamed`) carrying selected sources, user queries, answers and
citations. Those are **audit-logging artifacts, not a published API contract**. The public
notebook resource does not list a Q&A method.

Engineering position: keep `query_notebook` in the abstract tool contract, have the official
provider raise/return `unsupported_public_api`, and plug in the real transport if and when Google
publishes one. If an organization must automate Q&A now, index the same governed source set into a
Google search/RAG service that *does* have a documented query API — and label the results as that
system, never as "the notebook answered."

## Documented usage limits

Product limits (not a complete per-RPC rate spec), from the Enterprise product overview:

| Limit | Value |
|---|---|
| Notebooks per user | 500 |
| Sources per notebook | 300 |
| Per source | 500 MB or 500,000 words |
| Queries per user per day | 500 |
| Audio overviews / video overviews / mind maps / reports per user per day | 20 each |
| Slide decks / infographics per user per day | 15 each |
| YouTube transcript | 500,000 words |

**Do not quote the consumer numbers.** Third-party articles list 50/100/300/600 sources by
consumer plan tier and a 200 MB upload cap; those are the consumer product, not Enterprise, and
mixing them produces confidently wrong capacity advice.

`ListRecentlyViewedNotebooks` has default and maximum `page_size` **500** and returns
`next_page_token`. Note the semantics: *recently viewed* is the calling user's inventory feed, not
an admin-wide "list everything" endpoint. Do not hard-code a Notebook RPM — implement `429`
backoff and watch the project's Cloud Quotas page.

## Representative JSON

Notebook (field structure real, identifiers illustrative):

```json
{
  "name": "projects/123456789012/locations/global/notebooks/nb_abc123",
  "title": "Market Research",
  "notebookId": "nb_abc123",
  "emoji": "📚",
  "metadata": {
    "isShared": false,
    "isShareable": true,
    "lastViewed": "2026-01-15T07:32:11Z",
    "createTime": "2025-12-14T10:00:00Z"
  },
  "sources": [
    {
      "name": "projects/123456789012/locations/global/notebooks/nb_abc123/sources/src_001",
      "title": "Market outlook",
      "sourceId": { "id": "src_001" },
      "metadata": {
        "wordCount": 28472,
        "tokenCount": 39110,
        "sourceAddedTimestamp": "2026-01-08T12:01:33Z"
      },
      "settings": { "status": "SOURCE_STATUS_COMPLETE" }
    }
  ]
}
```

Pagination: `pageToken` / `nextPageToken` (REST), `page_token` / `next_page_token` (RPC).

Batch-create sources:

```json
{
  "userContents": [
    { "textContent": { "sourceName": "Internal research notes", "content": "Research material..." } },
    { "webContent": { "sourceName": "Official statistics page", "url": "https://example.gov/statistics" } },
    { "googleDriveContent": {
        "documentId": "DRIVE_DOCUMENT_ID",
        "mimeType": "application/vnd.google-apps.document",
        "sourceName": "Quarterly plan" } },
    { "videoContent": { "youtubeUrl": "https://www.youtube.com/watch?v=VIDEO_ID" } }
  ]
}
```

Four content keys, exactly: `textContent`, `webContent`, `googleDriveContent`, `videoContent`.
Binary files do not go here — they use the separate `sources:uploadFile` endpoint on the
`/upload/v1alpha/` path with `X-Goog-Upload-File-Name` and `X-Goog-Upload-Protocol: raw` headers
(PDF, TXT, MD, DOCX, PPTX, XLSX, MP3/WAV/OGG, PNG/JPG).

Batch-delete sources — request takes full resource names; documented success response is `{}`:

```json
{
  "names": [
    "projects/123456789012/locations/global/notebooks/nb_abc123/sources/src_001",
    "projects/123456789012/locations/global/notebooks/nb_abc123/sources/src_002"
  ]
}
```

Your own provider-neutral query contract (yours, **not** a claimed Google schema):

```json
{
  "notebook": "projects/.../notebooks/nb_abc123",
  "sourceIds": ["src_001", "src_007"],
  "question": "What assumptions do these two sources make about 2030 demand?"
}
```

```json
{
  "status": "ok",
  "answer": "Normalized answer text...",
  "citations": [{ "sourceId": "src_001", "text": "Citation excerpt" }],
  "suggestedQuestions": []
}
```

## Source status and failure model

Status values: `PENDING`, `TENTATIVE`, `COMPLETE`, `ERROR`, `PENDING_DELETION` (plus unspecified).

Structured failure reasons are unusually rich — preserve them instead of collapsing to
"source failed". Documented families include: source too long, empty content, upload/ingestion
failure, paywall, unreachable URL, Drive download restriction, YouTube problem, audio
transcription failure, source-count limit exceeded, blocked domain or MIME type, policy-check
failure.

Automation implications:

- `sourceTooLong` / `sourceLimitExceeded` — surface to the user, never blind-retry.
- `googleDriveError` — check the file ACL *and* whether the caller's OAuth has Drive access.
- `PENDING` past your timeout — keep the row, mark it timed-out, do not re-create the source.

## Inventory metadata worth storing

Google gives you identity; you supply governance. Capture both layers:

| Layer | Fields |
|---|---|
| Tenancy | `project_id`, `project_number`, `location`, `endpoint_location`, environment |
| Identity context | Google subject/email, auth mode, license state, project role |
| Notebook | full `name`, `notebook_id`, `title`, `emoji`, `create_time`, `last_viewed`, `is_shared`, `is_shareable` |
| Notebook authz | effective owner/editor/viewer role, sharing principals |
| Source identity | full `name`, `source_id`, `title`, inferred type |
| Source provenance | Drive doc ID + revision, YouTube video/channel ID, URL or original filename |
| Source metrics | `word_count`, `token_count`, `source_added_timestamp` |
| Source health | `status`, `failure_reason` |
| Local governance | selection sets, tags, data classification, owner, retention rule |
| Local integrity | `imported_at`, `last_synced_at`, optional content hash for files you supplied |

The local governance and integrity rows are what turn "ask my notebook using only the approved
sources" into a deterministic resource-name list instead of a fuzzy title search.

## Refresh algorithm

1. `notebooks:listRecentlyViewed`, following `nextPageToken`.
2. `GetNotebook` per notebook for full metadata and `sources[]`.
3. Upsert notebook rows keyed on the full resource name.
4. Upsert source rows keyed on the source resource name.
5. Mark remote objects missing from a *known-complete* refresh as stale — do not delete local history.
6. Record `last_synced_at`.
7. Resolve human aliases to exact notebook IDs locally.
8. Maintain named source-selection sets (for example `authoritative`, `filings`) by source ID.
