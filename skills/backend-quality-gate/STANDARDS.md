# Estándares de calidad backend Rely

Criterios de **producto Rely** (inspección industrial multi-tenant), no un catálogo genérico de “buenas prácticas”.

- **`G-*`**: siempre aplican a cualquier cambio backend/BD/runtime. Son los estándares verdaderos.
- **`S-*`**: cómo se concreta ese `G-*` en un contexto (db, CP, Edge, NATS, PLC…).
- Si no está aquí ni en CONTEXT/ADR/rules: **juicio de arquitectura**, no estándar de producto.

**Cobertura.** Arquitectura de producto (`G-*` / `S-*` de seam) **y** calidad de código (`G-CODE`, `S-CODE-GO`, `S-CODE-PY`). No es la skill de UI, ni de robot-assistant/MCP, ni de SLOs numéricos: si un cambio de esos rompe un `G-*`, se audita el `G-*`.

Cómo auditar cada ID: intención → debe/no debe → evidencia en el diff → violación típica → sitio canónico → severidad → fuentes.

---

# Parte A — Estándares generales (`G-*`)

Puntuar **cada** `G-*` como `PASS` / `FAIL` / `N/A`. `N/A` si el diff no puede romper ese invariante (un Field Pydantic no “pasa” `G-HEAL`: es `N/A`). Un `FAIL` de `G-*` tumba el veredicto aunque el `S-*` local se vea bien.

## G-LAYERS

**Intención.** Experiencia, coordinación, ejecución y persistencia no se mezclan. El atajo entre capas es el fallo típico de arquitectura en Rely.

**Debe.** Toda coordinación de runtime de planta sigue **UI → Control Plane → NATS → Edge**. Bytes e imágenes van por S3 / locator / SHM, no por el bus de control. Cada contexto posee lo que dice su `CONTEXT.md` y nada del vecino.

**No debe.** Un servicio “por comodidad” absorba el trabajo de otro (UI que deploya al Edge, Edge que escribe Postgres, CP que ejecuta frames, agents que importan Hub UI).

**Severidad.** Cruce de capa en planta: **bloqueante**. Detalle: `S-SEAM-UI-CP-EDGE`, `S-CP`, `S-EDGE-RUNTIME`.

## G-TRUTH

**Intención.** Un contrato, un master, el resto se genera. Dos masters = drift = incidente.

**Debe.** Schema → Alembic. Subjects → `contracts/nats/subjects.json` + codegen. S3 plataforma → `db_rely.storage` / `flowstorage`. Catálogo core nodos → pipeline CP + `check-node-catalog`. IDs → UUIDv7.

**No debe.** Prisma migrate, DDL en runtime, subjects literales, clientes S3 ad hoc, UUIDv4/secuencias, manifiestos de nodos a mano desfasados del Python.

**Severidad.** Master saltado: **bloqueante**. Codegen olvidado: **mayor**. Detalle: `S-TRUTH-SOURCES`, `S-NATS`, `S-SCHEMA-ALEMBIC`, `S-GRAPHIR-CATALOG`.

## G-TENANT

**Intención.** Isolation por organización (y estación en Edge) es invariante de producto, no un filtro de listado.

**Debe.** Toda lectura/escritura de datos de cliente lleva `organization_id` (repo `_tenant_filter` o WHERE explícito). Identidad Edge tipada `org_id` + `station_id`, inmutable en modo aislado. Jerarquía S3 `org/{org_id}/stations/{station_id}/...` en todos los modos. Features de estación vía **capabilities** efectivas, no flags sueltos por servicio.

**No debe.** Queries globales “de admin” sin seam. Override de scope por header en Edge aislado. Identidad en `os.environ` dentro de un nodo. Strings `"station:recipe"` como scope. FunctionNode como frontera entre orgs.

**Severidad.** Cross-tenant: **bloqueante**. Detalle: `S-TENANT-SCOPE`.

## G-FAIL-CLOSED

**Intención.** En planta, lo desconocido o irresoluble no “sigue adelante”. Un deploy/activate/resolve a medias es peor que un error explícito.

**Debe.** GraphIR compile (Hub y Edge) con los mismos códigos, **antes** de NATS. Pins/checksum/artifact de custom nodes. Resolve Object Store. PLC connect contra catálogo. IDs de assets de receta (`image_ids`, modelos) resolubles. Filtros de listado de object store cerrados (no barrer `base_path` por defecto).

**No debe.** Defaults permisivos (“si no hay pin, cargo latest”; “si no hay locator, subo el secreto en el grafo”; “si el puerto no existe, lo ignoro”).

**Severidad.** Fail-open en deploy/identidad/secretos: **bloqueante**. Detalle: `S-GRAPHIR-CATALOG`, `S-OBJECT-STORE`, `S-CP`, `S-EDGE-RUNTIME`, `S-PLC-HOTPATH`.

## G-THIN

**Intención.** Canales de control y ciclo son delgados. El producto escala por IDs, no por payloads.

**Debe.** Eventos de ciclo y HTTP/WS de runtime transportan identificadores (`element_id`, UUIDs) y metadatos. Píxeles: SHM/GCAP o S3. Grafos y pesos: S3 + IDs en el JSON persistido. Hydratación en Hub/BD/API, no en el webhook.

**No debe.** Base64, imágenes, detecciones/polígonos completos, grafo entero o secretos en NATS/WS/webhook/HTTP del engine.

**Severidad.** Evento gordo o secreto en canal de control: **bloqueante**. Detalle: `S-EDGE-RUNTIME`, `S-NATS`, `S-CP` (strip de blobs al persistir).

## G-TRUST

**Intención.** El grafo y la receta no son un almacén de secretos. El token interno no sustituye la red privada.

**Debe.** Credenciales de planta en Hub (`plc_connections`, Object Store connections). Edge resuelve por `connection_id` + APIs internas. Recetas se strippean de `_resolved_connection` y blobs runtime. `X-Rely-Internal-Token` en CP↔Edge y Object Store. APIs `resolve`/`object` y PLC agent en overlay privado, no LAN de planta ni Internet. Listados de connections **sin** secretos hacia la UI.

**No debe.** Secretos inline en `flow_config`. `http.Client` a pelo al Edge. Publicar puertos internos al host “para probar” en compose base.

**Severidad.** Secreto persistido o endpoint interno público: **bloqueante**. Detalle: `S-OBJECT-STORE`, `S-PLC-HOTPATH`, `S-CP`, `S-DOCKER`.

## G-HEAL

**Intención.** El Hub posee el desired state. El Edge se reconcilia; no tiene opinión persistida de “qué debería correr”.

**Debe.** Un runtime: Go-Brain. Al arrancar y al reconectar NATS: `POST /api/internal/reconcile-desired`. Mutaciones NATS→BD con QueueSubscribe (HA). Status: gana `ts_unix_ms` mayor. Inflight deploy hasta lifecycle/cancel.

**No debe.** Deploy autónomo desde disco. Segundo runtime Python-por-nodo. Dual-stack HTTP en un hot path que ya es UDS (PLC, captura).

**Severidad.** Desired state local en Edge: **bloqueante**. Detalle: `S-CP`, `S-EDGE-RUNTIME`, `S-CAPTURE`, `S-PLC-HOTPATH`.

## G-CHANGE

**Intención.** Un cambio de producto es código + contrato + imagen + prueba + contexto, no un PR a medias.

**Debe.** Schema: Alembic → Prisma pull → `SCHEMA.md`. NATS: JSON → `make gen-nats-contracts`. Prod: imagen `COPY`, bind-mount solo en overrides dev. Servicio nuevo: 3 niveles compose, desplegable solo. Vocabulario/seam: `CONTEXT.md` (+ EDGE_NATS si rompe HTTP/NATS).

**No debe.** Mergear contrato sin codegen. Bind-mount en base/prod. `.sh` como interfaz nueva. `.md` extra en `hub/db/`.

**Severidad.** Prod mutable o schema sin migración: **bloqueante**. Docs de contrato desfasadas: **mayor**. Detalle: `S-DOCKER`, `S-DOCS-CONTEXT`, `S-TESTS-OBS`, `S-ENTRYPOINTS`.

## G-EVIDENCE

**Intención.** El invariante se demuestra en el runtime real, junto al módulo que lo posee.

**Debe.** Tests al lado del paquete. Postgres real para `hub/db`. `make cp-test` / `stability-test` / `check-node-catalog` cuando el diff toca ese invariante.

**No debe.** Mockear `_tenant_filter` o Postgres. Silenciar fail-closed de GraphIR en un test “verde”.

**Severidad.** Seam de tenant/contrato/compile sin evidencia: **mayor**. Detalle: `S-TESTS-OBS`.

## G-CODE

**Intención.** El código de planta se opera a las 3 a.m. Tiene que ser localizable, tipado, con errores accionables y sin magia. Calidad de código es estándar de producto, no estilo opcional.

**Debe**

- **Idioma:** identificadores (paquetes, tipos, funciones, archivos, tablas) en **inglés**. Comentarios, docstrings y **logs de operador** en **español**. Mensajes de error que ve un operador: qué falló + qué implica, sin jerga de stacktrace crudo como único texto.
- **Nombres:** vocabulario de `CONTEXT.md` (Station, Recipe, Element, ExecutionScope, GraphIR…). No `data`, `manager`, `helper`, `util` como tipo de dominio. Un concepto = un nombre en todo el diff.
- **Módulos:** el comportamiento vive donde el estándar ya nombra el sitio (`BaseRepository`, `runtimeactivation`, `PersistWorker`, `graphircompile`, `internal/api/<area>`). Un archivo = una entidad en `db_rely`. `main`/wrappers finos. No pass-through (“service layer” que copia el handler). Testear la interfaz pública de ese módulo.
- **Higiene:** sin código comentado, imports muertos, duplicar `flowjson` / `db_rely.storage` / `pkg/relynats`. Lint: `make lint` (ruff) en `hub/db`; `go vet` / `lint` del módulo Go.
- **Tipos:** contratos explícitos (structs Go, Pydantic, `ExecutionScope`, enums en `db_rely.enums`). Prohibido `map[string]any` / `dict` / `interface{}` como modelo de un flujo nuevo si ya existe schema. JSONB queda para lo que el estándar marca flexible (config/meta).
- **Errores:** se devuelven, se envuelven con causa (`fmt.Errorf("…: %w", err)` / `raise … from`). Códigos estables de producto (`unknown_node_type`, `endpoint_not_in_catalog`, `contrib_*`) no se tragan ni se traducen a 500 genérico en el seam. No `panic` / `except Exception: pass` en hot path de request, deploy o persist. Go: `context.Context` primer parámetro en I/O; no ignorar `err` con `_` salvo write a métrica documentada.
- **Logs:** español, con `org_id`/`station_id`/`deploy_id` cuando el evento es de runtime. Nunca secretos, tokens, frames, snowballs completos ni `flow_config` entero.
- **Control de flujo:** fail-closed visible (early return). Goroutines/tareas: cancelación por `ctx`; no fugas al desconectar NATS.
- **Concurrencia y recursos:** cerrar rows/body/mmap/SHM en el mismo módulo que los abre. Tras `phase=ready` no retener el frame.

**No debe.** God-file nuevo. Copiar un bloque de otro servicio “y ya lo limpio luego”. Wrappers `_2` / `NewXxxImpl`. Comentarios que narran el código (`// incrementa i`). Inglés en logs de operador o español en nombres de API. Swallow de error para “que no falle el deploy”.

**Verificar.** Diff: nombres vs CONTEXT; `except:` / `_ = err`; `any`/`dict` donde hay schema; logs con payload; archivo +300 líneas de mezcla HTTP+SQL+NATS; lint no corrido.

**Violaciones típicas.** `utils.go` con tenant + S3 + UUID. `print`/`fmt.Println` de debug en CP/Edge. Traducir un error GraphIR a `fmt.Errorf("failed")` perdiendo el código. Pydantic `dict` para un Create que debería ser schema.

**Severidad.** Error tragado en deploy/persist/tenant: **bloqueante**. Tipos/god-file/logs malos: **mayor**. Higiene lint/comentario: **menor**. Detalle: `S-CODE-GO`, `S-CODE-PY`, `S-ENTRYPOINTS`.

### Relación G → S

| General | Se especializa en |
|---|---|
| G-LAYERS | S-SEAM-UI-CP-EDGE, S-CP, S-EDGE-RUNTIME, S-CAPTURE |
| G-TRUTH | S-TRUTH-SOURCES, S-SCHEMA-ALEMBIC, S-NATS, S-GRAPHIR-CATALOG |
| G-TENANT | S-TENANT-SCOPE |
| G-FAIL-CLOSED | S-GRAPHIR-CATALOG, S-OBJECT-STORE, S-CP, S-EDGE-RUNTIME, S-PLC-HOTPATH |
| G-THIN | S-EDGE-RUNTIME, S-NATS, S-CP |
| G-TRUST | S-OBJECT-STORE, S-PLC-HOTPATH, S-CP, S-DOCKER |
| G-HEAL | S-CP, S-EDGE-RUNTIME, S-CAPTURE, S-PLC-HOTPATH |
| G-CHANGE | S-DOCKER, S-DOCS-CONTEXT, S-TRUTH-SOURCES, S-ENTRYPOINTS |
| G-EVIDENCE | S-TESTS-OBS |
| G-CODE | S-CODE-GO, S-CODE-PY, S-ENTRYPOINTS |

---

# Parte B — Por contexto (`S-*`)

Aplicar los `S-*` del mapa de paths. No re-puntuar el mismo hecho como hallazgo aparte del `G-*`. `S-CODE-PY` no sustituye a `S-SCHEMA-ALEMBIC` (ORM/Alembic van ahí).

## S-SEAM-UI-CP-EDGE

**Intención.** Separar experiencia, coordinación runtime y ejecución en planta. Nadie “ataja” al vecino.

**Debe**

- Runtime de planta: `hub/ui` → Control Plane (HTTP/WS) → NATS → Edge.
- Inject/webhooks de planta: `POST /api/stations/{stationId}/inject|webhooks/{nodeId}` en CP; mismo subject NATS hacia Edge.
- CP: único con **pgx** para eventos de inspección/runtime y **WebSocket** de telemetría al editor/UI.
- Edge: ejecuta frames, telemetría, persist S3 off-path, `save_element` por NATS; **no** PostgreSQL.

**No debe**

- UI publicar NATS o llamar deploy/inject al Edge `:8000` en planta.
- `agents/` importar `hub/ui`.
- flow-engine servir WS de editor, mutar grafos de receta, o exponer catálogo NodeCatalog por HTTP/NATS.
- Duplicar modelos ORM o abrir SQLAlchemy/pgx en agents.
- Standalone (`FLOW_ENGINE_STANDALONE=true`: `POST /api/graphs/deploy|inject|stop`) usarse como diseño de planta. `http_writer` / `FLOW_HTTP_CONNECTIONS` son **solo standalone**.

**Verificar.** Nuevas rutas HTTP: ¿viven en CP `internal/api/<area>/` o en UI BFF hacia CP? ¿Hay cliente NATS en `hub/ui`? ¿Hay `sqlalchemy`/`pgx`/`DATABASE_URL` en flow-engine?

**Violaciones típicas.** “El Edge ya tiene HTTP, lo llamo desde Next.” “El worker Python escribe la fila en Postgres para ir más rápido.” Proxy UI → Edge sin token interno.

**Sitio canónico.** CP `internal/api/deploy`, `runtimeactivation`, `internal/consumer`. Edge `internal/agent/handlers`. Contrato: `docs/EDGE_NATS_ARCHITECTURE.md`.

**Severidad.** Cruce de seam en planta: **bloqueante**.

**Fuentes.** `CONTEXT-MAP.md`; CONTEXT de ui / CP / flow-engine; `docs/EDGE_NATS_ARCHITECTURE.md`.

---

## S-TRUTH-SOURCES

**Intención.** Un master por contrato. El resto se genera.

| Contrato | Master | Derivado | Prohibido |
|---|---|---|---|
| Schema SQL | Alembic `hub/db/alembic/versions` | SQLAlchemy; Prisma `db pull` + `generate`; copia a `hub/ui/prisma` | `prisma migrate`; DDL en CP/agents; `Base.metadata.create_all()` |
| Subjects NATS | `contracts/nats/subjects.json` | `make gen-nats-contracts` → `pkg/relynats`, `python/rely_nats` | strings de subject nuevos en Go/Python |
| S3 plataforma | `db_rely.storage` + CP `flowstorage.NewBuckets()` | mismos env (`S3_ENDPOINT`, buckets) | cliente S3/boto3 suelto; buckets hardcodeados distintos |
| IDs | UUIDv7 (`generate_uuid_v7()`, `uuid7()`, generadores Go del monorepo) | — | UUIDv4, secuencias, `Date.now()`, enteros de nodo |
| Catálogo nodos core | Python FIELDS + pipeline CP (`EnsureCoreNodesSynced`, `check-node-catalog`) | `node_definitions.definition_json` | manifest a mano desfasado del código |

**Verificar.** Diff de schema sin migración; subject literal (`rely.`, `station.`, wildcards inventados); `uuid.uuid4`; Prisma `.sql` de migrate.

**Severidad.** Master saltado: **bloqueante**. Codegen olvidado tras editar JSON: **mayor**.

---

## S-ENTRYPOINTS

**Intención.** `main` y wrappers son finos. El dominio es testeable en paquetes.

**Debe**

- Go: `cmd/*/main.go` parsea flags/env y cablea. Handlers y ciclo de vida en `internal/`.
- CP: rutas nuevas → `internal/api/<area>/`, no bloques en `main.go`.
- Edge: `agent.Run`; NATS en `internal/agent/nats_handlers.go` + `handlers/`; HTTP mínimo en `http_server.go`; reconcile en `reconcile.go`; scope en `scope.go`.
- Python engine: `wrapper.py` **solo** `--catalog` | `--field-action` | `--brain-mode`. Catálogo/`load_node_class` en `catalog_cli.py`; campo en `field_actions.py`; loop UDS en `brain_worker.py`. Si se mueve `load_node_class`, mantener re-export que usa el brain.

**No debe.** Reintroducir handlers NATS/HTTP largos en `main`. Un `wrapper.py` que importe negocio de nodos.

**Severidad.** Lógica de dominio en `main`: **mayor**. Wrapper hinchado: **mayor**.

---

## S-TENANT-SCOPE

**Intención.** Isolation por organización (y estación en Edge) es invariante, no un filtro opcional.

**Hub/db — debe**

- `BaseRepository[Model]` + `model = Model`. Constructor `(session, organization_id)`.
- Todo `select()` pasa por `self._tenant_filter(stmt)`.
- UPDATE/DELETE bulk: `organization_id` **en el WHERE** (el filter de select no aplica a `update()`).
- Paginación `CursorPage` keyset; nunca `OFFSET`.
- `selectinload()` en relaciones que salen a API (anti N+1).
- Excepciones al tenant: explícitas y documentadas en el repo.

**Edge — debe**

- Aislado (`RELY_MULTI_TENANT=false`): `ORGANIZATION_ID` + `STATION_ID` inmutables. Rechazar override por header, query, cookie o body.
- Dinámico (`true`): `org_id`/`station_id` del payload de deploy NATS. Tipo `ExecutionScope{OrgID, StationID}`; nunca `"station:recipe"` ni strings compuestos como identidad.
- Nodos Python: `self.rely_org_id`, `self.rely_station_id`, `self.rely_recipe_id` (o contexto inyectado). No `os.environ` para identidad.
- S3: `org/{org_id}/stations/{station_id}/...` en aislado y dinámico.
- CP atiende todas las orgs; subjects con prefijos truncados (`org8`, `stn8`); HTTP lleva UUID completos.

**No debe.** Query global “para admin” sin seam de autorización. Secretos de otra org en payload de receta. FunctionNode como frontera de aislamiento entre orgs (no lo es).

**Severidad.** Lectura/escritura cross-tenant: **bloqueante**. Scope stringly-typed: **mayor**.

**Fuentes.** `repositories.mdc`; flow-engine §6; CP CONTEXT § Multi-tenant.

---

## S-SCHEMA-ALEMBIC

**Intención.** El modelo de datos es el producto persistido. Alembic manda; el resto refleja.

**Paquete `db_rely`**

- `from __future__ import annotations` en todo `.py`.
- Un archivo = una entidad (`plc_connection.py`, no `plc.py` con tres clases). `snake_case.py`.
- Imports internos: `from db_rely.xxx import ...`.
- Enums **solo** en `enums.py`; tipo Python `(str, Enum)` en columna `String(N)`; nunca `sa.Enum` nativo PG.
- JSONB para config/meta/value flexibles; no proliferar columnas opcionales rígidas para cada marca/flag.

**Modelos** (`models.mdc`)

- Mixins: `PKMixin, TenantMixin, TimestampMixin, Base`. Omitir `TenantMixin` si el tenant llega por FK padre (`PlcSignal`, `Detection`, `View`, templates globales con `organization_id` NULL).
- PK: UUIDv7 vía `PKMixin` / `generate_uuid_v7()`.
- `__tablename__` snake_case plural. Columnas `Mapped[T]` + `mapped_column()`.
- FK a padre regular: `ondelete="CASCADE"`. Índices nombrados `ix_{tabla}_{columnas}` en `__table_args__`.
- Relaciones: imports en `TYPE_CHECKING`; `relationship("Clase")` string; `cascade="all, delete-orphan"` en colecciones hijas; `__repr__` de una línea.
- Registrar en `models/__init__.py` + `__all__`.

**Particiones** (`elements`, `views`, `detections`, `audit_log`)

- `PARTITION BY RANGE` mensual. PK compuesta `(id, timestamp|created_at)`. Columna de partición con `primary_key=True`.
- **Sin FK** entre particionadas: `primaryjoin` + `foreign_keys` en `relationship()`.
- FK desde particionada hacia tabla regular (p. ej. `Element.station_id`) sí.

**Schemas Pydantic** (`schemas.mdc`)

- Create: obligatorios + `Field(...)` y límites. Update: todo `Optional` `default=None`. Read: `ConfigDict(from_attributes=True)` + id + timestamps.
- Discriminated unions donde el dominio las tiene (detecciones). Configs por marca (PLC) + mapa; `extra="allow"` solo para `OTHER`.
- Registrar `schemas/__init__.py`.

**Migración y docs**

- Toda tabla/columna/constraint → Alembic. Luego `alembic upgrade head` → `prisma db pull` → `prisma generate` (`make up`).
- Actualizar `hub/db/SCHEMA.md`. No crear `.md` nuevos dentro de `hub/db/` salvo petición.

**Verificar.** Modelo nuevo sin migración; Prisma editado a mano; OFFSET; UUID default `gen_random_uuid()`; enum PG; FK `views.element_id` a nivel SQL.

**Severidad.** Schema sin Alembic o Prisma master: **bloqueante**. OFFSET / UUIDv4 en tabla nueva: **bloqueante**. SCHEMA.md desfasado: **mayor**.

---

## S-CP

**Intención.** El Control Plane traduce HTTP→NATS, persiste eventos y reconcilia desired state. No es un flow-engine.

**Debe**

- Responsabilidades: deploy/stop/inject HTTP, desired-runtime, reconciler, consumer NATS→pgx, WS telemetría, enrich S3, retention, catálogo, PLC commissioning, logs Loki.
- `POST /api/internal/reconcile-desired`: **único** disparador global de desired state. Coalescing (ventana mínima); cuerpo `{ "status": "ok", "triggered": boolean }`. Edge lo llama al **arrancar y al reconectar NATS**.
- Mutaciones NATS→BD: **QueueSubscribe** (HA, sin doble insert).
- Status coalescing: gana el evento con mayor `ts_unix_ms`.
- Inflight deploy por estación/receta hasta lifecycle o `cancel_ack`.
- Auth interna outbound CP→Edge: `auth.NewInternalHTTPClient` / `SetInternalTokenHeader` (`X-Rely-Internal-Token` = `RELY_INTERNAL_TOKEN`). Prod: token obligatorio en rutas internas.
- Proxy PLC live: `internal/api/edgehttp` PathPrefix `/api/stations/{id}/plc/` → flow-engine `/api/plc/`. Siempre inyectar token interno. Catálogo `connections` **no** se proxifica. Connect: host:port del body = `plc_connections.connection_config` activo (`plccatalog`, fail-closed `endpoint_not_in_catalog`).
- Enrich deploy: todo enricher de `NewDefaultPipeline` debe estar en `wiredEnricherPhases` / `Enrich`. Grafo canónico: IDs (`image_ids`, `reference_image_id`, `model_id`); strip de blobs `images[]` / `reference_image` al persistir. Fail-closed si no hay IDs resolubles. Recetas legacy sin `image_ids` usan filas `folder_gallery` del nodo.
- Activate: resuelve pines custom, **compila GraphIR** (`graphircompile`, mismos códigos que Edge) **antes** de NATS; adjunta `contrib_nodes`.
- Pool pgx: `CONTROL_PLANE_PG_MAX_CONNS` / `MIN_CONNS`. Sin DDL.

**No debe.** Ejecutar grafos, spawn workers Python, SHM, hot path de frames. Sustituir Alembic. `http.Client` a pelo hacia flow-engine.

**Paquetes (no reubicar dominio).** `internal/api/{deploy,station,internalsvc,plc,flowconn,logs}`, `reconciler`, `recipepersist`, `deployenrich`, `consumer`, `persistence`, `flowjson`, `flowstorage`, `runtimeactivation`, `nodecatalog`, `graphircompile`.

**Severidad.** Deploy sin GraphIR fail-closed / enricher huérfano: **bloqueante**. HTTP client sin token interno: **bloqueante**. Lógica de frame en CP: **bloqueante**.

**Fuentes.** `control-plane.mdc`; `hub/control-plane/CONTEXT.md`.

---

## S-EDGE-RUNTIME

**Intención.** Un runtime (Go-Brain). Frames por UDS+SHM. NATS es control/telemetría, no el bus de píxeles.

**Debe**

- Go orquesta; Python `--brain-mode pool|dedicated`. No proceso Python-por-nodo con pub/sub NATS de frames.
- Hot path: UDS + SHM. Contrato de píxeles: `views[]._gcap_path` o `views[]._shm_key`; consumidores `BaseNode.get_frame` / agentes NATS `read_view_frame`.
- Kernel GraphIR opaco (`pkg/flowkernel.Compile`). Pack Rely (snowball, sink, cámara, histórico) opcional. Join congelado en **tres** caminos (no unificar): Go `accumulateJoin`, Go `mergeJoinSnowballMsg`, Python `merge_snowballs`.
- Puertos: `trigger` | `image-ref` | `json` | `snowball` (`any` legado = snowball). `json`→`snowball` sin adaptador = fail-closed `port_type_mismatch`. `trigger`→`snowball` permitido.
- Deploy fail-closed: `unknown_node_type`, `dangling_edge`, `empty_node_id`, `duplicate_node_id`, `unknown_port`, `cyclic_graph`. CP corre el mismo `Compile` antes de NATS.
- Thin events / canales: identificadores (`element_id`, UUIDs) y metadatos. **Prohibido** imágenes embebidas, base64, polígonos/detecciones completas, grafo entero por HTTP/WS/webhook de ciclo.
- Persist: `internal/relypack.PersistWorker` / `persist_offpath.py` vía `db_rely.storage`. Dual-quality según `RELY_PERSIST_IMAGE_FORMAT`. Tras `phase=ready` se libera SHM+lane; `save_element` sigue en background.
- Detector/seg/cls: `agents/detector-agent` + `internal/detectorproxy` (NATS request-reply + SHM), no YOLO in-process en el brain como diseño nuevo.
- Custom org: no importar `rely_nodes.inspection`, snowball, `rely_nodes.core` ni `rely_nodes.io`. `from rely_nodes import BaseNode` sí. Un fichero `{node_type}.py`. Allowlist `contracts/nodes/org_custom_import_allowlist.json`. Cache `RELY_CONTRIB_DIR` en deploy.

**No debe.** Redeploy local desde disco al reconectar. NATS en el hot path de frames. PostgreSQL desde Edge. Catálogo de editor en el Edge.

**Severidad.** Postgres/DDL en Edge, o frames por NATS, o eventos gordos: **bloqueante**. Unificar joins o relajar fail-closed GraphIR: **mayor** (suele ser **bloqueante** si rompe contrato de ciclo).

**Fuentes.** `flow-engine.mdc`; `agents/flow-engine/CONTEXT.md`; `docs/SNOWBALL_CONTRACT.md`; ADR-020.

---

## S-NATS

**Intención.** El bus es un contrato versionado, no strings de conveniencia.

**Debe**

- Editar `contracts/nats/subjects.json` y correr `make gen-nats-contracts`.
- Wrappers: Edge/CP `internal/natsbus` sobre `pkg/relynats`. Python generado en `rely_nats`.
- Payloads de deploy: `org_id`, `station_id`, `recipe_id`, `flow_config`, `deploy_id`, `is_test` cuando aplique; `contrib_nodes` si hay custom.
- Cola de mutaciones en CP: QueueSubscribe. Telemetría status/log/lifecycle; persist `save_element`; presencia.

**No debe.** Subject mágico en un handler. Payload de inspect con bytes. Duplicar el JSON de subjects en un `.go` a mano.

**Severidad.** Subject no generado: **bloqueante**. Campo de identidad ausente en deploy: **bloqueante**.

---

## S-GRAPHIR-CATALOG

**Intención.** NodeCatalog (editor) ≠ NodeRuntime (Edge). Custom org es carril B (ADR-020), no un plugin suelto.

**Debe**

- Core: sync al arrancar CP + `make check-node-catalog` anti-drift.
- Publish custom: API interna Platform (`publish-node`); pin `package_version`+checksum en Flow; activate valida en servidor.
- Visibilidad: `required_capability` + capabilities efectivas de estación.
- Compile GraphIR en Hub **y** Edge con los mismos códigos de error; fail-closed antes de NATS.

**No debe.** Nodo custom NATS-proxy o Go ingest (B1: solo Python worker). Detector/anomalib/cámara industrial sustituidos por custom. Imports fuera de allowlist. Publicar custom sin ser Platform/superadmin.

**Severidad.** Drift catálogo/runtime o activate sin compile: **bloqueante**.

**Fuentes.** ADR-010, ADR-020; CP CONTEXT § NodeCatalog.

---

## S-PLC-HOTPATH

**Intención.** PLC de ciclo es RLCP/UDS, no HTTP loopback (ADR-021).

**Debe**

- Nodos `plc_read` / `plc_write` / `plc_wait` → `go_plc_client` (UDS) → Go RLCP → `rely-plc.sock` → plc-agent.
- Sesión Go keyed por `connection_id`; endpoint congelado en deploy (`_resolved_signal.endpoint`).
- Lecturas compartidas: `InterestBank` + `ReadMany`. `plc_edge` es fuente de ciclo (flanco BOOL → `RunFrame`).
- Commissioning: BFF/CP HTTP → FE `/api/plc` traduce a RLCP. Credenciales de planta en Hub (`plc_connections`); listado `GET /api/stations/{id}/flow/connections` **sin secretos**.
- Nodos kernel (`delay`, `function`, `inject`, `switch`, …) **no** llevan `connection_id`.

**No debe.** Nuevo hot path PLC por `FLOW_ENGINE_HTTP_BASE/api/plc`. Python hablando RLCP directo al sock. Secretos en el grafo persistido (mismo espíritu que Object Store).

**Severidad.** HTTP en hot path PLC nuevo: **bloqueante**.

**Fuentes.** ADR-021; flow-engine CONTEXT § PLC.

---

## S-OBJECT-STORE

**Intención.** Buckets del cliente ≠ S3 de plataforma. Trust boundary explícita (ADR-019).

**Debe**

- Servicio `hub/object-store` (`db_rely.object_store_api`): catálogo, browse, resolve Edge, proxy de bytes.
- Edge resuelve `connection_id` **solo** vía `OBJECT_STORE_INTERNAL_URL` + token interno.
- `GET .../object`: objectKey bajo `base_path` de la connection.
- Locator de View (`views.image_locator`): `kind=platform` vs `kind=org_object_store`; no copiar bytes a plataforma en el segundo caso.
- Token interno obligatorio con el módulo on, salvo flag explícito de dev inseguro.
- APIs `resolve`/`object` en red privada Hub↔Edge; no publicar a LAN de planta ni Internet. Compose: no publicar puerto host por defecto.

**No debe.** Snapshots `_resolved_connection` o secretos inline en recetas (Edge rechaza; persist strippea). Presign al browser como diseño v1 de review. Confundir RustFS de plataforma con Object Store org.

**Severidad.** Secreto en grafo o resolve sin token/red privada: **bloqueante**.

**Fuentes.** ADR-019; `docs/ORG_OBJECT_STORE_CONTRACT.md`; `hub/db/CONTEXT.md` (View Image Locator).

---

## S-CAPTURE

**Intención.** Cámaras industriales son sidecar (ADR-007), no lógica metida en el brain.

**Debe**

- `agents/capture-agent`: ring buffer, RLCP UDS, RCAP HTTP, SHM compartido con flow-engine.
- Emparejamiento y transporte según docs de captura; Hub no habla GenICam directo.

**No debe.** Reimplementar GenICam dentro de `rely_nodes`. Montar el agent como librería Python del worker.

**Severidad.** Dual-stack de captura sin ADR: **mayor** / **bloqueante** si rompe SHM.

**Fuentes.** `agents/capture-agent/README.md`; ADR-007; `docs/industrial-camera-nodes.md`.

---

## S-DOCKER

**Intención.** Prod reproducible. Dev rápido sin contaminar la imagen.

**Debe**

- Dockerfile: código vía `COPY`. Target `base`/prod inmutable. Target `dev` + **overrides** aparte para bind-mount.
- Jerarquía 3 niveles: servicio (desplegable solo) → módulo `include` → raíz. `make prod-hub` vs `make prod-agents`.
- Perfiles compose existentes (`setup`, `flow`, `ui`, `proxy`, `test`, `tools`).
- Ejecutar vía `make` / compose. Makefile de BD: `hub/db/Makefile`; raíz delega `$(MAKE) -C hub/db`.

**No debe**

- Bind-mount de código en compose **base** o prod (`./src:/app/src`, python del monorepo en el yaml de planta).
- Scripts `.sh` nuevos como interfaz (preferir Make). Reescribir `docker-compose.yml` raíz sin necesidad explícita.
- Un mount de archivo encima de un directorio `:ro` anidado (rompe el árbol). Go/C: rebuild, no bind-mount “por si acaso”.

**Overrides permitidos (únicos).** `agents/flow-engine/docker-compose.dev.yml` (python, detector/anomalib, `db_rely` → `/opt/db_rely`). `hub/docker-compose.dev-code.yml` (object-store `--reload`, migrate/seed).

**Severidad.** Bind-mount en prod/base: **bloqueante**. Servicio nuevo solo en la raíz: **mayor**.

---

## S-TESTS-OBS

**Intención.** El invariante se demuestra junto al paquete, en el mismo runtime Docker.

**Debe**

- Go: `*_test.go` al lado (`internal/api/*`, `flowjson`, `recipepersist`, `consumer`, `deployenrich`, …).
- `hub/db`: pytest-asyncio contra **PostgreSQL real** (compose test); nunca mock del motor SQL.
- Targets: `make cp-test` en cambio sustancial CP; `make stability-test` si toca engine+CP de verdad; `make check-node-catalog` si toca FIELDS/core nodes.

**No debe.** Tests que “pasan” mockeando `_tenant_filter`. Silenciar fail-closed de GraphIR/FunctionNode.

**Severidad.** Sin test en seam de tenant/contrato: **mayor**. Mock de Postgres en db: **mayor**.

---

## S-CODE-GO

**Intención.** El runtime (CP, Edge, capture, `pkg/relynats`) es Go idiomático y operable.

**Debe**

- `context.Context` primero en funciones con I/O, NATS, SQL, HTTP. Respetar cancelación (reconnect NATS, `Stop()`, `WaitStationIdle`).
- Errores: `fmt.Errorf("acción: %w", err)`; comparar con `errors.Is` / `errors.As` en códigos de producto (`ErrContribPinMissing`, GraphIR). HTTP/NATS mapea esos códigos, no un string libre.
- Paquete = área (`internal/api/deploy`, `internal/agent/handlers`). Tests `*_test.go` en el mismo paquete o `package foo_test` si se testea la interfaz pública.
- `go vet` / `make lint` del módulo; `go mod tidy` si cambian deps. No `init()` con I/O. No `log.Fatal` en librerías internas.
- Concurrencia: QueueSubscribe ya es el patrón de mutación; no `go func()` sin `ctx` ni `WaitGroup`/errgroup en el ciclo de vida del proceso. No data races en coalescer de status (el que gana es `ts_unix_ms`).
- JSON: tipos en `internal/flowjson` y contratos; no segundo parser de ShortUUID/LacksNodes.

**No debe.** Ignorar `err`. `panic` en handler. Duplicar subjects. `http.Client` global sin timeouts hacia Edge.

**Severidad.** `err` ignorado en persist/deploy: **bloqueante**. Paquete basura / race: **mayor**.

**Fuentes.** `control-plane.mdc`, `flow-engine.mdc`; estilo existente en `runtimeactivation`, `consumer`.

---

## S-CODE-PY

**Intención.** Python de `db_rely`, workers del engine y nodos es 3.11+, tipado y con ruff.

**Debe**

- Ruff (`make lint` en `hub/db`; py311, line-length 100). Alembic versions fuera del lint de app.
- `from __future__ import annotations` e imports `from db_rely.xxx` en `db_rely`. ORM/Pydantic/enums: ver `S-SCHEMA-ALEMBIC`.
- Async: `AsyncSession`; no `time.sleep` ni SQL sync en el event loop.
- Nodos/brain: `self.rely_*`; `get_frame` / SHM; no `print` de producción. Custom org: un fichero + allowlist.
- Excepciones: no `except Exception: pass`. S3 vía `db_rely.storage`.

**No debe.** `uuid.uuid4` para PKs. `create_all`. `os.environ` para org/station en nodos. `dict` crudo donde hay schema Create/Read.

**Severidad.** Swallow en persist/tenant: **bloqueante**. Ruff/tipos/archivo-multi-entidad: **mayor**.

**Fuentes.** `db_rely_general.mdc`, `models.mdc`, `schemas.mdc`, `repositories.mdc`; `hub/db/pyproject.toml`.

---

## S-DOCS-CONTEXT

**Intención.** El siguiente agente (y el humano) encuentra el seam en CONTEXT, no en el PR.

**Debe** actualizar, si el cambio mueve el seam, el contrato o el vocabulario:

- `CONTEXT.md` del contexto.
- `docs/EDGE_NATS_ARCHITECTURE.md` + README del servicio si rompe HTTP/NATS.
- `hub/db/SCHEMA.md` si cambia tablas.
- ADR **solo** si se decide algo que futuros reviews no deben re-sugerir.

**No debe.** Nuevo `.md` dentro de `hub/db/`. Duplicar CONTEXT-MAP en la UI. Relitigar ADR estable sin marcar “reabrir porque…”.

**Severidad.** Contrato runtime cambiado sin EDGE_NATS: **mayor**. SCHEMA.md: **mayor**.

---

## Mapa: qué puntuar

**Siempre:** tabla `G-*` con PASS / FAIL / **N/A**.

**Además, por path** (solo estos `S-*` en el informe, más los que el diff toque de verdad):

| Path tocado | `S-*` |
|---|---|
| `hub/db/**` | S-TRUTH-SOURCES, S-SCHEMA-ALEMBIC, S-TENANT-SCOPE, S-TESTS-OBS, S-DOCS-CONTEXT, S-CODE-PY |
| `hub/control-plane/**` | S-SEAM-UI-CP-EDGE, S-CP, S-NATS, S-ENTRYPOINTS, S-GRAPHIR-CATALOG, S-TESTS-OBS, S-CODE-GO |
| `agents/flow-engine/**` | S-SEAM-UI-CP-EDGE, S-EDGE-RUNTIME, S-NATS, S-ENTRYPOINTS, S-TENANT-SCOPE, S-DOCKER, S-CODE-GO, S-CODE-PY |
| `agents/capture-agent/**` | S-CAPTURE, S-SEAM-UI-CP-EDGE, S-DOCKER, S-CODE-GO |
| `agents/plc-agent/**` | S-PLC-HOTPATH, S-DOCKER, S-CODE-GO |
| `agents/detector-agent/**`, `agents/anomalib-agent/**` | S-EDGE-RUNTIME, S-NATS, S-CODE-PY |
| `hub/object-store/**` | S-OBJECT-STORE, S-TENANT-SCOPE, S-DOCKER, S-CODE-PY |
| `contracts/nats/**`, `pkg/relynats/**` | S-NATS, S-TRUTH-SOURCES, S-DOCS-CONTEXT, S-CODE-GO |
| PLC / `plc_*` | S-PLC-HOTPATH, S-CP, S-EDGE-RUNTIME, S-CODE-GO |
| Org custom / contrib / catalog | S-GRAPHIR-CATALOG, S-CP, S-EDGE-RUNTIME, S-CODE-PY |
