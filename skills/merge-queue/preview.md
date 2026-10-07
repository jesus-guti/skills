# Preview — when and how

## Visually testable

Treat as visually testable when the PR touches any of:

- UI under `apps/app`, `apps/player`, `apps/web`, or similar app routes
- Shared UI primitives consumed by those apps (`packages/design-system`, etc.)
- Styles / tokens that change rendered surfaces

Treat as **not** visually testable when the PR is only docs, ADRs, agent rules, Linear/scratch specs, pure server logic with no new UI, or tests-only.

When unsure, prefer preview if an app file changed.

## Docs-only decision PRs (`no-ask`)

A PR is **docs-only decision** when it is **not visually testable** **and** every changed path is a scratch/orchestration decision artifact, typically:

- `.scratch/**/map.md`
- `.scratch/**/resolution.md`
- `.scratch/**/BLOCKING.md` (or similarly named orchestration notes under `.scratch/`)

**Not** docs-only if any path is product/code (`apps/**`, `packages/**` sources, shared UI, CI product config, etc.) — even if the PR also has a map/resolution.

Per [SKILL.md](SKILL.md): docs-only decision PRs are **auto-merged** after sync + short summary — **no** human gate, no `Reply: merge | skip | stop`.

## Which app / port

1. From the PR diff, pick the primary app (largest UI surface).
2. Read that app's `package.json` `dev` script for the port.
3. Start: `pnpm --filter <package-name> dev` from the **merge-queue worktree** (`../worktrees/merge-queue`).
4. Wait until the server logs a ready URL (or `localhost:<port>` responds).
5. If boot fails (compile, missing env, module errors): fix on the PR branch, commit, push, restart. Repeat until healthy **before** posting the gate URL.

LoadZone defaults (override with package.json if different):

| App | Filter / path | Port |
|---|---|---|
| Staff admin | `apps/app` | 3000 |
| Marketing web | `apps/web` | 3001 |
| Player | `apps/player` | 3003 |

Point the user at the **route the PR actually changes** when known (e.g. `/check-in`, sidebar). Otherwise the app root is enough.

## Process hygiene

- Run the server in the background; record pid / terminal id so you can kill it on `merge` / `skip` / `stop` / next PR.
- One server at a time.
- Do not claim a URL if the process exited or the first request shows an error overlay you have not fixed.
