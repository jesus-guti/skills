# Signatures — por qué local “verde” ≠ Jenkins verde

Clasificar el log contra esta lista. Una *signature* = un fallo con remediación conocida. Infra (timeout, abort) no se “arregla” en código: *gate* `blocked` con la *signature*. El stage (gitleaks / Trivy) sigue activo.

## Repair — autonomía

| Clase | Acción |
|---|---|
| FP de identificador (gitleaks `generic-api-key` sobre nombre de campo, `*S3Key` / `*_s3_key`) | Auto: regex de **cluster** en `[allowlist].regexes` de `.gitleaks.toml` + comentario de justificación. Re-ejecutar `./scripts/ci-gitleaks.sh .`. |
| CVE Trivy con *signature* en la tabla | Auto: el repair de esa fila |
| CVE Trivy **sin** *signature* | HITL / `blocked`. No inventar entradas en `.trivyignore`. |

## Históricas (git `fix(ci)` / comentarios Jenkinsfile)

| Signature | Síntoma | Repair |
|---|---|---|
| `gitleaks identifier *S3Key` | `generic-api-key` en `intent.FrozenS3Key` / `FlowS3Key` / `weights_s3_key` | cluster `(?i)[A-Za-z0-9_.]*(S3Key\|s3_key)` en `.gitleaks.toml` |
| `trivy-fs golang.org/x` | HIGH/CRITICAL en módulos Go | bump en `go.mod` de CP/flow-engine (ver `006493c9`); no ignore ciego |
| `trivy-image debian FP` | CVE sin FIXED VERSION (p. ej. capture-agent) | CVE sola en `.trivyignore` + comentario **línea anterior** (Trivy 0.21 rompe si hay texto inline) |
| `trivy disk quota` / `fanal-*` | `/tmp` del agente lleno (anomalib) | pipeline ya usa `TMPDIR` en workspace; si persiste: disco del host, no código |
| `next build BUCKET_*` | `pnpm build` host OK, Docker hub-ui KO | defaults `BUCKET_*` en `hub/ui/Dockerfile` builder |
| `next build Zod/types` | error de tipos solo en `next build` | alinear schemas; el *gate* `images` lo caza, `pnpm dev` no |
| `Error 143` | build abortado | pushes seguidos + `disableConcurrentBuilds`; relanzar, no parche de producto |
| `Timeout waiting for agent` | docker build paralelo | Jenkinsfile ya serializa builds; no reintroducir `parallel` en Build |
| `gitleaks: command not found` | imagen Jenkins vieja | `scripts/ci-gitleaks.sh` autoinstala; rebuild `rely-jenkins` si falta el binario |
| `hub/db compose collision` | tests DB pisan contenedores | `COMPOSE_PROJECT_NAME` por job (Jenkins) / `ci-db-test` (local) |
| `deploy health-wait` | contenedores no `healthy` en 360s | fuera del *gate* local; cold start flow-engine ~4 min; no fingir deploy |

## Mejoras (pipeline y *gate*)

1. **Cerrar el *gap* merge-queue.** El closing build solo corría `pnpm build`. Obligar este skill en el close.
2. **Allowlist de identificadores S3**, no un regex por hallazgo.
3. **Una política Trivy.** Jenkins pinea 0.21 en dirs; GHA usa 0.36 en todo el repo. Subir Jenkins a una Trivy moderna (o bajar GHA) y escanear los mismos paths.
4. **Vet local con `CGO_ENABLED=0`** como el stage Jenkins (`ci-local.sh` hoy no lo exporta).
5. **Documentar 9 imágenes**, no 4 (`docs/ci-cd-workflow.md` desfasado).
6. **No simular deploy** en el *gate* de merge: muta dev-demo. Health-wait solo en Jenkins post-push.
7. **Credencial de lectura Jenkins** (`JENKINS_USER`/`JENKINS_TOKEN`) para el agente: hoy la API pública da 403; sin ella el *gate* es solo local (suficiente si `fast`/`images` son paridad real).
8. **Rebuild periódico de `ci/Dockerfile.jenkins`**: ruff se instala unpinned (`pip install ruff`); el host puede no tener ruff (fallback Docker latest) → drift de versión.

## Qué no es un fallo de producto

Agente caído en `post { cleanWs }`, `Error 143`, cuota de disco del daemon, webhook que no dispara. Reportar *signature* e infra; no abrir repair PR de app.
