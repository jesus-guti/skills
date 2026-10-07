# Readability and legibility

Text is where invisible design is won or lost: badly set type forces the reader to work on decoding
instead of understanding. These are checkable numbers, not preferences — measure them, don't eyeball
them.

## Type

| Property | Minimum | Target |
| --- | --- | --- |
| Body size | 16px (1rem) | 16–18px; 17–18px on mobile, where viewing distance is greater |
| Any readable text | 12px | 14px for fine print, with contrast raised to compensate |
| Body line height | 1.5 | 1.4–1.6 |
| Heading line height | 1.1 | 1.2–1.3 — larger type needs less leading |
| Measure (characters per line) | 45 | 65–75; hard ceiling 80, and 45–60 on mobile |
| Type scale steps | 1.2× | 1.25–1.5×, one ratio for the whole scale |

Hold the measure with a `max-width` in `ch` (around `66ch`) rather than a pixel guess — different
fonts fit different character counts into the same width.

Prose is left-aligned, never justified: justification opens rivers of whitespace that break tracking.

## Contrast

| Target | Ratio |
| --- | --- |
| Normal text (under 24px, or under 18.5px bold) | 4.5:1 |
| Large text (24px+, or 18.5px+ bold) | 3:1 |
| UI components, icons, focus indicators, graphical objects | 3:1 |
| Extended reading, small type — aim here when you can | 7:1 |

Check every text role against **every** background it can land on, in light and dark. Secondary and
placeholder text is where this fails most often: muted grey that passes on white fails on a tinted row.

## Resilience

The layout must survive the user changing things:

- **200% zoom** with no overflow, clipping or overlap.
- **Text-spacing overrides** (WCAG 1.4.12): line height 1.5×, letter spacing 0.12em, word spacing
  0.16em, paragraph spacing 2× font size — applied together, with no loss of content or function.
  Fixed-height containers around text are the usual thing that breaks here.
- **Relative units** (`rem`/`em`) for font sizes so both of the above work at all.

## Cognitive accessibility

Where readers include dyslexic or low-vision users — which is everywhere — these tighten:

- Body 18px+, line height 1.5+, measure 45–60 characters.
- Sans-serif with distinctive letterforms (no ambiguous `Il1` / `O0`).
- Slightly increased letter and word spacing.
- Real text, never images of text.
- Plain language: short sentences, the user's vocabulary, one idea per paragraph.

## Quick check

- [ ] Body ≥16px in `rem`, line height ≥1.5
- [ ] Measure between 45 and 75 characters
- [ ] All text ≥4.5:1 (or ≥3:1 if large) on every background it appears over
- [ ] Focus indicators and icons ≥3:1
- [ ] No layout break at 200% zoom or under text-spacing overrides
- [ ] Left-aligned prose, no text below 12px, no images of text
