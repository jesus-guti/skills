# Matriz de autonomía

Cada decisión que surge al planificar una issue recibe **uno** de tres niveles. Se clasifica por decisión, nunca por issue entera: una issue normal mezcla los tres.

| Nivel | El agente | El usuario |
|---|---|---|
| `auto` | Decide y sigue | Ve una línea en el informe |
| `assume` | Decide, aplica de forma aislada y reversible | Ve una línea marcada, con cómo revertirla |
| `hitl` | Se detiene | Recibe la pregunta con recomendación |

## Criterios de escalada

Evaluar en orden. La primera que se cumple fija el nivel.

### Escala a `hitl` si se cumple alguna

- **Contrato compartido**: esquema Alembic, contratos NATS en `contracts/nats`, API entre features, o forma de datos que otro servicio consume.
- **Design system transversal**: tokens en `styles/design-tokens.css` o primitives de `components/ui` de forma que cambia más de una pantalla.
- **Irreversible o costoso de revertir**: migración de datos, borrado, renombrado masivo, cambio de dependencia mayor.
- **Externo o de seguridad**: credenciales, permisos, gasto, exposición pública.
- **Contradice una decisión ya registrada** en un `map.md` o en un ADR.
- **Producto, no implementación**: el resultado cambia lo que el usuario final puede hacer, no cómo está construido.

### Escala a `assume` si se cumple alguna

- Radio de impacto contenido en una feature o una pantalla.
- Hay dos opciones razonables y ninguna es claramente mejor, pero elegir mal se corrige con un revert limpio.
- Se apoya en una convención del repo que existe pero no es unánime.

### Todo lo demás es `auto`

Nombres internos, estructura de ficheros dentro de una feature, orden de implementación, qué test escribir, aplicar una convención ya documentada en `.cursor/rules/` o en las skills, o repetir un patrón ya presente en el código adyacente.

## Tope

**Máximo 3 `hitl` por issue.** Si salen más, la issue está mal definida: no preguntar, devolverla marcada y proponer cómo partirla.

## Antes de clasificar

Buscar precedente. Si una decisión equivalente ya está resuelta en un `map.md` del mismo lote, en un ADR o en el código adyacente, no es una decisión: es aplicar lo que ya existe, y baja a `auto` aunque el tema parezca grande.

## Registro

Toda decisión, sea del nivel que sea, se escribe en `Decisions so far` del `map.md` con su nivel. Las `assume` añaden una línea de cómo revertirse. Una decisión sin registrar no existe: el implementador no puede saber si fue elegida o inventada.
