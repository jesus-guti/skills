# Auditoría del perfil frontend — 2026-11-11

## Decisión

Conservar Impeccable como proveedor general, convertir el conocimiento de Jakub y Emil en referencias de dos entradas especializadas y hacer portable el acceso a Sir Jony Ive. El perfil ofrece cinco entradas principales y cuatro optativas. La colección histórica permanece disponible; este trabajo no ha desinstalado ni borrado skills.

Las cinco entradas son una selección editorial nueva, pendiente de evaluación funcional en tareas reales. Los checks del paquete prueban estructura, integridad y comportamiento del instalador; no prueban que un agente diseñe mejor.

## Fuentes y alcance

Se consultaron los repos completos de [Jakub](https://github.com/jakubkrehel/skills), [Emil](https://github.com/emilkowalski/skills), [Impeccable](https://github.com/pbakaus/impeccable) y [Sir Jony Ive](https://github.com/jesus-guti/sir_jony_ive) mediante GitHub autenticado, con revisiones fijadas en `../sources.lock.json`. También se inspeccionaron el clon local de [skills](https://github.com/jesus-guti/skills), su instalador y las instalaciones presentes. Se aplicó el checklist de `skill-stocktake`: solapamiento, utilidad concreta, alcance, actualidad y uso. Los conjuntos de Jakub y Emil tienen veredictos individuales en JSON; el resto se revisó según su relevancia para front. No es una auditoría semántica de las 393 skills canónicas.

| Ruta inspeccionada | Entradas inmediatas con SKILL.md |
| --- | ---: |
| Repo canónico `jesus-guti-skills/skills` | 393 |
| Global `~/.agents/skills` | 421 |
| Global `~/.claude/skills` | 12 |
| Sialos `.agents/skills` | 33 |
| Sialos `.claude/skills` | 15 |
| Sialos `agent/skills` | 25 |

El inventario guarda rutas resueltas, hashes y mtimes. No suma esos números como skills únicas: hay enlaces y copias, y no incluye skills anidadas ni plugins. Diez de las 33 entradas locales coinciden byte a byte con su homónima global. Las quince de `.claude/skills` son enlaces a `.agents/skills`; no son quince copias físicas adicionales. Uso en siete y treinta días: desconocido. No se ha usado mtime como sustituto de frecuencia.

En Codex aparece además Impeccable como plugin, mientras existe una entrada global; sus versiones visibles son 4.3.1 y 4.5.0 respectivamente. Hay también dos proveedores visibles de la skill Impeccable. Mantener ambos puede cargar criterios o comandos de revisiones distintas; escoger una única distribución activa por agente es parte de la migración.

## Encaje con Sialos

El workspace actual tiene como origin `Sialitech/sialos-app`. Se contrastó el checkout local `ad18b9477634ea135f63ad7f605eb8f8d2367f8f` con cinco contratos de main remoto `210b1f6e30ca5f5422f2e635c18254fc5323dfdc`, descargados sin mover ramas ni modificar el checkout. Hay cambios locales de otros trabajos; no se han tocado.

Los contratos de `apps/web`, `packages/ui` y la identidad describen una aplicación de operación con DS propio, tokens y pictogramas. Los widgets con comportamiento se apoyan en React Aria; los comandos de comprobación vienen del Makefile. Las fichas tienen revisión humana para pasar a stable. `DESIGN.md` se genera y no debe sobrescribirse desde una skill de extracción o documentación.

La selección debe conservar esos contratos: evitar nuevas escalas visuales en componentes, cambios de fuente por preferencia genérica, reemplazar primitivos o añadir animaciones para que la pantalla parezca más viva. La identidad de Sialos no se impone a otros proyectos que usen este perfil.

`agent/skills` alimenta el perfil del agente del producto, mientras `.agents/skills` sirve al agente que desarrolla el repositorio. Sus adaptaciones y destinos difieren. No se debe propagar automáticamente una limpieza del entorno de desarrollo al agente de Build/Ask ni importar indiscriminadamente toda una colección en ambos.

## Qué conservar y qué absorber

| Fuente | Decisión del perfil | Aportación concreta |
| --- | --- | --- |
| Impeccable | Keep, distribución oficial intacta | Diseño y pulido general, comandos especializados y separación entre superficies de operación y comunicación |
| Jakub better-interface + seis dominios | Merge into frontend-review | Evidencia, cobertura, severidad por impacto, causas compartidas y guías verificables |
| Jakub interface-review | Merge into frontend-review | Alcance de diff y clasificación Introducido / Regresión / Preexistente |
| Emil animate, review, performance, choreograph, gestures, remove, vocabulary | Merge into frontend-motion | Propósito y frecuencia, interrupción, origen, diagnóstico y movimiento reducido |
| Emil emil-design-eng | Referencia de origen; fuera de entradas core | Es útil pero su catálogo extenso repite las guías concretas; no necesita activarse en cualquier tarea UI |
| Sir Jony Ive | Improve | Mantener lectura por capas; resolver ruta por usuario, entorno o checkout del producto y declarar recurso ausente |
| Jakub variant, break, state-machine, build-design | Keep, optativas | Exploración visual, estrés, estados alcanzables e implementación de diseño explícito |
| Jakub afk | Retire del perfil | El barrido de horas, ideas y commits excede la selección de herramientas para una tarea de front |
| Jakub explain-interface, teardown | Fuera del core | Estudiar una interfaz y hacer ilustración técnica son encargos puntuales, no requisitos del front de Sialos |
| Emil prototype / emil-prototype | Elegir variant como optativa | Dos flujos de variantes compiten; conservar uno en el perfil reduce ambigüedad |
| Emil animate-expo, write-swift | Fuera de este perfil web | Son especialidades nativas, disponibles para un futuro perfil específico |
| Emil mobile-native, apple-design, ask-sonner, pick-ui-library | Consulta puntual, fuera del core | Dispositivo, estética o biblioteca particulares; Sialos ya decide primitivos y stack |
| Emil improve-animations, find-animation-opportunities | Absorber selección de intención en frontend-motion | El encargo decide auditar o proponer; no hace falta exponer otro disparador por cada verbo |

La síntesis conserva las guías como referencias y sus licencias. No modifica el Impeccable original. En las optativas de Jakub, las remisiones a las antiguas skills better-* e interface-review se adaptan a frontend-review para que no exijan reinstalar todo el conjunto. Las referencias internas con rutas relativas se mantienen con sus árboles de recetas.

## Candidatos de la colección histórica

Estas decisiones afectan al perfil de front; no afirman que las skills carezcan de valor para cualquier otro trabajo.

| Skill o grupo | Veredicto propuesto | Evidencia y sustitución |
| --- | --- | --- |
| gpt-tasteskill | Retire | Exige simular una ejecución Python, AIDA en toda página, GSAP y UI siempre animada. Impeccable sigue el brief y frontend-motion decide si hace falta movimiento |
| taste-skill-v1 | Retire del perfil | Incluye motor Bento con loops perpetuos, prohibiciones de fuentes y dependencias impuestas. El propio texto la conserva para compatibilidad; no es el criterio por defecto de Sialos |
| taste-skill | Fuera del perfil de producto | Su alcance declarado son landings, portfolios y rediseños, excluyendo dashboards. Puede tener perfil de marketing si se solicita |
| redesign-skill | Retire del perfil | Recomienda cambios de fuente y transiciones de 200–300 ms en todos los elementos interactivos; compite con identidad y frecuencia de uso. Impeccable + frontend-motion cubren refinamiento contextual |
| frontend-design-direction | Merge into frontend-workflow | El brief y elección de dirección se solapan con Impeccable. Mantener una entrada de orientación, no un tercer director visual |
| invisible-design | Referencia de criterio | Buena orientación a tarea, carga cognitiva y claridad; se solapa con el cerebro y revisión. No necesita otro disparador universal |
| design-system | Consulta para trabajo explícito de DS | Genera tokens y DESIGN.md desde código; en Sialos DESIGN.md es generado por otro contrato. No ejecutar como efecto de pulir una pantalla |
| design-system-rules, content-design | Fuera del perfil genérico | Nombran Rely y rutas hub/ui. Mantenerlas ligadas a ese producto; Sialos usa sus contratos y frontend-review |
| accessibility, frontend-a11y | Consolidar revisión bajo frontend-review | Hay varias entradas para el mismo dominio. Las recetas deben comprobarse según el primitivo real y docs actuales; no reimplementar teclado ya resuelto por el DS |
| motion-foundations, motion-patterns, motion-advanced | Fuera del core, referencia técnica eventual | Montan otra escala y catálogo de Motion además de Emil. No instalar una segunda política de tokens por añadir una transición; exactitud de sus APIs no certificada |
| image-to-code-skill, imagegen-frontend-web/mobile | Opcionales para un encargo visual explícito | Exigir imagen previa en tareas de front añade otra fase y herramientas que un ajuste en Sialos no necesita |
| ui-demo | Fuera del core | Grabar una demo es un entregable diferente; cargarla cuando se solicite |
| Swift, vídeo, marca, slides y otros frameworks | Fuera de alcance | No se declaran malas ni obsoletas. Mantener perfiles separados según tarea |

## Migración pendiente de instalaciones activas

1. Elegir una única instalación activa de Impeccable por agente; verificar si se desean sus hooks y herramientas oficiales antes de sustituir una distribución instalada por la copia manual de este paquete.
2. Comparar las 33 entradas locales y las globales con los veredictos. Los alias `.claude` y las copias `agent/skills` requieren tratamiento distinto.
3. Preparar un diff de retirada con cada ruta, origen, alternativa y dependencias. Las guías better-* pasan a referencias; animate y las revisiones de motion pasan a frontend-motion; el acceso al cerebro se mantiene portable.
4. Retirar o archivar solo las entradas aprobadas. No ejecutar `skillsctl sync-globals`, `sync-external` ni una instalación global indiscriminada como parte de esa retirada: volverían a importar fuentes o actualizar contenido fuera de la selección.
5. Instalar el perfil donde se haya resuelto cada colisión y probar los escenarios. Comprobar también el catálogo que el agente muestra al iniciar una sesión nueva.

`skill-stocktake` exige confirmación explícita para archivar o borrar. Esta auditoría entrega decisiones y un perfil revisable; no ejecuta esa fase. La restricción procede de su SKILL.md, sección Notes: “Archive / delete operations always require explicit user confirmation”.

## Límites de la revisión

No se ejecutaron hooks, instalación del motor de Impeccable, sesiones de diseño con cada harness ni benchmarks de calidad visual. No hay métricas de uso para decidir por frecuencia. No se declara una API obsoleta sin verificarla; las advertencias técnicas se verifican contra documentación actual al implementar. No se han ejecutado tests del producto porque el cambio reside en la colección de skills, no en Sialos.
