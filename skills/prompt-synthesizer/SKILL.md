---
name: prompt-synthesizer
description: Synthesizes the current user prompt and conversation into a clearer request, asks targeted clarifying questions, and returns a polished prompt optimized for Cursor-style coding agents with product-design and prompt-engineering framing. Use when the user wants to sharpen a vague request, turn a discussion into an actionable agent prompt, or asks for better prompt wording from existing chat context.
disable-model-invocation: true
---

# Prompt Synthesizer

Use this skill when the user wants a stronger prompt built from the latest request plus the current conversation.

## Quick start

1. Read the latest user request and the relevant conversation context.
2. Infer the real goal, constraints, target output, and missing decisions.
3. Ask clarifying questions before drafting the final prompt.
4. After the answers arrive, return only the final prompt unless the user asks for analysis too.

## Workflow

### 1. Extract the working brief

Build a private synthesis from:

- User goal
- Business or product context
- Target system, artifact, or workflow
- Constraints and non-goals
- Success criteria
- Unknowns blocking a strong prompt

Do not dump this synthesis by default. Use it to improve the prompt.

### 2. Work through two lenses

- Product designer: clarify the user outcome, actors, flows, trade-offs, risks, and success criteria.
- Prompt engineer: remove ambiguity and specify role, context, inputs, deliverables, boundaries, and quality bar.

### 3. Clarify first

Always ask follow-up questions before writing the final prompt.

- Ask the smallest set of questions that materially improves the prompt.
- Prefer concrete either-or or multiple-choice questions when possible.
- Do not ask again for information already present in the conversation.
- If the user explicitly says to skip questions, draft with explicit assumptions.

### 4. Write the final prompt

Return one polished prompt in English for a Cursor or coding agent.

The prompt should usually include:

- Role
- Goal
- Relevant context distilled from the conversation
- Constraints
- Deliverables
- Success criteria

### 5. Output rules

- Default output is the final prompt only.
- Do not include hidden reasoning or meta commentary.
- Keep the prompt concrete and execution-ready.
- If assumptions remain, state them explicitly inside the prompt.

## Prompt template

Use this structure when it helps:

```md
You are ...

Goal:
...

Context:
- ...

Constraints:
- ...

Deliverables:
- ...

Quality bar:
- ...
```

Adapt freely when another structure fits better.

## Additional resources

- For the deeper workflow and heuristics, see [reference.md](reference.md).
- For example transformations, see [examples.md](examples.md).
