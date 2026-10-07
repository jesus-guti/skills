---
name: orchestrator
description: Coordina un lote de issues de LoadZone de principio a fin — worktrees, planificación en paralelo, decisiones con autonomía graduada, implementación por waves, PR y review. Agrupa issues con el mismo bundle: en un solo worktree. Usar cuando el usuario pide llevar varias issues a la vez, menciona "modo orquestador", pasa una lista de issues Linear/JES-*, o pide encadenar wayfinder → implementación → PR.
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

## Unidad de entrega

El issue-forge escribe `plan:` / `risk:` / `area:` / `bundle:` en la primera línea de la descripción. El orquestador no abre un worktree por issue: abre **uno por unidad de entrega**.

- Sin `bundle:` → esa issue es su propia unidad (rama `jgutierrez/jes-NNN-<slug>`).
- Mismo `bundle:<slug>` en varias issues → **una** unidad: un worktree, una rama `jgutierrez/bundle-<slug>`, un PR que cierra todas las issues del bundle.
- Si falta el header `bundle:` pero Linear las tiene `relatedTo` y todas son `plan:direct` + `risk:low` + misma `area:`, tratarlas como bundle y anotarlo en `BLOCKING.md`.
- Nunca mezclar en un bundle una issue `plan:auto` / `hitl` o `risk:med` / `high`. Si el forge las agrupó mal, separarlas y decirlo.

Un bundle `plan:direct` salta planificación (fase B) igual que una issue `direct` suelta. El implementador recibe la lista de issues y cumple los no-goals de cada una sin fusionar alcance.

## Ciclo

### A. Setup

1. Confirmar base branch (`dev` salvo acuerdo distinto) y `git fetch`.
2. Inventariar issues (equipo `Jesus-guti-workspace`, proyecto `LoadZone`). Leer de cada una la cabecera `plan:` / `risk:` / `bundle:` de la descripción, que fija la ruta: `direct` va directo a implementar sin planificador, `auto` planifica sin bloquearte, `hitl` planifica y espera. Agrupar por `bundle:`. Si falta la cabecera, clasificar con `autonomy-matrix.md`. Si el MCP de Linear no responde, trabajar con URLs y anotar "MCP offline".
3. Escribir el grafo de bloqueos en `.scratch/orchestration-<lote>/BLOCKING.md` (plantilla en `templates.md`), **una fila por unidad de entrega**, no por issue suelta dentro de un bundle.
4. Un worktree + rama por unidad de entrega, **siempre desde la base acordada**, nunca desde la rama actual del usuario:
   - path `../worktrees/loadzone/jes-NNN` o `../worktrees/loadzone/bundle-<slug>`
   - branch `jgutierrez/jes-NNN-<slug>` o `jgutierrez/bundle-<slug>`, o el `gitBranchName` de Linear si la unidad es una sola issue y Linear ya lo trae.

### B. Planificación en paralelo

Un subagente por unidad **que no sea `plan:direct`**, en su worktree. Las `plan:direct` (incluidos bundles directos) saltan a la fase D. Instrucciones que debe recibir:

- Leer la skill `wayfinder` y las reglas de dominio que apliquen (`loadzone-design-system`, admin shell, `CONTEXT.md`, `docs/agents/product-direction.md` para staff).
- Crear `.scratch/<effort>/map.md`.
- **Clasificar cada decisión** como `auto`, `assume` o `hitl` según `autonomy-matrix.md`, y resolver las `auto` y `assume` él mismo, registrándolas en el map con su nivel y, para las `assume`, cómo se revierten.
- No implementar, no commitear.
- Devolver el **informe de decisiones** con el formato de `templates.md`.

Tope duro: **máximo 3 `hitl` por issue**. Si el subagente necesita más, no pregunta: devuelve la issue marcada como mal definida y propone cómo partirla.

### C. Revisión (antes de implementar)

Al llegar cada informe, el orquestador entrega al usuario un bloque por unidad de entrega: primero las decisiones ya tomadas en una línea cada una, luego las `hitl` pendientes con recomendación.

El usuario puede:

- `JES-XXX: ok` — se implementa (o `bundle-<slug>: ok`).
- `JES-XXX: 3 → <otra cosa>` — revoca una decisión concreta; el orquestador reabre solo esa rama del map, no el plan entero.
- Responder las `hitl`.

Toda respuesta del usuario se escribe en `Decisions so far` del `map.md` del worktree antes de lanzar implementación. Los overrides del usuario mandan sobre cualquier recomendación previa.

### D. Implementación por waves

1. Wave 1: fundacionales e independientes, en paralelo (una unidad de entrega = un subagente).
2. Waves siguientes: al aterrizar la fundacional, se puede **mergear su tip en el worktree hijo** para avanzar en stack antes del merge a `dev`.
3. Respetar el grafo. Cada implementador: worktree only, decisiones ya cerradas (no reabrir HITL), commit con HEREDOC, push, resumen corto.
4. En un bundle, un solo implementador recorre las issues del slug en el mismo worktree, respeta los no-goals de cada una, y abre **un** PR que las referencia todas.

### E. PR y review

- `gh pr create` con base correcta (`dev` o la rama padre si es stack — avisar del riesgo de cierre, ver `git-runbook.md`). En un bundle, el cuerpo del PR lista cada `JES-NNN`.
- Skill `code-review` (ejes Standards + Spec) y `@cursor review` en el PR.
- Hallazgos **high**: fix en commit nuevo (nunca amend), push, y propagar a las PRs hijas del stack.

### F. Cierre

- "Libera worktrees" → `git worktree remove --force`, **manteniendo las ramas**.
- Si al mergear una base stacked GitHub borra la rama head y cierra las hijas, aplicar el remedio de `git-runbook.md`.

## Checklist por lote

- [ ] Base branch + fetch
- [ ] Issues inventariadas, bundles agrupados, `BLOCKING.md` escrito por unidad de entrega
- [ ] Linear actualizado o nota "MCP offline"
- [ ] Worktrees/ramas creadas desde la base (una por unidad, no una por issue bundlada)
- [ ] Planificadores lanzados en background (omitidos en `plan:direct`)
- [ ] Informe de decisiones entregado por unidad que planificó
- [ ] Respuestas y revocaciones escritas en los maps
- [ ] Implementación por waves según desbloqueo
- [ ] Commit + push + PR por unidad de entrega
- [ ] Review Standards/Spec + `@cursor review`
- [ ] Fixes high → push → propagados a hijas
- [ ] Worktrees liberados bajo petición

## Anti-patrones

- Crear un worktree desde la rama actual del usuario y contaminarlo con otra feature.
- Abrir un worktree por cada issue `plan:direct` + `risk:low` que comparte `bundle:`.
- **Auto-resolver una decisión clasificada `hitl`.** Auto-resolver `auto` y `assume` es lo esperado; saltarse una `hitl` no.
- Clasificar como `auto` algo que cumple un criterio de escalada para evitar preguntar.
- Implementar antes de que el usuario haya visto el informe de decisiones (salvo unidades `plan:direct`).
- Usar modelo fast cuando el usuario pidió low.
- `git add .`, amend o force-push sin petición explícita.
- Dejar worktrees montados cuando el humano necesita `gh pr checkout`.

## Recursos

- `autonomy-matrix.md` — cómo clasificar cada decisión.
- `templates.md` — `BLOCKING.md` e informe de decisiones.
- `git-runbook.md` — worktrees y PRs stacked.
