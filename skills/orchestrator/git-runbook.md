# Runbook git del orquestador

## Worktrees

Crear siempre desde la base acordada, con `git fetch` previo:

Issue suelta:

```bash
git worktree add -b jgutierrez/jes-NNN-<slug> ../worktrees/loadzone/jes-NNN origin/dev
```

Bundle (`bundle:<slug>` compartido por varias issues `plan:direct`):

```bash
git worktree add -b jgutierrez/bundle-<slug> ../worktrees/loadzone/bundle-<slug> origin/dev
```

Liberar manteniendo la rama:

```bash
git worktree remove ../worktrees/loadzone/jes-NNN --force
git worktree remove ../worktrees/loadzone/bundle-<slug> --force
```

Un `git checkout <rama>` falla mientras esa rama siga montada en un worktree. Liberar antes de que el humano haga `gh pr checkout`.

## PRs en stack

Cuando una PR hija tiene como base la rama de la PR padre, avisar al usuario del riesgo: **si al mergear la padre GitHub borra la rama head, las PRs hijas se cierran solas.**

Remedio:

```bash
git push origin <sha-de-la-rama-borrada>:refs/heads/<rama-base>
gh pr reopen <N>
gh pr edit <N> --base dev
```

## Adelantar trabajo bloqueado

Para avanzar en paralelo antes de que la base llegue a `dev`, mergear el tip de la rama padre dentro del worktree hijo. Al mergear el fix de un hallazgo high en la padre, propagarlo igual a cada hija del stack.

## Commits

Siempre bajo petición del usuario, con HEREDOC, sin `git add .` indiscriminado, sin `--amend` y sin force-push salvo petición explícita. Un fix de review es un commit nuevo.
