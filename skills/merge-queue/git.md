# Git — merge-queue worktree + stack

## Paths

- Queue + closing build: `../worktrees/merge-queue` (single worktree for the whole run).
- Orchestrator issue worktrees (to free): e.g. `../worktrees/rely/jes-NNN`.

Primary repo checkout stays untouched for day-to-day editing.

## Setup: bulk-free + create

```bash
git fetch origin
git worktree list
# For each path whose checked-out branch is in the queue:
git worktree remove <path> --force   # keeps the branch

git worktree add ../worktrees/merge-queue origin/<base>
# If it already exists: remove only when idle/clean-close rules allow, then recreate;
# or inside it: git fetch && git checkout -B <temp> origin/<base>
```

Report which worktrees were removed.

## Per-PR sync (inside merge-queue worktree)

```bash
git fetch origin
git checkout <pr-head-branch>
# If stack parent already merged into base:
gh pr edit <N> --base <base>
git merge origin/<base>
# resolve → commit → push
git push origin HEAD
```

Prefer **merge** of base into the PR head (not rebase) unless the user asks for rebase.

## Stack close risk

Merging a parent can delete its head on GitHub and auto-close children. After each parent merge, check children; if closed because the base branch vanished:

```bash
git push origin <parent-sha>:refs/heads/<parent-branch>
gh pr reopen <child>
gh pr edit <child> --base <base>
```

## Merge command

```bash
gh pr merge <N> --merge --delete-branch=false
```

`--squash` / `--rebase` only if the user asked. Keep `--delete-branch=false` during the walk.

## Dispose merge-queue worktree

**Remove** (`git worktree remove ../worktrees/merge-queue --force`) when:

- Closing build was already green (no repair), or repair PR merged; or
- Session had zero merges and user `stop`ped with no dirty repair work.

**Keep** the worktree when closing build is `blocked`, or the repair branch has unmerged commits — tell the user the path.

## Conflict resolution

Follow `resolving-merge-conflicts`. Prefer the queue item's intent against current base when intents clash; note trade-offs in the gate.
