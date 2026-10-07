---
name: conventions
description: Quick reference for Rely architecture, TypeScript, and Next.js patterns. Use when working in `hub/ui`, wiring Server Actions, shaping feature modules, or when the user asks for repo conventions and preferred patterns.
---

# Rely Quick Reference

Use this skill for fast reminders before editing. For domain language, read `CONTEXT-MAP.md` first, then the relevant `CONTEXT.md` and ADRs.

## Critical rules

**TypeScript**
- Explicit types on exported functions, parameters, props, and complex variables.
- Avoid `any`; use `unknown`, narrow it, or define a proper type.
- Prefer small, composable helpers over large multi-purpose utilities.

**App structure**
- `hub/ui` is one Next.js App Router app with two shells:
  - Admin: `hub/ui/src/app/[locale]/(admin)`
  - Station: `hub/ui/src/app/[locale]/stations/[stationId]`
- Keep the dependency flow one-way: `app` -> `features` / `components` -> `lib` / `hooks` / `types`.
- Pages and layouts compose from `features` and shared `components`; don't bury domain logic in route files.
- Features do not import from other features.

**Next.js**
- Prefer React Server Components by default.
- Add `'use client'` only when browser APIs, local state, or interactive libraries require it.
- Keep locale-aware routes under `app/[locale]`.
- Do not use `/api` routes for normal page reads when an RSC can fetch directly.

**Data flow**
- Read data in server components with Prisma or server-side data helpers.
- Write through Server Actions with `"use server"` at file level.
- Validate Server Action inputs with Zod through `next-safe-action`.
- Use TanStack Query only for highly interactive client behavior such as polling, optimistic updates, or live-ish views.

**Auth and boundaries**
- Keep auth UI and user-session helpers in `hub/ui/src/features/auth` or app-wide config in `hub/ui/src/lib`.
- Do not move pipeline or execution logic into the frontend.
- Station routes must stay station-scoped; no admin navigation or cross-station controls.

**UI composition**
- Reuse primitives from `hub/ui/src/components/ui` before adding new shared abstractions.
- Reuse `cn()` from `hub/ui/src/lib/utils`.
- Keep shared primitives and theme building blocks in `components/ui` and `styles`; keep domain widgets in `features`.

**Errors and feedback**
- Wrap async mutations in `try/catch`.
- Return typed action results like `{ success, data?, error? }`.
- Show user-facing failures with inline errors, alerts, or toasts; never fail silently.

## Common patterns

**Feature placement**
- Put route-local actions in `actions.ts` next to the route.
- Put reusable actions in `hub/ui/src/actions/<domain>.ts` or a feature `api/` folder.
- Keep feature internals inside `features/<name>/{components,hooks,types,utils,api}` as needed.

**When editing existing UI**
- Preserve current behavior and structure first.
- Restyle only when the task asks for visual changes.
- Add or update focused tests when the change affects behavior or a fragile branch.

## Quick checklist

- [ ] RSC by default, client only when needed
- [ ] Explicit TypeScript types
- [ ] Zod-validated Server Actions for writes
- [ ] No feature-to-feature imports
- [ ] Reuse existing primitives before creating new ones
- [ ] Domain language matches `CONTEXT.md`
