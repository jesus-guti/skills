---
name: ralph-chat
description: Interactive guide that reads local issue-tracker tickets, determines dependency order, and outputs a portable prompt for the `implement` skill. Use when the user says ralph, ralph-chat, wants to know what to work on next, or needs implementation order from `.scratch/` tickets.
---

# Ralph Chat

Interactive guide that reads `.scratch/<feature-slug>/` tickets, resolves dependency order, and hands you a **portable prompt** to paste into a fresh chat with the `implement` skill.

You **plan and guide only.** Do not implement issues in this chat.

## Invocation

| Pattern | Mode |
|---------|------|
| `ralph <feature-slug>` | Analyze all tickets, output order, print prompt for the first ready ticket |
| `ralph <feature-slug> next` | Output prompt for the next ready ticket (use mid-session to advance) |
| `ralph <feature-slug> list` | Print dependency-ordered list of all AFK tickets with status |

Aliases: `/ralph-chat`, "corre ralph en …", "qué sigue de …", "orden de tickets …".

## Orchestrator rules

Before output:

1. Confirm `.scratch/<feature-slug>/PRD.md` exists; stop with the expected path if missing.
2. Read all issue files under `.scratch/<feature-slug>/issues/*.md`.
3. Read the PRD.
4. Read `CONTEXT-MAP.md` and follow it to relevant `CONTEXT.md` files.
5. Read recent commits: `git log -n 5 --format="%H%n%ad%n%B---" --date=short`.

### Determine ready tickets

A ticket is **ready** when:
- `Type: AFK` (ignore HITL)
- `Status: ready-for-agent` (or equivalent active state)
- All blockers listed in the issue are resolved (check referenced tickets' status)

### Order

Sort ready tickets by:
1. Critical bugfixes
2. Development infrastructure
3. Tracer bullets for new features
4. Polish and quick wins
5. Refactors

Respect explicit `Blocked by:` notes in issue files.

### Output format

Print a summary table of all issues (ordered, with status), then output a **portable prompt** for the first ready ticket using the template in [WORKER.md](WORKER.md).

On `ralph <slug> next`: output the prompt for the next ready ticket, skipping any the user already completed.

On `ralph <slug> list`: print only the ordered table, no prompt.

## User controls (mid-run)

- **next / siguiente** — output prompt for the next ready ticket
- **done `<issue-path>`** — mark a ticket as done (so `next` skips it)
- **list** — re-print the ordered table

## Relation to `implement` skill

Ralph Chat outputs a prompt. The user opens a **separate chat**, loads the `implement` skill, and pastes the prompt (or the ticket path) to implement that ticket.

The `implement` skill follows the same conventions (TDD, typecheck, code-review, commit, update issue file) but runs fresh for each ticket, keeping context clean.

## Relation to terminal Ralph

| | `tools/ralph` (CLI) | `ralph-chat` (this skill) |
|--|---------------------|---------------------------|
| Runtime | `@cursor/sdk` + API key | Interactive guide + portable prompts |
| Implementation | Automatic | Delegates to `implement` skill in separate chat |
| Interactive | No | Yes (order, next, done) |
| Unattended AFK | Yes | No (manual, one ticket per chat) |
