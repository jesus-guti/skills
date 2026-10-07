---
name: issue-forge
description: Convierte un texto suelto del usuario, o la conversación actual, en issues de Rely bien formadas y etiquetadas por tipo, ruta de planificación y riesgo. Publica en Linear por defecto, o en .scratch si se pide. Acepta lotes heterogéneos — issues sin relación entre sí, de frontend, backend o infra a la vez. Usar cuando el usuario describe trabajo en prosa informal y pide crear issues o tickets.
---

# Issue forge

Actúas como product owner de Rely. La entrada es un texto explicativo pero imperfecto, a menudo un **volcado de varias cosas sin relación entre sí**. La salida son issues que un agente puede coger sin volver a preguntar.

Tres reglas gobiernan todo lo demás:

**El lote es heterogéneo por defecto.** No fuerces una feature común, un PRD ni un grafo de dependencias sobre issues que no lo tienen. La mayoría de lotes son una bandeja de entrada, no un proyecto.

**No inventes intención en silencio.** Cada issue separa lo que dijo el usuario de lo que tú infieres.

**Etiqueta la ruta, no solo el contenido.** Lo que hace útil una issue aquí es que diga cuánta planificación necesita y cuánto puede decidirse sola. Es lo que lee la skill `orchestrator`.

## Destino

**Linear es el destino por defecto.** Equipo `SIALI` (prefijo `SIA`), asignadas a **Jesús Gutierrez** salvo que el usuario indique otra persona. Solo publicar en `.scratch/` si el usuario lo pide, o si el MCP de Linear no responde — en ese caso avisar de que se ha usado el fallback.

Toda issue creada por esta skill lleva **siempre** dos etiquetas fijas:

- `RELY 2.0` — ya existe, agrupa el trabajo de esta línea de producto.
- `agent-forged` — ya existe, marca que la redactó esta skill y que hay inferencia dentro.

Además, **una** etiqueta de tipo reutilizando las que ya existen en el workspace: `Bug`, `Feature` o `Improvement`. No crear etiquetas nuevas. `plan:` y `risk:` no son etiquetas: van en la primera línea de la descripción (ver `issue-template.md`), donde el orquestador las lee.

## Proceso

### 1. Trocear el volcado

Primero separa el texto en asuntos independientes. Un asunto es una cosa que se puede terminar y verificar por su cuenta. Dos frases sobre la misma pantalla pueden ser un asunto o dos; dos frases sobre el editor de recetas y sobre NATS nunca son el mismo asunto.

Solo después, dentro de cada asunto, decide si necesita partirse en varias rebanadas verticales. Cada rebanada cruza todas las capas que toque y cabe en una sesión de agente. Para refactors amplios, expand–migrate–contract en vez de forzar la rebanada.

### 2. Leer el terreno

Para cada asunto, y solo para las áreas que toca: `CONTEXT-MAP.md` si existe y el `CONTEXT.md` correspondiente, más las reglas de `.cursor/rules/` que apliquen. Usa el vocabulario de dominio del repo en los títulos, no el del texto suelto. En un lote heterogéneo esto significa leer trozos distintos por issue — no leas el repo entero.

### 3. Buscar solapes

Antes de crear nada, buscar en Linear las issues abiertas del equipo y en `.scratch/*/issues/`. Si algo ya existe, no duplicar: proponer ampliar la existente, o crear la nueva con relación `relatedTo`. Un lote con duplicados hace que dos worktrees se pisen.

### 4. Etiquetar

Tres ejes, todos obligatorios. Detalle en `taxonomy.md`.

- **Tipo** → etiqueta Linear `Bug` / `Feature` / `Improvement`.
- **`plan:`** → `direct`, `auto` o `hitl`. Cuánta planificación necesita y si va a bloquear al usuario.
- **`risk:`** → `low`, `med` o `high`, por radio de impacto. Justifica el `plan:`.

Un `plan:` incoherente con su `risk:` es un error: `risk:high` con `plan:direct` no existe.

### 5. Relaciones

Solo declarar bloqueos **reales**. En Linear, `blockedBy` entre issues del lote; publicar en orden de dependencia para tener identificadores a los que referirse. Si dos issues no se gatean, no las relaciones aunque hayan llegado en el mismo mensaje. Usar `relatedTo` para vecindad temática sin bloqueo.

Añadir `PRD.md` o proyecto de Linear **solo** si el lote sí es una feature coherente y el usuario lo pide.

### 6. Publicar

- **Linear**: `save_issue` por issue, en orden de dependencia, con `team: "SIALI"`, `assignee: "Jesús Gutierrez"`, las etiquetas de la sección Destino y la descripción de `issue-template.md`. Estado por defecto `Backlog`; no meter en ciclo salvo petición.
- **`.scratch/`**: un fichero por issue. Si el lote es una feature, `.scratch/<feature-slug>/issues/<NN>-<slug>.md`. Si es heterogéneo, `.scratch/inbox-<YYYY-MM-DD>/<NN>-<slug>.md`. Estado `ready-for-agent`, o `needs-info` si quedan preguntas abiertas.

### 7. Devolver el índice

Al chat solo va una tabla: identificador y URL, título, tipo, `plan:`, `risk:`, bloqueada por. Después, las ambigüedades que no pudiste resolver, agrupadas como preguntas concretas. Nunca volcar el contenido de las issues al chat.

## Qué hace buena a una issue aquí

- **No-goals explícitos.** Es lo único que impide que un subagente expanda el alcance.
- **Criterios de aceptación verificables**: observables desde fuera, no "el código está limpio".
- **Sin rutas de fichero ni snippets**, salvo que el snippet codifique una decisión que la prosa no puede expresar (una forma de tipo, un esquema, una máquina de estados).
- **Las asunciones se registran, no se esconden.**

## Anti-patrones

- Agrupar en una feature o un proyecto issues que solo comparten el mensaje en que llegaron.
- Inventar bloqueos para dar sensación de orden.
- Reescribir el texto del usuario y perder el original.
- Presentar una inferencia tuya como si fuera un requisito suyo.
- Preguntar al usuario cosas que se responden leyendo el código.
- Crear etiquetas nuevas en Linear en vez de usar las que hay.
- Issues que son un listado de capas (schema, luego API, luego UI) en vez de rebanadas verticales.
- Copiar prosa de `CONTEXT.md` dentro de la issue en lugar de enlazarla.
