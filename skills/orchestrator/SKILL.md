---
name: orchestrator
description: Coordina un lote de issues de Rely de principio a fin — worktrees, planificación en paralelo, decisiones con autonomía graduada, implementación por waves, PR y review. Usar cuando el usuario pide llevar varias issues a la vez, menciona "modo orquestador", pasa una lista de issues Linear/SIA-*, o pide encadenar wayfinder → implementación → PR.
---

# Orquestador de lotes

El chat orquestador **no implementa**. Coordina subagentes, mantiene el grafo de bloqueos y decide qué se pregunta al humano y qué no.

Regla que define esta skill: **la mayoría de decisiones de planificación las toma el agente y se reportan; solo se bloquea en las que cumplen los criterios de escalada.** Ver `autonomy-matrix.md`.

## Comunicación

Español, conciso. No volcar informes de subagentes. Por wave, un solo mensaje: qué se decidió, qué falta por decidir, qué se está construyendo. Nunca pegar el `map.md` entero.

## Subagentes

- Modelo por defecto `cursor-grok-4.5-low`, salvo que el usuario pida otro. Nunca variantes `*-fast` si pidió `low`.
- `run_in_background: true`; el orquestador sigue atendiendo mientras corren.
- Cada subagente trabaja **solo dentro de su worktree**. Nunca en el repo principal.

## Ciclo

### A. Setup

1. Confirmar base branch (`dev` salvo acuerdo distinto) y `git fetch`.
2. Inventariar issues (equipo `SIALI` en Linear). Leer de cada una la cabecera `plan:` / `risk:` de la descripción, que fija la ruta: `direct` va directo a implementar sin planificador, `auto` planifica sin bloquearte, `hitl` planifica y espera. Si falta la cabecera, clasificar con `autonomy-matrix.md`. Si el MCP de Linear no responde, trabajar con URLs y anotar "MCP offline".
3. Escribir el grafo de bloqueos en `.scratch/orchestration-<lote>/BLOCKING.md` (plantilla en `templates.md`).
4. Un worktree + rama por issue, **siempre desde la base acordada**, nunca desde la rama actual del usuario:
   - path `../worktrees/rely/sia-NNN`, branch `jgutierrez/sia-NNN-<slug>` o el `gitBranchName` de Linear.

### B. Planificación en paralelo

Un subagente por issue **que no sea `plan:direct`**, en su worktree. Las `plan:direct` saltan a la fase D. Instrucciones que debe recibir:

- Leer la skill `wayfinder`, `conventions`, y las reglas de dominio que apliquen (`design-system-rules` para UI, `flow-engine.mdc` / `control-plane.mdc` para runtime).
- Crear `.scratch/<effort>/map.md`.
- **Clasificar cada decisión** como `auto`, `assume` o `hitl` según `autonomy-matrix.md`, y resolver las `auto` y `assume` él mismo, registrándolas en el map con su nivel y, para las `assume`, cómo se revierten.
- No implementar, no commitear.
- Devolver el **informe de decisiones** con el formato de `templates.md`.

Tope duro: **máximo 3 `hitl` por issue**. Si el subagente necesita más, no pregunta: devuelve la issue marcada como mal definida y propone cómo partirla.

### C. Revisión (antes de implementar)

Al llegar cada informe, el orquestador entrega al usuario un bloque por issue: primero las decisiones ya tomadas en una línea cada una, luego las `hitl` pendientes.

**HITL y grilling: siempre `AskQuestion`.** No pegar las `hitl` como lista markdown. Leer la skill `grilling` y recoger cada ronda (tope 3 `hitl` por issue) con una sola llamada `AskQuestion` que cubra el frontier; opción recomendada primera y con `(Recommended)` en el label. Lo mismo si un planificador o `grill-with-docs` escala al humano desde este chat.

El usuario puede:
- `SIA-XXX: ok` — se implementa.
- `SIA-XXX: 3 → <otra cosa>` — revoca una decisión concreta; el orquestador reabre solo esa rama del map, no el plan entero.
- Responder las `hitl`.

Toda respuesta del usuario se escribe en `Decisions so far` del `map.md` del worktree antes de lanzar implementación. Los overrides del usuario mandan sobre cualquier recomendación previa.

### D. Implementación por waves

1. Wave 1: fundacionales e independientes, en paralelo.
2. Waves siguientes: al aterrizar la fundacional, se puede **mergear su tip en el worktree hijo** para avanzar en stack antes del merge a `dev`.
3. Respetar el grafo. Cada implementador: worktree only, decisiones ya cerradas (no reabrir HITL), commit con HEREDOC, push, resumen corto.

### E. PR y review

- `gh pr create` con base correcta (`dev` o la rama padre si es stack — avisar del riesgo de cierre, ver `git-runbook.md`).
- Skill `code-review` (ejes Standards + Spec) y `@cursor review` en el PR.
- Hallazgos **high**: fix en commit nuevo (nunca amend), push, y propagar a las PRs hijas del stack.

### F. Cierre

- "Libera worktrees" → `git worktree remove --force`, **manteniendo las ramas**.
- Si al mergear una base stacked GitHub borra la rama head y cierra las hijas, aplicar el remedio de `git-runbook.md`.

## Checklist por lote

- [ ] Base branch + fetch
- [ ] Issues inventariadas + `BLOCKING.md` escrito
- [ ] Linear actualizado o nota "MCP offline"
- [ ] Worktrees/ramas creadas desde la base
- [ ] Planificadores lanzados en background
- [ ] Informe de decisiones entregado por issue
- [ ] Respuestas y revocaciones escritas en los maps
- [ ] Implementación por waves según desbloqueo
- [ ] Commit + push + PR por issue
- [ ] Review Standards/Spec + `@cursor review`
- [ ] Fixes high → push → propagados a hijas
- [ ] Worktrees liberados bajo petición

## Anti-patrones

- Crear un worktree desde la rama actual del usuario y contaminarlo con otra feature.
- **Auto-resolver una decisión clasificada `hitl`.** Auto-resolver `auto` y `assume` es lo esperado; saltarse una `hitl` no.
- Clasificar como `auto` algo que cumple un criterio de escalada para evitar preguntar.
- Implementar antes de que el usuario haya visto el informe de decisiones.
- Usar modelo fast cuando el usuario pidió low.
- `git add .`, amend o force-push sin petición explícita.
- Dejar worktrees montados cuando el humano necesita `gh pr checkout`.

## Recursos

- `autonomy-matrix.md` — cómo clasificar cada decisión.
- `templates.md` — `BLOCKING.md` e informe de decisiones.
- `git-runbook.md` — worktrees y PRs stacked.
