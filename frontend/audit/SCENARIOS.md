# Escenarios para revisar el comportamiento del perfil

Estos son criterios de aceptación, no ejecuciones de agentes ya realizadas.

| Petición | Ruta esperada | Resultado que permite evaluar |
| --- | --- | --- |
| Ajusta el espaciado de este menú en Sialos | Contrato local; Impeccable si aporta al ajuste | Conserva tokens, API e identidad; no crea una paleta ni reemplaza iconos |
| Revisa los cambios sin commit del front | frontend-review | Resuelve diff, separa regresiones y preexistencias, cita evidencia |
| El popover se siente lento | frontend-motion → animate o review | Revisa propósito, token, origen e interrupción; sin auditoría de todo el repo |
| El arrastre pierde frames | frontend-motion → performance y gestures | Reproduce y mide; no atribuye un bug a una versión sin comprobarla |
| Dame variantes de esta pantalla | variant optativa si está instalada | Variantes comparables y elección del usuario; no se inicia por un ajuste menor |
| Qué patrón debe tener este selector | sir-jony-ive | Lee mapa y notas pertinentes; respeta primitivo existente |
| Revisa estados largos, vacíos y sin permisos | frontend-review; break optativa a petición | Evidencias de render y cobertura declarada |
| Arregla esta consulta SQL | Ninguna entrada frontend | No carga guías de diseño |
| Crea una landing para otro producto | frontend-workflow → impeccable | Sigue el brief de ese producto; no impone densidad ni identidad de Sialos |
| Funciona en otra máquina sin el cerebro clonado | sir-jony-ive | Declara el recurso ausente y continúa con el contrato local |

Una evaluación funcional futura debe guardar trazas de rutas y cargas de referencias, cambios producidos y juicio humano del resultado visual. Los checks de estructura y de instalación no miden calidad de diseño.
