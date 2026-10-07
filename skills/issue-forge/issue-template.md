# Issue templates

Same body for Linear (`description`) and `.scratch/` files. Header differs. Section order matches `/to-tickets` so a forged ticket is a tracer-bullet ticket plus LoadZone routing.

Read `to-tickets/SKILL.md` (`<issue-template>` / `<local-ticket-template>`) if you need the upstream wording. Do not edit that skill. This file is the LoadZone superset.

## Header

**Linear** — first line of the description (not labels):

```markdown
`plan:auto` · `risk:low` · area: apps/app/wellness
```

Shared delivery unit (see `taxonomy.md`):

```markdown
`plan:direct` · `risk:low` · area: apps/app/wellness · bundle: wellness-hygiene
```

Area hints: `apps/app/…`, `apps/player/…`, `packages/design-system`, `packages/database`.

Labels: `agent-forged`, `ready-for-agent` (or `needs-info`), one of `Bug` / `Feature` / `Improvement`. Project `LoadZone`. Native `blockedBy` for gates.

**`.scratch/`:**

```markdown
# <NN> — <title>

**Status:** ready-for-agent
**Labels:** Feature · plan:auto · risk:low
**Bundle:** <slug, or omit this line>
**Blocked by:** <NN, or "None — can start immediately">
```

## Body

English. User quote literal (Spanish allowed inside the blockquote).

```markdown
## Parent

<Linear id+title of the PRD or wayfinder map, if this slice has one. Omit the section when there is no parent.>

## What Jesús asked

> <literal user text for this concern only>

## What I understand

<Inference, two or three sentences, including what the short grill confirmed.>

**Assumptions taken**
- <assumption> — <why it is reasonable>

**Open questions** (only if plan:hitl)
- <question> → recommendation: <option>

## What to build

<End-to-end behaviour from the user’s perspective — not a layer list.>

## No-goals

- <what this ticket explicitly does not do>

## Acceptance criteria

- [ ] <observable from outside>
- [ ] <observable from outside>

## Blocked by

- <blocking ticket id+title, or "None — can start immediately">
```

Omit **Assumptions taken** / **Open questions** when empty. Keep the quote block even when the rest is short.

## Bug

Replace **What to build** with:

```markdown
## Reproduction

1. <step>
2. <step>

**Expected:** <what should happen>
**Actual:** <what happens>
**Scope:** <since when, which environments, who is affected>
```

Bug acceptance always includes a regression test.

## Parent PRD

Forge does not invent a parallel PRD format. When the user refused a `/to-prd` hand-off and still wants a parent issue now, read the `<prd-template>` in `to-prd/SKILL.md` and use that as the parent Linear description (plus the LoadZone route header on line one). Link children via **Parent** and native `blockedBy`.
