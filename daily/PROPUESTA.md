# daily/ — propuesta (pendiente de aprobar)

Skills de uso diario para todos los agentes (Claude, Codex, Grok vía ~/.agents/skills).
Al aprobar: crear daily/skills/<nombre> y `skillshare link ~/github/jesus-guti-skills/daily/skills --name _daily --enable && skillshare sync`.

Evidencia de uso real (sesiones Claude Code, últimos 30 días): superpowers (plugin, ya cargado aparte) 74 usos, icm-architect 5, impeccable 1.
Las sesiones de Codex solo muestran el catálogo listado, no usos reales.

| Skill | Origen | Motivo |
|---|---|---|
| icm-architect | ~/.agents/skills.bak-skillsctl-20261116 | Usado 5× en 30 días; método ICM de sialos |
| context7-mcp | backup | Docs oficiales (Context7 está instalado) |
| pixijs (+ subskills que hagan falta) | backup | Solo si el sinóptico usa PixiJS: confirmar |
| tdd | skills/ | Base de trabajo |
| diagnose | skills/ | Depuración |
| code-review | skills/ | Revisión no-front |
| verification-loop | skills/ | Verificar antes de dar por hecho |
| git-workflow | skills/ | Commits/ramas |
| handoff | skills/ | Pasar trabajo entre agentes/cuentas (herdr) |
| to-spec | skills/ | Specs para openspec/superpowers |
| grill-me | skills/ | Afinar requisitos |
| codebase-onboarding | skills/ | Entrar en repos nuevos |
| deep-research | skills/ | Investigación |
| context-budget | skills/ | Medir tokens |
| skill-stocktake | skills/ | Auditar skills |
| writing-great-skills | skills/ | Escribir skills |
