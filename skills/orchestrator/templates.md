# Plantillas

## Informe de decisiones

Lo que el subagente planificador devuelve y el orquestador pega al chat, una issue por mensaje. Sin preámbulo, sin resumen del plan.

```markdown
### SIA-NNN — <título>

**Decidido**
1. <decisión> — <motivo en media línea>
2. <decisión> — <motivo>
3. [assume] <decisión> — <motivo>. Revertir: <cómo>

**Pendiente de ti** — no pegar A/B/C en el chat. El orquestador las lanza con `AskQuestion` (skill `grilling`): una ronda, opción recomendada primera.

**Riesgo**: <bajo|medio|alto> · **Bloquea a**: SIA-XXX, SIA-YYY
```

Si no hay `hitl`, se omite el bloque "Pendiente de ti" y se dice que la issue está lista para implementar.

Si la issue superó el tope de 3 `hitl`, el informe se sustituye por:

```markdown
### SIA-NNN — mal definida

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

## Issues

| Issue | Rama / worktree | Bloqueada por | Estado |
|---|---|---|---|
| SIA-NNN | jgutierrez/sia-NNN-slug | — | planificando |

## Notas

- Bloqueos blandos (se pueden adelantar mergeando el tip del padre en el worktree hijo).
- Issues aplazadas y por qué.
```

El estado va de `planificando` → `esperando revisión` → `implementando` → `PR abierta` → `merged`.
