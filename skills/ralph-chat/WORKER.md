# Portable prompt assembly

The orchestrator builds a portable prompt the user copies into a fresh chat with the `implement` skill.

## Files to read (orchestrator)

For feature slug `<feature-slug>`:

| Source | Path |
|--------|------|
| PRD | `.scratch/<feature-slug>/PRD.md` |
| Issues | `.scratch/<feature-slug>/issues/*.md` (sorted) |
| Commits | `git log -n 5 --format=%H%n%ad%n%B--- --date=short` |
| Context | `CONTEXT-MAP.md`; follow to relevant per-context `CONTEXT.md` |

## Portable prompt template

Output exactly this for the user to copy-paste:

```markdown
## Ticket: <issue path relative to repo root>

<full issue content>

---

Implementa este ticket. Lee la PRD en `.scratch/<feature-slug>/PRD.md` para contexto completo.

Explora el repo antes de editar. Cambios pequeños y revisables. Respeta los límites de arquitectura documentados en `CONTEXT-MAP.md` y los `CONTEXT.md` relevantes.

Solo trabajes tickets `Type: AFK`. Si hay bloqueos no resueltos, repórtalo y no implementes.

Antes de terminar:
- Corre la validación más relevante (e.g. `pnpm typecheck`, `pnpm test`, `make cp-test`)
- Actualiza el issue file: cambia `Status:` al estado done correspondiente, marca checkboxes de acceptance criteria
- Si no terminaste, agrega una nota en `## Comments` con lo hecho y lo que falta
- Crea un solo commit local si el task está completo; no hagas push
```
