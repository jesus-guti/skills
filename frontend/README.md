# Frontend: selección y mantenimiento

Este perfil reduce las entradas de diseño a cinco, manteniendo el conocimiento especializado bajo demanda. Está pensado para interfaces de producto como Sialos; también distingue trabajo editorial y de marketing.

| Entrada | Responsabilidad |
| --- | --- |
| `frontend-workflow` | Orientar el encargo y elegir una ruta |
| `impeccable` | Diseño, UX, pulido y herramientas de diseño del proveedor |
| `frontend-review` | Revisión con evidencias; seis dominios de Jakub como referencias |
| `frontend-motion` | Movimiento con siete guías de Emil como referencias |
| `sir-jony-ive` | Consultar el segundo cerebro por decisión, sin cargarlo entero |

Las cuatro optativas son `variant`, `break`, `state-machine` y `build-design`. Se instalan por necesidad explícita. Sus políticas originales de invocación se conservan; no son parte del perfil básico.

## Usar el perfil

Desde este directorio, `python3 frontctl check` comprueba estructura, enlaces y hashes; `python3 audit/verify.py` prueba el instalador en directorios temporales; `python3 frontctl inventory` resume el inventario capturado. La instalación siempre empieza como un plan:

```sh
python3 frontctl install --project /ruta/al/proyecto --harness codex
python3 frontctl install --project /ruta/al/proyecto --harness codex --apply
python3 frontctl install --project /ruta/al/proyecto --harness claude --apply
python3 frontctl install --project /ruta/al/proyecto --harness cursor --skills variant --apply
```

Se copian árboles completos para que las referencias sigan disponibles al mover el proyecto. Las optativas incluyen su dependencia frontend-review. Una entrada idéntica se conserva; una colisión de contenido detiene toda la operación antes de escribir. No hay `--force` ni eliminación automática. No uses el `skillsctl link-global` sin nombres para instalar este perfil: ese comando instala la colección histórica completa y no lee `profile.json`.

Instalar estas cinco no reduce por sí solo las skills que ya expone tu agente. Para terminar la migración hay que revisar las instalaciones globales, los plugins y las copias locales indicadas en [la auditoría](audit/REPORT.md), y retirar o desactivar sus duplicados en una acción separada. Este paquete no ha modificado ninguna instalación activa.

En Codex puedes invocar `$frontend-workflow`, `$frontend-review`, `$frontend-motion`, `$impeccable` o `$sir-jony-ive`. En Claude Code el nombre se usa como slash command. Las rutas de instalación se derivan de la documentación de distribución de los proveedores revisados; no se ha hecho una sesión funcional con cada agente.

## Mantener la selección

`sources.lock.json` fija las revisiones consultadas; `files.lock.json` fija el contenido empaquetado. No se sincroniza a HEAD al instalar. Un cambio de fuente requiere revisar el diff, los criterios y las referencias, actualizar los hashes y repetir los escenarios de aceptación en `audit/SCENARIOS.md`. Nunca basta con regenerar el lock para dar por bueno un cambio.

Para volver a auditar en Claude Code, la skill existente `skill-stocktake` ofrece el flujo `/skill-stocktake full`. Sus rutas por defecto son `~/.claude/skills` y `.claude/skills`, y su caché vive bajo `~/.claude/skills/skill-stocktake/`; hay que ampliar el alcance para incluir `.agents`, el repositorio canónico y plugins. La auditoría de este paquete está acotada al front y se guarda aquí, sin escribir esa caché global. El comando propone Keep/Improve/Update/Retire/Merge; no decide por sí solo qué borrar.

Consulta [NOTICE.md](NOTICE.md) para licencias y modificaciones de empaquetado. Impeccable se copia como skill oficial; su motor y hooks mantienen el ciclo de distribución del proveedor.
