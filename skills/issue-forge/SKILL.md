---
name: issue-forge
description: Forges LoadZone Linear tickets from informal prose — one concern, a heterogeneous inbox, or a hand-off to wayfinder/to-prd/to-tickets. Short-grills inferred intent, tags plan/risk/bundle for the orchestrator. Use when the user dumps work, asks to create issues or tickets, or says una issue.
---

# Issue forge

Product owner for **LoadZone**. Input is imperfect prose. Output is tracker tickets an agent can grab, or a **hand-off** to a planning skill you do not rewrite.

**Guess in the open, then grill the guess.** Infer what the work is for, mark it as inference, put the essential forks to the user before publishing.

**Label the route and the delivery unit.** `plan:`, `risk:`, `area:`, `bundle:` live on the first line of the body — that is what the `orchestrator` skill reads. Axes in `taxonomy.md`.

Destination, team, labels, language: `docs/agents/issue-tracker.md` plus the header rules in `issue-template.md`. Tracker is Linear (`JES-…`, project `LoadZone`). Fallback `.scratch/` only if the user asks or Linear MCP fails.

## Process

### 1. Scale

Count **concerns** — each independently verifiable. Then take one branch. Done when the branch is chosen and named in chat (one sentence).

| Branch | Test | What you do |
|---|---|---|
| **One concern** | The user named a single change, one bug, or said *una issue* / *un ticket* | Stay here. Skip inbox slicing and bundling. |
| **Inbox** | Two or more concerns that do not share one destination | Stay here. Heterogeneous by default: no shared PRD, no fake graph. |
| **PRD** | One coherent feature, way already clear, bigger than one session, needs a parent + tracer bullets | **Hand-off.** Ask the user to run `/to-prd`, then `/to-tickets`. Read those skill files for templates; do not edit them. Stop. |
| **Map** | Fog — the way to the destination is not visible yet, more than one session | **Hand-off.** Ask the user to run `/wayfinder`. Stop. |

A hand-off is complete when the user has the skill name to type. Forge does not publish that work, and does not impersonate those skills.

If they refuse the hand-off and still want tickets now, continue on **one concern** or **inbox** and say the parent/map will be thinner than those skills would have made.

### 2. Terrain and overlaps

For each concern you will forge: read the scraps it touches (`CONTEXT.md`, applicable `.cursor/rules/`, and for staff sessions / exercises / calendar / load work also `docs/agents/product-direction.md`). Titles use domain vocabulary (**Team**, **Player**, **DailyEntry**, **Exercise**, **Carga**, **Match Day**, …).

Search open Linear issues (team `Jesus-guti-workspace`, project `LoadZone`) and `.scratch/*/issues/`. Extend or `relatedTo` instead of duplicating.

Done when every concern has a title in domain words and a duplicate check.

### 3. Delivery units (inbox only)

Propose what the orchestrator turns into one worktree. Rules in `taxonomy.md` (`bundle:`). Default: one issue = one unit. Collapse same concern into one issue. Bundle only distinct `plan:direct` + `risk:low` siblings that share `area:` and can share a PR.

One-concern runs omit this step.

Done when every slice has a unit (solo or a shared `bundle:` slug) ready to grill.

### 4. Short grill

One AskQuestion round before publish (grilling shape: recommended option first, `(Recommended)`, slug `id`s). Essential forks only:

- Confirm the inferred intent (your guess as the recommended option).
- Inbox: confirm bundles vs keep-separate vs merge.
- At most one product fork per concern that would leave `plan:hitl` hollow.

Skip only if they said forge without questions **and** every slice is `plan:direct` with no product fork. Repo facts are your **legwork**.

Fold answers into the ticket body. Remaining escalation forks stay `plan:hitl` with a named recommendation.

Done when every fork in that round has an answer or an explicit skip.

### 5. Publish

Body from `issue-template.md` — same sections as `/to-tickets` (`Parent`, `What to build`, `Acceptance criteria`, `Blocked by`), plus quote, inference, no-goals, and the route header.

Linear: `save_issue` in dependency order, `blockedBy` only for real gates, `relatedTo` among a bundle. Labels: `agent-forged`, `ready-for-agent` (or `needs-info`), one of `Bug` / `Feature` / `Improvement`.

Chat index only: id+URL, title, type, `plan:`, `risk:`, `bundle:` or —, blocked by.

Done when every unit is on the tracker (or `.scratch/` fallback) and the index is in chat.

## Ticket quality

Explicit no-goals. Acceptance observable from outside. Assumptions recorded. Grill answers in the body. Paths/snippets only when they *are* the decision (type shape, schema, state machine).
