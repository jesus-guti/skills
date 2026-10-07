# Plantillas

## Informe de decisiones

Lo que el subagente planificador devuelve y el orquestador pega al chat, una issue por mensaje. Sin preámbulo, sin resumen del plan.

```markdown
### JES-NNN — <título>

**Decidido**
1. <decisión> — <motivo en media línea>
2. <decisión> — <motivo>
3. [assume] <decisión> — <motivo>. Revertir: <cómo>

**Pendiente de ti**
A. <pregunta> → recomendación: <opción> porque <motivo>

**Riesgo**: <bajo|medio|alto> · **Bloquea a**: JES-XXX, JES-YYY
```

Si no hay `hitl`, se omite el bloque "Pendiente de ti" y se dice que la issue está lista para implementar.

Si la issue superó el tope de 3 `hitl`, el informe se sustituye por:

```markdown
### JES-NNN — mal definida

Necesita <N> decisiones de producto para poder planificarse. Propuesta de partición:
- <sub-issue 1>
- <sub-issue 2>
```

## BLOCKING.md

En `.scratch/orchestration-<lote>/BLOCKING.md`.

```markdown
# Lote <nombre> — grafo de bloqueos

**Base**: dev · **Fecha**: YYYY-MM-DD · **Linear**: <activo | MCP offline>

## Grafo

<diagrama ascii: quién bloquea a quién>

## Unidades de entrega

Una fila por **unidad de entrega** (issue suelta o bundle). Las issues dentro de un bundle van en la columna Issue, no en filas extra de worktree.

| Unidad | Issues | Rama / worktree | Bloqueada por | Estado |
|---|---|---|---|---|
| JES-NNN | JES-NNN | jgutierrez/jes-NNN-slug | — | planificando |
| bundle-wellness-hygiene | JES-12, JES-13 | jgutierrez/bundle-wellness-hygiene | — | implementando |

## Notas

- Bloqueos blandos (se pueden adelantar mergeando el tip del padre en el worktree hijo).
- Issues aplazadas y por qué.
```

El estado va de `planificando` → `esperando revisión` → `implementando` → `PR abierta` → `merged`.
