# Taxonomía

Tres ejes independientes. Cada issue lleva uno de cada.

## Tipo → etiqueta de Linear

Reutilizar las etiquetas que ya existen en el workspace. No crear nuevas.

| Etiqueta | Cuándo | Consecuencia |
|---|---|---|
| `Bug` | Comportamiento observable distinto del esperado | Plantilla con repro, esperado vs. real. Se implementa con la skill `diagnose`, no planificando |
| `Feature` | Capacidad nueva para el usuario final | Necesita no-goals explícitos |
| `Improvement` | Mejora de algo que ya existe: refactor, rendimiento, restyle, tooling | Si es refactor, el criterio de aceptación es comportamiento idéntico |

Trabajo de investigación pura (un spike) va como `Improvement` con `plan:direct`, y su entregable es una respuesta escrita, no código.

## `plan:` — cuánta planificación necesita

Va en la cabecera de la descripción, no como etiqueta. Es el eje que consume la skill `orchestrator`.

| Valor | Significa | El orquestador |
|---|---|---|
| `direct` | No queda nada que decidir | Va directo a implementar |
| `auto` | Hay decisiones, pero todas caen en `auto`/`assume` | Lanza planificador, reporta lo decidido, no bloquea al usuario |
| `hitl` | Hay al menos una decisión que cumple criterio de escalada | Lanza planificador y espera respuesta antes de implementar |

Los criterios de escalada son los de `.cursor/skills/orchestrator/autonomy-matrix.md`. Al redactar, si detectas una decisión que toca un contrato compartido, tokens o primitives transversales, algo irreversible, seguridad o coste, o el alcance de producto, la issue es `plan:hitl` y esa decisión se nombra dentro de la issue como pregunta abierta con recomendación.

## `risk:` — radio de impacto

| Valor | Radio |
|---|---|
| `low` | Una pantalla o un módulo; revertible con un revert |
| `med` | Una feature completa, o varios consumidores dentro del mismo servicio |
| `high` | Cruza servicios, migra datos, o cambia contratos que otros consumen |

## Combinaciones válidas

- `risk:high` implica `plan:hitl`. Nunca `plan:direct`.
- `risk:low` + `plan:hitl` es válido y frecuente: decisión pequeña pero de producto.
- Un `Bug` es casi siempre `plan:direct`. Si necesita `plan:hitl`, probablemente no es un bug sino un cambio de comportamiento deseado, y debería ser `Feature`.
