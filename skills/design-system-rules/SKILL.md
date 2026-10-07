---
name: design-system-rules
description: Review and enforce the Rely design system in `hub/ui`, including OKLCH tokens, open-layout composition, and compact Linear/Attio control density. Use when editing UI primitives, Tailwind classes, page layouts, or reviewing visual regressions and styling choices.
---

# Rely Design System Review Rules

Use these rules when working in `hub/ui/src/components/ui`, `hub/ui/src/features`, and `hub/ui/src/styles`.

## 1) Source priority

Prefer this order when choosing UI building blocks:

1. Existing primitives in `hub/ui/src/components/ui`
2. Semantic tokens from `hub/ui/src/styles/design-tokens.css`
3. New shared variants or helpers only when the existing primitives cannot express the need
4. Hardcoded visual values only as a last resort, with a clear reason

## 2) Token usage

Use semantic Rely tokens and mapped utilities, not raw palette guesses.

Flag these as violations:
- Tailwind color families like `slate-*`, `zinc-*`, `gray-*`, `neutral-*`, `stone-*`
- Hex colors, `rgb()`, `hsl()`, or ad hoc `oklch()` values in feature code
- Generic shadow utilities when a semantic shadow token should be used

Preferred token families include:
- Backgrounds: `bg-bg-primary`, `bg-bg-secondary`, `bg-bg-tertiary`, `bg-bg-quaternary`
- Text: `text-text-primary`, `text-text-secondary`, `text-text-tertiary`, `text-text-brand`
- Borders: `border-border-primary`, `border-border-secondary`, `border-border-tertiary`
- Semantic states: `brand`, `premium`, `success`, `warning`, `danger`, `info`

Severity: strong warning.

## 3) Open layout before boxed layout

Default to open page composition:
- Lead with spacing, stacking rhythm, and subtle dividers
- Do not wrap every block in a bordered card by default
- Use `--border-tertiary` style separators for ordinary grouping

Reserve full bordered containers and elevated surfaces for named exceptions:
- Forms
- Alerts and warnings
- Embedded technical surfaces
- Modals, drawers, inspectors, and other decoupled layers

Severity: warning when the layout looks card-heavy without a clear reason.

## 4) Compact control density

The interface is a desktop-first product in the Linear / Attio / macOS inspector tradition: dense, quiet, and precise. Do not enlarge controls for fat-finger or shop-floor touch. A control that looks oversized is a defect.

Canonical scale. Source of truth: `Button` `size` in `hub/ui/src/components/ui/button.tsx` and row height in `SectionChrome`. Do not invent a parallel scale in features. Dense controls and section bars step up on large screens; default controls do not.

| Role | Base | `xl` | `2xl` |
|---|---|---|---|
| Dense toolbar control (`sm`) | `h-8 min-h-8 px-2.5 text-[13px] rounded-lg` | same | `h-9 min-h-9 text-sm` |
| Dense icon (`icon-sm`) | `size-8`, glyph `size-4` | same | `size-9`, glyph `size-5` |
| Default control | `h-9 min-h-9 px-3 text-sm` | same | same |
| Comfortable (`lg`) | `h-10 min-h-10 px-4 text-sm rounded-lg` | same | same |
| Section bar row (`SectionChrome`) | `min-h-11`, pad `px-1.5` | `min-h-12`, pad `lg:px-2` | `min-h-14` |

Section bars:
- Top row always has `border-b border-border-tertiary`.
- A second row renders only when it has filters or badges, and that row owns its own `border-b`. An empty second row is a double border.
- Listing second row is one flex line: applied filters or badges on the left, date, filter, and layout controls on the right (`ml-auto`).

Flag as strong warnings:
- `h-12` and above on ordinary buttons, inputs, selects, or list rows
- `min-h-10` / `h-10` used as the default when the surrounding surface is a side panel, toolbar, or table
- Ad hoc `className="h-8"`, `h-9`, or `size-8` that overrides `size` and blocks the `2xl` step
- An inner `text-[13px]` (or `size-4` on the svg) that overrides the `sm` / `icon-sm` type scale
- A section bar stuck at `min-h-10` or `h-10` with no `xl:min-h-12` / `2xl:min-h-14`
- A second toolbar row that stays mounted when it has no filters or badges
- Mixed radii on the same row (`rounded-md` next to `rounded-lg` / `rounded-xl`) without a layer reason
- Icon-only hit areas below `size-8` (32px). 32px is the floor; 48px is not a goal

Severity: strong warning.

## 5) Focus, contrast, and mode support

All interactive states must stay obvious in light and dark mode.

Expected focus treatment:
- `focus-visible:outline-none`
- `focus-visible:ring-4`
- `focus-visible:ring-ring`
- `focus-visible:ring-offset-2`
- `focus-visible:ring-offset-background`

Flag:
- Weak or missing visible focus
- Styling that only works in one color mode
- Disabled states that still look interactive

Severity: strong warning.

## 6) Depth and motion

Use depth sparingly.

Flag:
- Tailwind shadows used as generic grouping tools
- Floating surfaces without semantic elevation intent
- Animation or timing values that do not match the existing system feel

Prefer `shadow-soft`, `shadow-elevated`, and `shadow-floating` only when the surface is genuinely layered.

## 7) Review checklist

- [ ] Reused an existing primitive before adding a new one
- [ ] Used semantic Rely tokens instead of hardcoded colors
- [ ] Preserved open-layout composition where possible
- [ ] Uses the compact density scale, including the `2xl` step on `sm` / `icon-sm` and the `xl` / `2xl` step on section bars
- [ ] Visible focus states in light and dark mode
- [ ] Uses semantic borders, depth, and state colors
