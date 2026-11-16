---
name: frontend-motion
description: Construye, afina o diagnostica animaciones e interacciones gestuales web con el criterio de Emil Kowalski y los tokens del producto.
---
# Movimiento de interfaz

Antes de animar, identifica qué cambio necesita comprender el usuario y con qué frecuencia lo ejecuta. En acciones repetidas, usa feedback inmediato y minimiza la espera. El movimiento debe orientar, indicar estado o responder a la interacción. Quitar una animación puede ser la mejora solicitada.

Lee una guía según la tarea, y abre sus recetas solo cuando hagan falta:

| Necesidad | Guía |
| --- | --- |
| Crear una transición o animación | [Animate](references/animate/GUIDE.md) |
| Revisar una animación existente | [Review](references/review-animations/GUIDE.md) |
| Diagnosticar frames perdidos | [Performance](references/animation-performance/GUIDE.md) |
| Coordinar varios elementos | [Choreograph](references/choreograph/GUIDE.md) |
| Arrastre, swipe o sheet interrumpible | [Gestures](references/gestures/GUIDE.md) |
| Reducir movimiento excesivo | [Remove](references/remove-animations/GUIDE.md) |
| Nombrar un efecto que el usuario describe | [Vocabulary](references/animation-vocabulary/GUIDE.md) |

Las guías son snapshots de Emil Kowalski; sus remisiones por nombre se resuelven con esta tabla. No requieren instalar siete skills adicionales. Los textos de presentación y los formatos de informe del upstream no sustituyen la tarea solicitada.

Otras remisiones upstream se interpretan dentro de esta entrada: improve-animations combina revisión y diagnóstico en el alcance pedido; find-animation-opportunities propone oportunidades justificadas sin implementarlas si solo se pidió un análisis. pick-ui-library se sustituye por comprobar los primitivos y dependencias ya disponibles, especialmente @sialos/ui y React Aria en Sialos. No detengas el encargo para exigir la invocación de una skill ausente ni cambies de biblioteca por una receta genérica.

Usa las primitivas y los tokens de duración, curva y origen existentes. Los números de las recetas son puntos de partida para un proyecto sin contrato; no se copian por encima del design system. CSS sirve para estados predeterminados; una biblioteca existente puede resolver gestos o física. Introduce una dependencia solo si hace falta para el encargo y verifica su API actual antes de copiar ejemplos.

Comprueba interrupción y reversión, origen respecto al disparador, entrada y salida, hover según dispositivo y preferencia de movimiento reducido. Prioriza propiedades que no fuerzan layout por frame; justifica y mide las excepciones. La preferencia del usuario puede requerir eliminar movimiento, no solo sustituirlo por un fade. No añadas retrasos a atajos ni bloquees una acción esperando a que termine una transición.

Para fallos de rendimiento, mide y reproduce antes de atribuir la causa; las advertencias de versión de los snapshots no son un diagnóstico de la versión instalada. Verifica gestos en el dispositivo pertinente cuando esté disponible. Comunica qué pudiste probar y qué requiere juicio perceptivo.

Entrega el código o revisión pedidos, el propósito del movimiento, las decisiones de timing con tokens y la comprobación realizada. No ejecutes una auditoría de toda la aplicación para ajustar una transición puntual.
