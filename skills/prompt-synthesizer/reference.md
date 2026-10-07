# Prompt Synthesizer Reference

## Goal

Turn the latest request plus the current conversation into a prompt that is specific, actionable, and aligned with the user's real objective.

## Core method

### 1. Build a silent brief

Before asking questions, infer:

- Problem to solve
- User or operator outcome
- Scope boundaries
- Inputs already available
- Desired artifact
- Quality expectations
- Missing decisions

Keep this internal unless the user asks for the reasoning.

### 2. Use product-design framing

Check whether the conversation reveals:

- Primary user or actor
- Job to be done
- Main workflow or touchpoint
- Failure modes or pain points
- Trade-offs
- Definition of success

If these are weak or missing, ask about them.

### 3. Use prompt-engineering framing

Make sure the final prompt is explicit about:

- Role: who the target agent should act as
- Objective: what success looks like
- Context: what source material matters
- Constraints: hard rules, exclusions, preferences
- Deliverables: exact output format
- Quality bar: what "good" looks like

## Clarifying-question heuristics

Ask the smallest useful set of questions. Prioritize these gaps:

1. Wrong target: the agent or audience is unclear.
2. Wrong outcome: the user wants a plan, code, copy, review, or strategy but has not said which.
3. Missing constraints: deadlines, stack, permissions, scope limits, style, or format are absent.
4. Missing quality bar: no acceptance criteria, no definition of done, or no risk tolerance.

Prefer questions like:

- "Should the prompt optimize for planning or implementation?"
- "Is the target a coding agent, a general LLM, or a design assistant?"
- "Should the output be concise or exhaustive?"
- "What constraints are non-negotiable?"

## Prompt assembly checklist

- Use the user's terminology where possible.
- Normalize contradictions instead of copying them blindly.
- Convert vague wants into explicit instructions.
- Turn implied constraints into written constraints.
- Add assumptions when the user asked to skip questions.
- Remove filler and duplicate context.
- Keep the prompt self-contained.

## Output policy

Default response after clarification:

- Return only the final prompt.

If the user explicitly asks for more, you may also include:

- Short synthesis
- Assumptions
- Alternate prompt variants

## Failure handling

If the conversation is too ambiguous:

1. Say what is missing in one sentence.
2. Ask the minimum number of questions needed.
3. Do not generate a low-confidence prompt just to fill space.
