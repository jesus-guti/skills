# Stages — Jenkinsfile ↔ local

Job `rely-dev` (rama `dev`, modo `integration`). Job `rely-main` añade imágenes release y deploy prod; este *gate* no las corre salvo land a `main`.

Scripts canónicos (no reescribir el pipeline a mano):

| Jenkins stage | Local |
|---|---|
| (GHA workflows, XML jobs) | `./scripts/workflows-local.sh` |
| Lint Go (`go vet` CP + flow-engine, `CGO_ENABLED=0`) | `CGO_ENABLED=0 ./scripts/go-docker.sh hub/control-plane -- vet ./...` y lo mismo en `agents/flow-engine` |
| Python lint | `ruff check .` en `hub/db` (o imagen `ghcr.io/astral-sh/ruff`) |
| Secret scan | `./scripts/ci-gitleaks.sh .` |
| Trivy filesystem | dirs: `hub/control-plane`, `agents/flow-engine`, `hub/db`, `hub/engine-autoscaler`, `agents/detector-agent` — `trivy 0.21` + `.trivyignore` (vía `ci-local.sh`) |
| Test | `make cp-test` · `make -C agents/flow-engine test-stable` · `COMPOSE_PROJECT_NAME=ci-db-test make -C hub/db test` |
| Build + Security Scan | `./scripts/pipeline-local.sh build|scan --mode integration --tag dev-git-$(git rev-parse --short HEAD)` |
| Push / Deploy | **fuera del gate** |

Atalhos:

```bash
./scripts/verify-ci.sh --quick              # workflows + lint + test + gitleaks + trivy fs
./scripts/verify-ci.sh --integration-only   # lo anterior + docker build/scan de las 9
./scripts/ci-local.sh                       # solo lint/test/scans FS
```

## Imágenes integration (`rely-dev`)

`control-plane` `flow-engine` `capture-agent` `beacon-agent` `detector-agent` `anomalib-agent` `hub-ui` `robot-assistant` `migrate`

Release extra (`rely-main`): `engine-autoscaler` `watchdog` `guide`.

Dockerfiles: `case` de `scripts/pipeline-local.sh`. `hub-ui` hace `pnpm build` **dentro** de Docker (env de builder: `BUCKET_*` en el Dockerfile, no el `.env` del host).

### Selección desde el diff

```bash
git diff --name-only origin/<source>...HEAD
```

`<source>` = rama de fork (suele ser `dev`). Unión de nombres; sin matches → omitir path `images`. Conjunto = las 9 → `--integration-only` vale como atajo.

| Path en el diff | Imagen |
|---|---|
| `hub/ui/**` | `hub-ui` |
| `hub/control-plane/**` | `control-plane` |
| `agents/flow-engine/**` | `flow-engine` |
| `agents/capture-agent/**` | `capture-agent` |
| `agents/beacon-agent/**` | `beacon-agent` |
| `agents/detector-agent/**` | `detector-agent` |
| `agents/anomalib-agent/**` | `anomalib-agent` |
| `agents/robot-assistant/**` | `robot-assistant` |
| `hub/db/**` | `migrate` |
| `pkg/relynats/**` `pkg/capabilitypolicy/**` `pkg/flowkernel/**` `pkg/relynodes/**` `contracts/**` `scripts/catalog_*.py` | `control-plane`, `flow-engine` |
| `pkg/python/rely_frame_shm/**` `hub/db/runtime-edge/**` `hub/db/src/db_rely/storage/s3_client.py` | `flow-engine`, `detector-agent`, `anomalib-agent` |

Un `Dockerfile*` bajo el árbol de una imagen cuenta como esa imagen. `go.mod` / requirements de un agente, igual.

Subset (no las 9):

```bash
TAG=dev-git-$(git rev-parse --short HEAD)
./scripts/pipeline-local.sh build --mode integration --tag "$TAG" --images hub-ui
./scripts/pipeline-local.sh scan --mode integration --tag "$TAG" --images hub-ui
```

## Paridad / drift

- **Agente Jenkins** = contenedor `rely-jenkins` con Go 1.25, Node 20, pnpm 9, ruff (pip), **Trivy 0.21.0**, gitleaks 8.22.1, socket Docker del host. Timeout 45 min. Builds Docker **secuenciales** (paralelos matan el heartbeat).
- **Local `go-docker.sh`**: host `go` si existe; si no, `golang:1.25-bookworm`. Forzar paridad Jenkins: `FORCE_GO_DOCKER=1` y `CGO_ENABLED=0` en vet.
- **GHA `security-scan.yml`**: gitleaks = mismo script; Trivy FS = action **v0.36 en todo el repo**, no las 5 dirs de Jenkins. Un verde GHA-Trivy no implica verde Jenkins-Trivy y al revés.
- Jobs XML son Pipeline from SCM (`*/dev`, `lightweight: true`), no Multibranch: `BRANCH_NAME` suele ir vacío; el Jenkinsfile infiere por `JOB_NAME`.
- `docs/ci-cd-workflow.md` lista 4 imágenes de CI; el Jenkinsfile construye **9**. Creer al Jenkinsfile.
- Live API: `https://jenkins.relyqa.com/jenkins/job/rely-dev/lastBuild/api/json` con user/token. Sin credenciales → 403; no es bloqueo del *gate* local.

## Qué no cubre `pnpm build`

Compila `hub/ui` en el host. No corre gitleaks, ruff, `go vet`, tests Go/Python, Trivy, ni el `pnpm build` del stage Docker (Prisma debian engine, `BUCKET_*`, distroless). Es un preview de UI, no el *gate*.
