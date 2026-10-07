# Taxonomy

Three independent axes on every issue, plus an optional delivery unit the orchestrator reads.

## Type → Linear label

Reuse labels that already exist in the workspace. Do not create new ones (except `agent-forged` once if missing — see SKILL.md).

| Label | When | Consequence |
|---|---|---|
| `Bug` | Observable behavior differs from expected | Template with repro, expected vs actual. Implement with the `diagnose` skill, not by planning |
| `Feature` | New capability for the end user | Needs explicit no-goals |
| `Improvement` | Improve something that already exists: refactor, performance, restyle, tooling | If refactor, acceptance is identical behavior |

Pure research (a spike) is `Improvement` with `plan:direct`; deliverable is a written answer, not code.

## `plan:` — how much planning is needed

Goes in the description header, not as a label. Consumed by the `orchestrator` skill.

| Value | Means | Orchestrator |
|---|---|---|
| `direct` | Nothing left to decide | Goes straight to implement |
| `auto` | Decisions exist, but all fall under `auto` / `assume` | Runs planner, reports what it decided, does not block the user |
| `hitl` | At least one decision meets the escalation criteria | Runs planner and waits before implementing |

Escalation criteria live in the orchestrator’s `autonomy-matrix.md`. When drafting, if a decision touches a shared contract, tokens or cross-cutting primitives, something irreversible, security or cost, or product scope, the issue is `plan:hitl` and that decision is named inside the issue as an open question with a recommendation.

LoadZone-specific escalation hints (in addition to the matrix):

- Changing `@repo/design-system` primitives or semantic tokens used by both `apps/app` and `apps/player`
- Player public-token / check-in security surfaces
- Domain vocabulary or persistence contracts for **DailyEntry**, **Player**, **Season**, consent, or care alerts

## `risk:` — blast radius

| Value | Radius |
|---|---|
| `low` | One screen or module; revertible with a revert |
| `med` | One full feature, or several consumers inside the same app/package |
| `high` | Crosses apps/packages, migrates data, or changes contracts others consume |

## `bundle:` — delivery unit (optional)

Goes in the description header. Consumed by the `orchestrator` skill: **one worktree, one branch, one PR per distinct `bundle:` slug** (and one per unbundled issue).

| When to set | When to omit |
|---|---|
| Several distinct issues, all `plan:direct` + `risk:low`, same `area:`, can ship in one PR | Anything `plan:auto` / `plan:hitl`, `risk:med` / `high`, or a different area |
| Trivial bugs and quick improvements on the same module | A single issue (no siblings) — omit rather than invent a one-issue bundle |
| User confirmed the grouping in the short grill | Heterogeneous inbox items that only arrived together |

Same slug on every sibling. Issues in a bundle stay separate Linear tickets (their own title, no-goals, acceptance) and are `relatedTo` each other.

**Collapse vs bundle.** Collapse two slices into *one* issue when they are the same concern. Bundle when they are different concerns that should still share a delivery unit.

## Valid combinations

- `risk:high` implies `plan:hitl`. Never `plan:direct`.
- `risk:low` + `plan:hitl` is valid and common: small but product-facing decision.
- A `Bug` is almost always `plan:direct`. If it needs `plan:hitl`, it is probably a desired behavior change and should be a `Feature`.
- A bundled issue is only `plan:direct` + `risk:low`. If a sibling needs planning, drop it from the bundle.
