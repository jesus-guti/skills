# Plantillas de issue

El mismo cuerpo sirve para Linear (campo `description`) y para `.scratch/` (contenido del fichero). Solo cambia la cabecera.

## Cabecera

**En Linear** la primera línea de la descripción es la cabecera de ruta, porque `plan:` y `risk:` no son etiquetas:

```markdown
`plan:auto` · `risk:low` · área: hub/ui
```

Etiquetas de la issue: `RELY 2.0`, `agent-forged` y una de `Bug` / `Feature` / `Improvement`. Los bloqueos van en el campo nativo `blockedBy`, no en el texto.

**En `.scratch/`** la cabecera es:

```markdown
# <NN> — <título>

**Status:** ready-for-agent
**Labels:** Feature · plan:auto · risk:low
**Blocked by:** <NN, o "Ninguna">
```

## Cuerpo

```markdown
## Lo que pidió Jesús

> <texto del usuario, literal, sin reescribir. Recortar solo lo ajeno a esta issue.>

## Lo que entiendo

<Tu lectura de la intención, en dos o tres frases. Es inferencia y va marcada como tal.>

**Asunciones tomadas**
- <asunción> — <por qué es razonable>

**Preguntas abiertas** (solo si plan:hitl)
- <pregunta> → recomendación: <opción>

## Qué construir

<El comportamiento de punta a punta desde la perspectiva del usuario. No un listado de capas.>

## No-goals

- <lo que esta issue explícitamente no hace>

## Criterios de aceptación

- [ ] <observable desde fuera>
- [ ] <observable desde fuera>
```

Si no hay asunciones ni preguntas, se omiten esos bloques. Si el texto del usuario ya es preciso, "Lo que entiendo" puede reducirse a una frase — pero el bloque literal nunca se elimina.

## Bug

Sustituye "Qué construir" por:

```markdown
## Reproducción

1. <paso>
2. <paso>

**Esperado:** <qué debería pasar>
**Real:** <qué pasa>
**Alcance:** <desde cuándo, en qué entornos, a quién afecta>
```

Los criterios de aceptación de un bug incluyen siempre un test de regresión.

## PRD del lote

Solo si el lote es una feature coherente y el usuario lo pide. En Linear, un proyecto; en `.scratch/`, `PRD.md` en la carpeta de la feature.

```markdown
# <Feature>

## Objetivo

<Una o dos frases: qué cambia para el usuario cuando esto esté hecho.>

## No-goals

- <fuera de alcance del conjunto>

## Issues

| # | Título | Labels | Bloqueada por |
|---|---|---|---|

## Decisiones de producto ya cerradas

- <decisión> — <origen: conversación, ADR, issue previa>
```
