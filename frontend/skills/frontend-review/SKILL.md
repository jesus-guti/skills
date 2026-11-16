---
name: frontend-review
description: Revisa una pantalla, flujo o diff de frontend con evidencias de accesibilidad, estructura, texto y consistencia visual.
---
# Revisión de interfaz

Resuelve el alcance desde la petición: pantalla, flujo, cambios sin commit o rango de commits. Si no puedes determinar la base de un diff, acláralo antes de atribuir regresiones. Lee el contrato y el design system existentes; una preferencia externa sobre fuente, densidad o radio no demuestra un defecto.

En un diff, inspecciona también líneas eliminadas y consumidores afectados aunque sus archivos no cambien. Un token, un componente compartido o una cadena eliminada puede causar una regresión en otra superficie; identifica ese alcance y comprueba los usos pertinentes antes de aprobarlo.

Consulta solo los dominios que afecta el alcance. Para una revisión integral, cubre los seis:

| Dominio | Guía local |
| --- | --- |
| Nombres accesibles, teclado, foco, objetivos y estados anunciados | [Accesibilidad](references/better-accessibility/GUIDE.md) |
| Agrupación, orden, crecimiento, recorte y responsive | [Layout](references/better-layout/GUIDE.md) |
| Vocabulario, acciones, errores, vacíos e internacionalización | [Texto](references/better-writing/GUIDE.md) |
| Jerarquía, medidas, números, truncado y lectura | [Tipografía](references/better-typography/GUIDE.md) |
| Roles semánticos, estados y contraste renderizado | [Color](references/better-colors/GUIDE.md) |
| Alineación óptica, capas, iconos y detalle | [Acabado](references/better-ui/GUIDE.md) |

Las guías son snapshots de Jakub Krehel, conservados con licencia y procedencia en el paquete. Sus referencias a skills hermanas se resuelven con esta tabla. Sus formatos de informe y números de pulido son recomendaciones; el formato de esta entrada y los tokens del proyecto gobiernan esta revisión. El movimiento detallado lo lleva `frontend-motion`; no combines automáticamente sus valores con los de `better-ui`.

Contrasta cualquier supuesto incumplimiento con el criterio aplicable y sus excepciones. Un mapa o tabla que necesita dos dimensiones no se evalúa como un párrafo de lectura. Distingue caja visible y zona pulsable, y verifica el hit-target del proyecto en el navegador. No declares incumplimiento por un umbral orientativo de fuente, espaciado o duración; cita el fallo observable. Tampoco des por conforme una implementación solo porque respeta sus tokens.

En Sialos, el contrato documenta el solapamiento de 1 px entre zonas de controles adyacentes: evalúa ese caso con sus comprobaciones, sin aplicar el veto absoluto a solapamientos de la guía. Verifica teclado, foco y overlays por comportamiento observable: React Aria puede delegarlos sin un onKeyDown local en cada nodo. No añadas una segunda implementación manual solo para satisfacer una detección textual de la referencia.

Prueba la interfaz renderizada cuando el hallazgo dependa de foco, responsive, recorte o percepción. El código permite localizar la causa; no prueba por sí solo cómo se ve. Usa los checks existentes del proyecto. Una herramienta que no pudo ejecutarse se declara pendiente, no aprobada.

Prioriza por impacto: bloqueo de tarea o pérdida de información, degradación de comprensión o eficiencia, y por último acabado. Agrupa síntomas causados por el mismo token o componente. Propón primero reutilizar o corregir lo existente.

Informa alcance y cobertura, luego una tabla `Severidad | Ubicación | Evidencia e impacto | Corrección`. En un diff, distingue Introducido, Regresión y Preexistente. Termina con checks ejecutados, áreas no verificadas y si queda algún bloqueo. Si no encuentras defectos, dilo sin fabricar hallazgos para llenar el informe.
