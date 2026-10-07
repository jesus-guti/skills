# Closing build

## When

Run after the queue is empty or the user `stop`s, **if and only if** this session successfully merged ≥1 PR into base. If zero merges, skip.

## Where

Inside `../worktrees/merge-queue`:

```bash
git fetch origin
git checkout <base>
git reset --hard origin/<base>
pnpm install   # if deps may have changed
pnpm build     # root → turbo build
```

Do **not** require `pnpm check` or filtered builds for this gate.

## If green

No repair PR. Report success. Dispose worktree per [git.md](git.md). Queue run is complete.

## If red → repair PR

1. `git checkout -b fix/merge-queue-build` from current `origin/<base>` (or `fix/merge-queue-build-<short-date>` if the name exists).
2. Fix compile / type / import breakage caused by the merged queue. Commit (HEREDOC) and push.
3. `gh pr create --base <base> --title "fix: merge-queue integration build" --body "…"` with failing packages and root cause summary.
4. Re-run `pnpm build`.

### Bounds (hybrid)

- Auto-fix only **compile / TypeScript / import** failures clearly tied to the queue.
- **Max 5** build→fix→commit cycles on the repair branch.
- Escalate immediately (gate `blocked`, no more auto-fix) when:
  - missing env/secrets/infra,
  - product/design ambiguity,
  - the **same** error signature persists after 2 fix attempts,
  - or the 5-cycle cap is hit.

On escalate, post the gate with logs + diff summary and **keep** the worktree.

## Gate (end the turn) when green or blocked

```
### Gate — closing build
Status: ready (pnpm build green) | blocked (<reason>)
Repair PR: <url or "n/a — already green">
Reply: `merge` | `stop`
```

| Reply | Action |
|---|---|
| `merge` | If repair PR exists: `gh pr merge` it. Dispose worktree on success. |
| `stop` | Leave repair PR open if any. Keep worktree if dirty/blocked. Halt. |

Do **not** ask for confirmation on each failed build attempt — only when green or blocked.

## Completion

Closing build is done when: base builds green and any repair PR is merged, or the user `stop`s / accepts `blocked`.
