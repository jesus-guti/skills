# Plantilla de informe

Rellenar en español. Entregar como un único bloque Markdown.

```markdown
# Quality gate backend — [título corto del cambio]

- **Veredicto:** CONFORME | NO CONFORME
- **Fecha:** YYYY-MM-DD
- **Alcance:** [contextos y rutas]
- **Tipo:** feature | fix | contrato | schema | infra
- **Destinatario:** [equipo o contexto owner]

## Resumen ejecutivo

[3–6 líneas: qué se contrastó, resultado, riesgo principal si NO CONFORME.]

## Conformidad general (`G-*`, siempre)

| ID | Resultado | Nota |
|---|---|---|
| G-LAYERS | PASS/FAIL/N/A | |
| G-TRUTH | | |
| G-TENANT | | |
| G-FAIL-CLOSED | | |
| G-THIN | | |
| G-TRUST | | |
| G-HEAL | | |
| G-CHANGE | | |
| G-EVIDENCE | | |
| G-CODE | | |

## Conformidad por contexto (`S-*`)

Solo filas **aplicables** (borrar el resto). Menú:

`S-SEAM-UI-CP-EDGE` · `S-TRUTH-SOURCES` · `S-ENTRYPOINTS` · `S-TENANT-SCOPE` · `S-SCHEMA-ALEMBIC` · `S-CP` · `S-EDGE-RUNTIME` · `S-NATS` · `S-GRAPHIR-CATALOG` · `S-PLC-HOTPATH` · `S-OBJECT-STORE` · `S-CAPTURE` · `S-DOCKER` · `S-TESTS-OBS` · `S-CODE-GO` · `S-CODE-PY` · `S-DOCS-CONTEXT`

| ID | Resultado | Nota |
|---|---|---|
| | PASS/FAIL | |

## Hallazgos

### H1. [título]

- **Severidad:** bloqueante | mayor | menor
- **Estándar:** G-… (S-… si aplica)
- **Evidencia:** `path` — [qué hace el código]
- **Impacto:** [tenant, prod, contrato, operabilidad]
- **Solución (según estándar):** [cambio concreto en el módulo canónico]
- **Owner:** [hub/db | control-plane | flow-engine | contratos | infra]

(Repetir H2, H3…)

Si no hay hallazgos: *Ninguno. El diff cumple los estándares aplicables.*

## Plan de mejora

Ordenado. Cada ítem cierra un hallazgo.

1. **[H1]** — [acción] — owner — [criterio de hecho]
2. **[H2]** — …

### Fuera de este cambio (opcional)

Deuda visible no introducida por el diff. No mezcla con bloqueantes del cambio.

## Pruebas y cierre

- [ ] Tests / make targets a correr
- [ ] Contratos a regenerar (`make gen-nats-contracts`, Prisma pull, SCHEMA.md)
- [ ] Docs a tocar

## Decisión

[Mergeable con menores | No mergear hasta cerrar H… | Reabrir ADR-… ]
```
