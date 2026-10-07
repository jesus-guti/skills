---
name: invisible-design
description: Audit and refactor a screen so it disappears — cognitive load, readability and legibility, scannable hierarchy, affordances and feedback, copy, and spatial layout. Use when the user says a screen "feels off"/"se siente raro", asks to review or refactor a page or its readability, or when another skill needs the rules to judge a UI.
---

# Invisible Design

The user's goal is never to use the interface — it is to finish a task. The interface is the medium,
and it becomes **visible** the moment it makes someone stop and think: where is that button, what
does this icon mean, which of these two actions is the real one, what does this filter apply to.
Every stop is a failure.

The test: after using the screen, can the user describe **what they did** without describing **how it
looked**? "I logged the injury in ten seconds" is a pass. "The buttons had a nice glow" is not.

Invisible is not empty and not undesigned — it is aesthetics in the service of the task. It is also
not cardified: boxes, borders, fills and shadows everywhere are saturation, not structure. Structure
comes from negative space, alignment, and typographic hierarchy.

## Run the audit

Walk **all six dimensions** below against the screen, at mobile width and at full laptop width. Each
dimension gets a verdict: pass, or a named violation with a concrete fix. A dimension you skipped is
a dimension that failed — a screen "feels weird" precisely because of the one thing nobody checked.

### 1. Cognitive load

Every element must earn its place by serving the task. Hunt the **extraneous** load: competing CTAs
where the primary one is not obvious, the same concept labelled differently on two screens, navigation
that reorders itself, decorative chrome that adds nothing, options offered where a sensible default
would do. Chunk what is inherently complex into smaller steps instead of one dense wall. Fewer
decisions, and the right one made obvious, beat more choices. For LoadZone staff screens, also apply
`docs/agents/product-direction.md`: success is less time in the app (not staff gamification).

### 2. Readability and legibility

Text is the interface. Body copy at 16px or more, line height 1.4–1.6, measure held to 45–75
characters, contrast at least 4.5:1 (3:1 for large text and for UI components and focus rings), and
nothing readable below 12px. Sizes in `rem`/`em` so the layout survives 200% zoom and user text-spacing
overrides. Numbers, thresholds and the full accessibility checklist: [READABILITY.md](READABILITY.md).

### 3. Scannable hierarchy

People scan before they read. One level of emphasis per level of meaning, so importance is legible at
a glance and the eye follows an F or Z path without backtracking. Violation: stacked headings that all
weigh the same, or a heading restating the active tab. Fix: delete the redundant one, or demote it to a
plain state descriptor.

### 4. Affordances and feedback

Every interactive element answers "what happens next?" before it is touched, and confirms what
happened after. Check: visible focus states, pending/loading feedback on anything asynchronous, a
result the user can see after a mutation, touch targets of at least 24×24px (44×44px where thumbs are
the input), and icons that carry a label unless the metaphor is universally understood. Silence after
an action is the interface making itself visible.

### 5. Copy

Labels use the user's vocabulary, not the codebase's. No internal mechanics, no state-machine names,
no prose explaining the logic on the page. Optional reference copy ("what does this do?", domain
definitions, caveats) belongs in an info icon + tooltip next to the title — never as a paragraph that
competes with the task. In this repo, product UI copy is Spanish and the domain vocabulary is the one
in `CONTEXT.md`.

### 6. Spatial layout

Predictable eye path, contained max-width on wide screens, separation by whitespace and hairlines
instead of cards, a visual sitting beside the data it describes, the primary CTA in the header of the
module it acts on, and filters grouped by function next to what they filter. The seven layout rules
with their violations and fixes: [LAYOUT.md](LAYOUT.md).

## Report, then refactor

Report the audit first: violation → dimension → fix, ordered by how much each one costs the user. Then
change code, and change nothing the audit did not name.

Apply fixes with the project's own tokens, spacing scale and primitives — an invisible screen built
from ad-hoc values is a new violation. In this repo: semantic tokens, 4px spacing multiples, and the
invisible list/table chrome in `.cursor/rules/loadzone-admin-shell.mdc`.

Done when all six dimensions have a verdict, every violation named has a fix landed, and the screen has
been re-read at both widths.
