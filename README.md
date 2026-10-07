# Skills

Colección privada de Agent Skills para Cursor y otros agentes compatibles con
el formato `SKILL.md`.

El repositorio es la fuente canónica. Las instalaciones globales y locales
pueden ser enlaces simbólicos, por lo que un `git pull` actualiza todas las
skills inmediatamente.

## Primera instalación

```bash
git clone git@github.com:jesus-guti/skills.git ~/.local/share/jesus-guti-skills
~/.local/share/jesus-guti-skills/skillsctl link-global
```

Cursor descubre las skills globales desde `~/.agents/skills`. El instalador
crea un enlace por skill y conserva cualquier entrada ajena que ya exista.
Si una entrada real tiene el mismo nombre, se omite; `--force` permite
reemplazarla.

## Actualizar

```bash
~/.local/share/jesus-guti-skills/skillsctl update
```

Los enlaces apuntan al clon, así que no hace falta reinstalar después de
actualizar.

## Instalar en un proyecto

Enlace local, ideal para trabajar en una sola máquina:

```bash
skillsctl link-project /ruta/al/proyecto
skillsctl link-project /ruta/al/proyecto tdd diagnose code-review
```

Copia portable, adecuada para guardar las skills dentro del proyecto:

```bash
skillsctl copy-project /ruta/al/proyecto tdd diagnose
```

Ambos comandos instalan en `.cursor/skills`. Añade `--force` para sustituir
skills existentes con el mismo nombre.

## Incorporar cambios

Importar todas las skills globales nuevas o modificadas:

```bash
skillsctl sync-globals
```

El comando las incorpora al repo y deja las entradas globales enlazadas a la
fuente canónica.

Importar las skills propias de un proyecto, por ejemplo Rely:

```bash
skillsctl sync-project /home/jesus-siali/github/siali/rely
```

Actualizar las colecciones externas configuradas:

```bash
skillsctl sync-external
```

Actualmente sincroniza:

- [`pbakaus/impeccable`](https://github.com/pbakaus/impeccable)
- [`Leonxlnx/taste-skill`](https://github.com/Leonxlnx/taste-skill)
- [`emilkowalski/skill`](https://github.com/emilkowalski/skill)

Los commits importados quedan registrados en `SOURCES.lock`. La skill
`prototype` de Emil se instala como `emil-prototype` para no sustituir la
skill homónima que ya existía.

Después:

```bash
git add skills SOURCES.lock
git commit -m "sync skills"
git push
```

`sync-globals` ignora las skills que ya están enlazadas a este mismo repo, lo
que evita copiarse sobre sí mismo. Las skills importadas desde terceros son
snapshots privados: este repositorio no sustituye sus canales oficiales de
actualización.

## Comandos

```text
skillsctl update
skillsctl link-global [--force] [skill...]
skillsctl link-project <proyecto> [--force] [skill...]
skillsctl copy-project <proyecto> [--force] [skill...]
skillsctl sync-globals [directorio]
skillsctl sync-project <proyecto>
skillsctl sync-external
skillsctl status
```
