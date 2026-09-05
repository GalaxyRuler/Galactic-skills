# Standards

## Frontend Standards

Minimize client-side JavaScript unless interactivity requires it.

For React and Next.js:

- Prefer Server Components where supported and appropriate.
- Use Client Components only for interactivity, browser APIs, hooks, or local UI state.
- Keep data fetching close to the server boundary where possible.
- Avoid sending large data or unnecessary logic to the client.

State management preference:

1. URL/search params for shareable UI state.
2. Server state, loader data, or query cache.
3. Local component state.
4. Small shared store only when needed.
5. Heavy global state only when already established or clearly justified.

For UI work, verify responsive behavior, loading state, empty state, error state, keyboard navigation, focus state, contrast, accessible labels, and visual hierarchy.

For performance, check unnecessary Client Components, redundant imports, large bundles, poor tree-shaking, repeated network calls, unpaginated lists, expensive rerenders, missing loading/error states, image optimization, and accessibility regressions. Tie optimization to observed risk or measurable cost.

## Backend Standards

Use Clean, Hexagonal, or Onion Architecture only when complexity justifies it. For smaller projects, keep boundaries simple but explicit.

Separate domain logic, application/use-case logic, infrastructure adapters, external services, database layer, and HTTP/API layer when the project size warrants it.

For REST APIs:

- Use correct HTTP methods and consistent route naming.
- Validate inputs.
- Return consistent error shapes and appropriate status codes.
- Avoid leaking implementation details.
- Version APIs when breaking changes are likely.
- Document public routes.

For API changes, include request schema, response schema, error cases, auth requirements, and useful example payloads.

## Security Standards

Check authentication, authorization, input validation, rate limiting, secret handling, dependency vulnerabilities, insecure logging, CSRF, XSS, SSRF, SQL injection, unsafe uploads, open redirects, permissive CORS, and webhook signature validation.

Never print secrets. Redact tokens, passwords, keys, private URLs, cookies, and other credentials.

Require explicit error boundaries where appropriate, structured errors, actionable logs, retry/backoff for transient external failures, timeouts for external calls, idempotency for retryable operations, and correlation/request IDs for multi-step flows when useful.

## Database and Migration Standards

Inspect the current schema and migration framework first. Never assume production data shape from schema alone.

Avoid destructive migrations without a backup and rollback strategy. Prefer backward-compatible migrations and Expand-Migrate-Contract:

1. Add nullable columns, tables, or indexes first.
2. Deploy code that writes both old and new fields if needed.
3. Backfill safely.
4. Switch reads.
5. Remove old structure later.
6. Verify with tests and data checks.

## CI/CD and Delivery Standards

Prefer trunk-based development and short-lived branches unless the repository uses another process.

Healthy CI should run lint, typecheck, unit tests, integration tests where appropriate, build, and security/dependency checks where feasible. Do not claim CI is healthy unless verified from config or recent runs.

For production deployment, prefer rolling, blue-green, or canary strategies where feasible. Require rollback path, health checks, downtime-safe migrations, service status verification, and post-deploy log checks.
