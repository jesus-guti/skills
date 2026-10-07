---
name: content-design
description: Write, review, and audit user-facing copy for Rely with strong i18n and industrial-UX constraints. Use when editing labels, buttons, errors, empty states, onboarding text, confirmation dialogs, or translation keys in `hub/ui`. Default to invisible UI; expand copy only when the user explicitly asks or the surface truly requires it.
---

# Rely Content Design

You are reviewing product copy for an industrial application. Clarity beats personality. Operators and admins should understand the action, risk, and next step on the first read.

## Default: invisible UI

Unless the user **explicitly** asks for explanatory copy, onboarding prose, section intros, or educational empty states:

- **Do not** add page titles, subtitles, helper text, tooltips, or info banners "for orientation".
- **Do not** translate `CONTEXT.md`, PRDs, or domain docs into user-facing paragraphs.
- **Do not** duplicate what the shell, navigation, field label, or data already communicates.
- Prefer **omitting** copy over writing a "helpful" explanation.
- When implementing UI (not a dedicated copy task), use the shortest viable label and stop.

Expand copy only when there is real operational need: destructive confirmation, blocking error, mandatory first-run flow, or explicit user request for more guidance.

## Modes

1. **Write**
   - Draft new UI copy for a specific surface.
   - Default: **one** minimal option unless the user asked for alternatives.
   - Return 1-3 ranked options only when the user asked to compare wording.
   - Include the suggested i18n key.
   - Add a one-line rationale **only** in dedicated copy-review tasks, not when shipping UI layout.

2. **Review**
   - Check existing copy against the rules below.
   - Flag **excess** copy first: redundant headers, intros, helper text, and domain summaries in the UI.
   - Then check terminology drift, weak actions, vague errors, and i18n issues.

3. **Audit**
   - Scan files for hardcoded strings, inconsistent terminology, and missing dictionary keys.
   - Prefer dictionary-backed copy over inline strings in components.
   - Flag surfaces that explain instead of operate.

## Where copy lives

- Primary dictionaries: `hub/ui/src/lib/i18n/messages/en.json` and `hub/ui/src/lib/i18n/messages/es.json`
- Feature UI: `hub/ui/src/features/**/*.tsx`
- Routes and shells: `hub/ui/src/app/**/*.tsx`, `hub/ui/src/components/**/*.tsx`

When editing copy:
- Prefer updating `en.json` and `es.json` together.
- Follow the existing key hierarchy instead of inventing a new pattern.
- If you find inline user-facing text in components, flag it unless there is a strong reason it cannot be localized.

## Key naming

- Match nearby sections such as `Common`, `Auth`, `Navigation`, `Station`, and `History`.
- Use nested objects for feature areas before adding flat keys.
- Use `camelCase` for leaf keys.
- Reuse existing generic labels like save, cancel, loading, and empty states when they already exist nearby.

## Copy rules

**Tone**
- Direct, calm, and precise.
- Sentence case for labels, titles, and buttons.
- Short sentences. No marketing language.
- Warmth is fine for onboarding **when the product already defines that surface**; never at the cost of clarity or brevity.

**Industrial context**
- Lead with the action or system state.
- Make risky actions explicit.
- Prefer concrete operational words over abstract product language.
- Do not assume the reader wants a tutorial on every screen.

**Errors**
- Include what happened.
- Include what the user can do next.
- If the cause is known, say it plainly.
- Never blame the user.

**Buttons and actions**
- Start with a verb.
- Name destructive actions specifically: `Delete station`, not just `Delete`.
- Use `Cancel` to stop an action and `Close` to dismiss information.

**Empty states**
- One short line by default.
- Add a primary action only when there is an obvious next step.
- Do not teach domain concepts or repeat page purpose unless the user asked for onboarding-style copy.

**Placeholders**
- Use realistic examples.
- Do not repeat the label.

**Page and section headers**
- Omit when shell and navigation already orient.
- Add a header only when navigation context is insufficient or a real decision needs framing.

## Terminology guardrails

- Use the product's existing domain terms consistently.
- When terminology is unclear, check `CONTEXT-MAP.md` and the relevant `CONTEXT.md` **for your own understanding** — not to paste summaries into the UI.
- If code, dictionaries, and docs disagree, surface the inconsistency instead of guessing.

## Review checklist

- [ ] No redundant titles, intros, helper text, or tooltips
- [ ] Copy is localized through `en.json` and `es.json`
- [ ] Key fits the existing feature hierarchy
- [ ] Sentence case and concise wording
- [ ] Button labels start with a verb
- [ ] Errors say what happened and what to do next
- [ ] Destructive actions name the exact thing affected
- [ ] Empty states are one line (+ action if needed), not essays
- [ ] Terminology matches the domain docs and nearby UI
