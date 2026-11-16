---
name: frontend-workflow
description: Selecciona el criterio y la herramienta para construir o mejorar una interfaz web cuando hay varias skills de diseño disponibles.
---
# Trabajo de frontend

Empieza por la tarea del usuario, la superficie y su contrato local. Identifica si se opera una herramienta, se lee contenido o se presenta un producto. Conserva las decisiones de identidad y las dependencias existentes salvo que el encargo pida cambiarlas.

Elige una ruta principal; carga otra especialidad solo si el trabajo la necesita:

| Trabajo | Ruta |
| --- | --- |
| Diseñar una pantalla, planificar UX, pulir o corregir copy | `impeccable`, con el comando pertinente de su tabla |
| Revisar una pantalla o un cambio y producir hallazgos verificables | `frontend-review` |
| Crear, afinar, diagnosticar o simplificar movimiento | `frontend-motion` |
| Resolver un patrón, token o decisión de diseño que necesita fundamento | `sir-jony-ive` |

Estas rutas nombran skills del mismo perfil instalado. Si falta una, indica cuál y continúa con el contrato y las herramientas disponibles; no simules haberla consultado. Una tarea pequeña no necesita una ceremonia de diseño ni una auditoría completa.

En Sialos, sigue `CONTEXT-MAP.md` y el `CONTEXT.md` de la carpeta afectada. Para el design system, lee el contrato de `packages/ui`; para la aplicación, el de `apps/web`. El proyecto decide tokens, componentes, idioma, densidad, pruebas y aprobación de fichas. Los ejemplos de una colección externa no crean un segundo sistema de tokens ni sustituyen una revisión humana exigida por el producto.

Si la implementación depende de una API, consulta documentación actual de la versión instalada (Context7 cuando esté disponible). Las guías de diseño no verifican firmas, versiones ni compatibilidad de bibliotecas.

Entrega el cambio solicitado, los checks pertinentes y cualquier límite de verificación. Distingue una decisión de gusto de un defecto observable.
