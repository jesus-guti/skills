---
name: jenkins-gate
description: >-
  Simula el pipeline Jenkins de Rely en local (lint, tests, gitleaks, Trivy,
  builds Docker) y repara hasta que el merge final no se rompa en rely-dev.
  Use when merge-queue entra en closing build, el usuario pide check o simular
  Jenkins, rely-dev está rojo, o hay que aterrizar integration en `dev`.
---

# Jenkins gate

`pnpm build` **no** es el pipeline. El *gate* es la paridad con `Jenkinsfile` (job `rely-dev`). Fuente de verdad: simulación local. Jenkins vivo es opcional (API autenticada).

Leer [STAGES.md](STAGES.md) para comandos y selección de imágenes; [FAILURES.md](FAILURES.md) para *signatures* y autonomía de repair.

## Cuándo

| Entrada | Path |
|---|---|
| merge-queue **Closing build** | `fast`; `images` si STAGES selecciona ≥1 |
| Land a `dev` | igual: `fast`; `images` del diff |
| Usuario pide las 9 imágenes | `fast` + `--integration-only` |
| Solo diagnosticar un rojo | reproducir el stage que falló, luego `fast` |

`images` = unión de nombres que STAGES mapea desde el diff. El land a `dev` no añade detector/anomalib ni el resto. Conjunto vacío → solo `fast`.

Nunca `deploy` ni `push` salvo petición explícita.

## Path `fast`

En el checkout del *gate* (worktree de merge-queue si aplica):

```bash
./scripts/verify-ci.sh --quick
```

Cubre workflows GHA + mismos stages Jenkins **Lint & Static Analysis** y **Test** (`ci-local.sh`: `go vet`, ruff, gitleaks, Trivy FS, `cp-test`, `test-stable`, `hub/db` test).

**Done when:** exit 0. Si falla: clasificar *signature* en FAILURES.md → *repair* → re-ejecutar el stage roto, luego otra vez `--quick`.

## Path `images`

Nombres desde STAGES (diff vs `origin/<source>`, source = fork, suele ser `dev`). `--integration-only` solo si el conjunto es las 9 de integration o el usuario las pidió.

```bash
TAG=dev-git-$(git rev-parse --short HEAD)
./scripts/pipeline-local.sh build --mode integration --tag "$TAG" --images <nombres>
./scripts/pipeline-local.sh scan --mode integration --tag "$TAG" --images <nombres>
```

**Done when:** build + Trivy image de esas imágenes en verde.

## Repair

Mismo bound que merge-queue: máximo **5** ciclos; la **misma** *signature* tras 2 intentos → `blocked`. Commits nuevos (HEREDOC, hooks on). En closing build, el arreglo va a `fix/merge-queue-build` y PR **hacia `integration`**.

Autonomía (detalle en FAILURES.md): FP de identificador → allowlist de cluster, auto. CVE Trivy → solo con *signature* ya documentada; si no, HITL. El stage sigue activo.

## Gate (último bloque del turno)

```
### Gate — Jenkins
Status: ready | blocked (<signature>)
Path: fast | fast+images
Failed stage: <none | lint-go | ruff | gitleaks | trivy-fs | test-* | docker:<img> | trivy-image>
Parity: local sim | local sim + live Jenkins
Repair PR: <url or n/a>
Reply: `merge` | `stop`
```

`ready` solo con `fast` verde (y `images` si este run lo exigía). No declarar listo porque `pnpm build` pasó.

## Live Jenkins (opcional)

Si existen `JENKINS_USER` + `JENKINS_TOKEN`: consultar `rely-dev` `lastBuild` según STAGES.md. Sin credenciales, no loguearse a la UI; el *gate* local basta.
