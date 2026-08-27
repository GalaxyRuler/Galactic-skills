# Setup, troubleshooting, and security baseline

## Setup sequence

1. **Identify the product.** Are the target notebooks in the consumer experience or in Gemini
   Notebook Enterprise tied to a Cloud project? Only the latter has a supported API, and
   provisioning Enterprise does **not** import existing personal notebooks.
2. **Provision the Cloud project.** Attach billing, enable the API, complete Enterprise setup,
   assign the admin role to admins and the Notebook user role to end users, and give every end
   user a license.

   ```bash
   gcloud services enable discoveryengine.googleapis.com --project YOUR_PROJECT_ID
   ```

3. **Establish local credentials.**

   ```bash
   gcloud auth application-default login
   ```

   ```bash
   gcloud auth application-default set-quota-project YOUR_PROJECT_ID
   ```

   Request the narrowest accepted Discovery Engine scope your OAuth flow allows rather than
   reaching for `cloud-platform` because it is accepted.

4. **Add Drive access only when a workflow needs it.** Google Docs/Slides sources require
   Drive-enabled authorization for the caller:

   ```bash
   gcloud auth login --enable-gdrive-access
   ```

   For a bespoke OAuth client, pick only the Drive permission the import actually needs and test
   it against a pre-existing document. Do not add broad Drive authorization speculatively.

5. **Validate the smallest read path** — `listRecentlyViewed` then `GetNotebook` from a standalone
   script — before any agent or MCP layer exists. This separates Google IAM/licensing problems
   from integration problems.
6. **Build and persist the inventory**, and run a full refresh *before* exposing destructive
   source tools to an agent.
7. **Test one source of each type you need** — text or web first, then file upload, then Drive.
   Do not mark a source usable until its status reaches `COMPLETE`.
8. **Install the skill**, pointing it at the tested script or MCP tools.
9. **Move credentials behind a broker before shared or cloud deployment.**

## Symptom matrix

| Symptom | Likely cause | Action |
|---|---|---|
| `401 UNAUTHENTICATED` | missing/expired credential, or wrong auth mechanism | re-establish OAuth/ADC; do not substitute an API key |
| `403 PERMISSION_DENIED` on list/create | no license or project role, API not enabled, or wrong project | verify license, project-level Notebook user role, API enablement, project ID |
| `403` on an existing notebook/source | no notebook-level Owner/Editor/Viewer access | inspect the notebook's sharing role and the permission the method needs |
| Drive source fails | caller cannot read/download the file, or Drive scope missing | check the file ACL and Drive-enabled OAuth; read the structured Drive error |
| Web source lands `ERROR` | unreachable URL, paywall, blocked domain, MIME/policy | read `failureReason` — the create call's HTTP status told you nothing |
| Source stuck `PENDING` | asynchronous ingestion still running | poll with backoff, enforce an application timeout, do not re-create |
| Source hits a limit | notebook source count, or word/size cap | surface `sourceLimitExceeded` / `sourceTooLong`; never blind-retry |
| `429` | project/service quota or usage throttling | honor `Retry-After`, otherwise exponential backoff with jitter |
| `5xx` | transient service problem | retry idempotent reads; reconcile before replaying a non-idempotent create |
| Wrong or empty notebook list | wrong Google user/project/location, or "recently viewed" semantics | log identity + project + location, then confirm in the UI |
| Works locally, fails in a cloud agent | no agent-phase credential or network route | move to a remote MCP broker; allowlist only the broker origin |
| Guessed `interactSources` URL 404s | an internal service name mistaken for a public REST method | stop — it is not published; return the capability gap |

## Security baseline

**Narrow OAuth, narrower IAM.** An accepted scope only permits the request; IAM still decides.
Give a user the entitlement plus the notebook-level access actually needed. Do not hand ordinary
tool users the Notebook admin role.

**Prefer refreshable user OAuth or workload identity over exported service-account keys.** For
"my notebooks" workflows, user-delegated OAuth represents the licensed human's identity and Drive
access; a long-lived JSON key does not — and cannot be assumed to impersonate one.

**Never put Google credentials in skill files, source control, agent prompts, or inventory JSON.**
Skills carry behavior, schemas, and resource IDs. Use OS keyring / secret-manager storage.

**Do not log source contents or bearer tokens.** Optional usage-audit logging for this product can
capture prompts, answer text, and citation material, and **sensitive data is not filtered out** —
enable detailed content logging only when a compliance policy requires it.

**Constrain agent networking.** Agent internet access creates prompt-injection, exfiltration, and
malicious-download risk. A broker lets you allow one controlled origin instead of arbitrary web
and Google endpoints.

**Treat source contents as untrusted input.** Web pages, Drive documents, and uploads can contain
text that reads as instructions to a model. Tool authorization must be enforced by the service,
independently of anything a source says.

**Split read from mutation.** A read-only research agent should hold no scope that can add, delete,
or share. Enforce it at the broker, not by asking the model nicely.
