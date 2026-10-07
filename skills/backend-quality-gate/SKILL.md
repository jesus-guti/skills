---
name: backend-quality-gate
description: Audits Rely backend, database, and runtime-service changes against product architecture and code-quality standards and produces an architect markdown report with findings and an improvement plan. Use whenever editing hub/db, hub/control-plane, hub/object-store, agents/flow-engine, agents/capture-agent, agents/plc-agent, agents/detector-agent, agents/anomalib-agent, contracts/nats, pkg/relynats, Alembic, NATS, pgx, SQLAlchemy, or Docker/compose for those services; also when adding a feature or fix in backend code, reviewing a PR, or the user mentions calidad, estándares, calidad de código, quality gate, o plan de mejora.
---

# Rely backend quality gate

Actúa como **arquitecto de software** de Rely. Contrasta el cambio (feature o fix) con los estándares de producto. Los estándares **siempre** deben cumplirse. Si no, el informe Markdown es el entregable para la persona responsable.

## Cuándo aplicar (obligatorio)

Aplicar en **cada** toque in-scope, no solo si el usuario pide review:

- `hub/db/**` (Alembic, modelos, schemas, repos, seed, Prisma slave, storage)
- `hub/control-plane/**`
- `hub/object-store/**`
- `agents/flow-engine/**`, `agents/capture-agent/**`, `agents/plc-agent/**`
- `agents/detector-agent/**`, `agents/anomalib-agent/**`
- `contracts/nats/**`, `pkg/relynats/**`
- Compose/Dockerfile/Makefile de esos servicios

**Fuera de alcance:** `hub/ui` (usar `design-system-rules` / skills de UI). Si el cambio es BFF/API en UI que **rompe** el seam `UI → CP → NATS → Edge`, sí auditar ese seam.

## Fuentes de verdad (leer antes de juzgar)

1. `CONTEXT-MAP.md`
2. `CONTEXT.md` del contexto tocado
3. ADRs de `docs/adr/` relevantes
4. `docs/EDGE_NATS_ARCHITECTURE.md` si hay runtime/NATS/CP/Edge
5. [STANDARDS.md](STANDARDS.md) — Parte A `G-*` (siempre) y Parte B `S-*` (por contexto). Un `S-*` no contradice su `G-*`.
6. Rules: `db_rely_general.mdc`, `models.mdc`, `schemas.mdc`, `repositories.mdc`, `control-plane.mdc`, `flow-engine.mdc`

No reinventar criterios. Si un punto no está en estas fuentes, marcarlo como **juicio de arquitectura** (no como estándar de producto).

## Flujo

1. **Acotar el cambio:** archivos, contexto(s), seam(s) afectados, tipo (schema / runtime / contrato / persistencia / infra).
2. **Puntuar cada `G-*`:** `PASS` (el diff lo respeta), `FAIL` (lo rompe), `N/A` (el diff no puede violarlo). `N/A` no es un aprobado fingido. Añadir solo los `S-*` del mapa por path (u otros si el diff los toca). Un incumplimiento = **un** hallazgo citado `G-*` + `S-*`, no dos filas duplicadas.
3. **Contrastar código vs estándar Rely.** Evidencia (ruta + comportamiento) + solución en el módulo que el estándar ya nombra. No Clean Code genérico, no “capa de servicio”, no relitigar ADRs.
4. **Veredicto:** `CONFORME` | `NO CONFORME`.
5. **Informe** con [REPORT-TEMPLATE.md](REPORT-TEMPLATE.md): tabla `G-*` completa; tabla `S-*` **solo filas aplicables**.

### Qué mostrar al usuario

- **NO CONFORME:** pegar el informe Markdown completo en el chat (listo para reenviar). No implementar el plan salvo que el usuario lo pida.
- **CONFORME** durante implementación: una línea `Calidad backend: CONFORME.` salvo que pidan el informe.
- **CONFORME** si pidieron review: informe corto (resumen + checklist PASS).

No mezclar este informe con el dump de CONTEXT. El MD es el artefacto.

## Cómo redactar (arquitecto)

- Un hallazgo = un incumplimiento (o un riesgo de incumplimiento).
- Citar primero el `G-*` de producto y, si aporta, el `S-*` de contexto (ej. `G-TENANT` / `S-TENANT-SCOPE`).
- Solución: **qué hacer en Rely**, con módulo/paquete y contrato canónico. Prohibido “añadir una capa de servicio” si el estándar ya nombra el sitio (`internal/reconciler`, `BaseRepository`, Alembic, `subjects.json`).
- Plan de mejora: ordenado por dependencia (contrato/schema → runtime → tests → docs).
- Destinatario: inferir (`hub/db`, `control-plane`, `flow-engine`, contratos, infra). Si cruza contextos, una sección por owner.
- Severidad: `bloqueante` (rompe invariante/tenant/contrato/prod) · `mayor` (deuda que no debe mergear) · `menor` (higiene).

## Veredicto

`NO CONFORME` si hay algún `bloqueante` o `mayor`. Los `menor` no tumba el veredicto pero van al plan.

No dar por cerrado un cambio in-scope con `bloqueante` o `mayor` abiertos.
