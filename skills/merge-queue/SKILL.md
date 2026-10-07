---
name: merge-queue
description: >-
  Walk a merge queue one-by-one: free related worktrees, sync each PR in a
  dedicated merge-queue worktree, resolve conflicts, preview UI when testable,
  gate on human confirmation (except docs-only decision PRs which auto-merge),
  then after merges run a closing pnpm build and fix until green. Use when the
  user wants a merge queue, recommended merge order walked sequentially,
  one-by-one PR merges into a base branch, or a gated merge with local preview
  and a final integration build.
---

# Merge queue

Process PRs **one-by-one** against a base (default `dev`). Never prepare PR N+1 while PR N is still at a **human gate**. All PR work and the closing build run in **one** worktree: `../worktrees/merge-queue` (see [git.md](git.md)).

## Setup

1. Confirm **base** (`dev` unless the user names another) and the ordered queue.
2. `git fetch origin`.
3. Show the queue once: `# · issue · title · current base · risk notes`.
4. **Bulk-free** orchestrator worktrees whose branches are in this queue (keep branches). Create or reset `../worktrees/merge-queue` from `origin/<base>`.

**Done when:** base + queue are explicit, queue-related worktrees are freed, and the merge-queue worktree exists on `origin/<base>`.

## Process current PR

Do every item for the head of the remaining queue inside the merge-queue worktree. Then either **auto-merge** (docs-only) or stop at the **human gate**.

### 1. Sync the branch

Follow [git.md](git.md): check out the PR head in the merge-queue worktree, retarget if its stack parent already landed on base, merge `origin/<base>`, resolve conflicts via `resolving-merge-conflicts`, push.

**Done when:** `gh pr view <N> --json baseRefName,mergeable` shows base = agreed base and `MERGEABLE` (or conflicts fully resolved and pushed).

### 2. Preview or summarize

Classify with [preview.md](preview.md).

- **Visually testable** → start the matching package `pnpm` dev from the merge-queue worktree, fix boot/compile errors until healthy, then report the **URL**.
- **Not visually testable** → short diff summary only.

**Done when:** a working preview URL is posted, or a non-UI summary is written. Never post a URL for an unhealthy server.

### 3. Docs-only auto-merge (`no-ask`) — or human gate

After classify + summary:

**Auto-merge (no gate)** when **all** of:

1. [preview.md](preview.md) says **not visually testable**, and
2. Diff vs base is **only decision artifacts** — typically `.scratch/**/map.md`, `.scratch/**/resolution.md`, orchestration notes like `BLOCKING.md` / similar scratch decision docs — **no** product app code (`apps/**`, `packages/**` product sources, shared UI, etc.).

Then: `gh pr merge <N>` per [git.md](git.md); log one line `Auto-merged PR #<N> (docs-only)`; increment `merges_this_session`; advance → **Process current PR**, or **Closing build** if the queue is empty. Do **not** present `Reply: merge | skip | stop`.

**Human gate** when visually testable **or** the diff includes product/code (or anything outside decision-doc paths):

```
### Gate — PR #<N> (JES-XX)
Status: ready | blocked (<reason>)
Preview: <url or "n/a — <why>">
Reply: `merge` | `skip` | `stop`
```

**Done when (gate path):** this block is the last substantive content of the turn and no further queue work has started.

**Done when (auto-merge path):** the one-liner is logged and the next PR (or Closing build) has started in the same turn.

## After the reply

| Reply | Action |
|---|---|
| `merge` | `gh pr merge <N>` per [git.md](git.md). Kill this PR's preview. Advance → **Process current PR**, or **Closing build** if the queue is empty. |
| `skip` | Leave PR open. Kill preview. Advance → **Process current PR**, or **Closing build** if the queue is empty. |
| `stop` | Kill previews. Enter **Closing build** if this session merged ≥1 PR; otherwise halt and report remaining queue. |
| anything else | Clarify token. Stay at the gate. |

Track `merges_this_session` (successful merges: human `merge` **or** docs-only auto-merge).

## Closing build

Enter when the queue is empty **or** the user said `stop`, and `merges_this_session ≥ 1`. Otherwise halt.

Follow [build.md](build.md): on `origin/<base>` in the merge-queue worktree, run root `pnpm build`; if it fails, open a repair PR and fix until green (bounded); gate once green (or `blocked`).

**Done when:** build is green and the repair PR is merged (or skipped because build was already green with no repair), or a `blocked`/`stop` gate ended the phase. Then dispose the worktree per [git.md](git.md).

## Hard rules

- **One active preview** at a time.
- Conflict/boot/build fixes on PR heads or the repair branch are new commits (HEREDOC, hooks on); never amend/force-push unless the user asks.
- Prefer package-level `pnpm --filter <app> dev` over root `turbo dev` when only one app changed.
- Docs-only decision PRs never wait on a human gate (rule 2026-08-05).
