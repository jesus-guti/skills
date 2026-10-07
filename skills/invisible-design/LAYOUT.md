# Spatial layout

Seven rules. Each one, checked at mobile width and at full laptop width, gets a verdict: pass, or the
violation named with its fix.

## 1. Eye path

The eye travels one predictable route. Violation: content pushed to the far corners with a void in the
middle, forcing an erratic top-left → right → bottom-left → centre jump.

Fix: anchor content on a modular grid. Mobile is one continuous vertical flow; desktop splits into
columns that preserve that same reading order, so the two versions teach the same layout.

## 2. Max-width

Wide screens must not stretch text, rows and inputs from edge to edge. Fix: centre the view in an
invisible frame — 1200–1280px is the usual landing spot — with real side margins. Body copy stays
inside its own measure regardless (see [READABILITY.md](READABILITY.md)).

## 3. Separation without cards

Group with **whitespace** (32–48px between blocks), **hairline** 1px low-opacity dividers between list
items and category boundaries, and weight/size contrast in type.

Violation: a card with fill and shadow wrapping a list, a table, or a whole section. Elevation belongs
to floating surfaces only — dialogs, popovers, menus, tooltips.

## 4. Heading hierarchy

One level of emphasis per level of meaning. Violation: stacked competing headings that all weigh the
same, or a heading restating the active tab (tab `Lesiones` → heading `LESIONES`).

Fix: delete the redundant heading, or demote it to a plain state descriptor.

## 5. Coupled context

A visual and the data it describes must be readable in one glance — adjacent columns, top-aligned.

Violation: a diagram floating detached, such as an anatomical body map at the bottom-centre while the
list of marked regions sits top-left. Fix: the visual in one column, its list and actions in the other,
so the mapping between them needs no scanning.

## 6. CTA placement

The primary action sits in the header of the module it acts on, or in the profile/top bar, right-aligned
on the same line as the section title. Violation: a primary button stranded mid-screen with no
operational context.

On mobile it becomes a floating action button or the primary action at the end of the flow. Secondary
actions (edit, discharge) drop to subtle tertiary weight or icon actions beside the item detail.

## 7. Filter grouping by function

Each filter sits next to what it filters, and controls of different kinds never share one group.

Violation: `Total · 2026 · Frente · Espalda` in a single button row, mixing a temporal filter with a
spatial one. Fix: the spatial view toggle becomes a flat segmented control on or beside the visual
itself; the period filter becomes a select or subtle text control on the history section header.
