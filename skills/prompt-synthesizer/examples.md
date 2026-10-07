# Prompt Synthesizer Examples

## Example 1: Vague feature request

### User input

"I want to improve our onboarding. Use what we already discussed and write a better prompt."

### Good clarifying questions

- "Should this prompt target product strategy, UX copy, or implementation?"
- "Do you want an output for a coding agent or a product-design assistant?"
- "What metric defines improvement: activation, completion time, or fewer support tickets?"

### Example final prompt

```md
You are a senior product-focused coding agent.

Goal:
Design and propose implementation-ready improvements to the onboarding flow.

Context:
- We want to improve onboarding based on the prior conversation context.
- Focus on the current flow's biggest friction points and likely drop-off moments.

Constraints:
- Stay within the existing product scope unless an extension is clearly justified.
- Prefer high-leverage changes over broad redesigns.
- Use explicit assumptions where the conversation leaves gaps.

Deliverables:
- A concise diagnosis of the top onboarding issues.
- A prioritized list of improvements.
- An implementation approach suitable for our codebase.
- Risks, trade-offs, and success metrics.

Quality bar:
- Recommendations should be specific, feasible, and tied to user outcomes.
- Avoid generic UX advice.
```

## Example 2: Messy implementation request

### User input

"Take everything we said about stations, task overlays, and operator confusion and make a proper prompt."

### Good clarifying questions

- "Should the prompt ask for a bug fix, a UX redesign, or a code review?"
- "Do you want the result optimized for Cursor to edit code directly?"
- "Should the output include tests and acceptance criteria?"

### Example final prompt

```md
You are a senior TypeScript and Next.js coding agent working in an existing product codebase.

Goal:
Improve the station preview and task-overlay experience to reduce operator confusion.

Context:
- Use the prior conversation as source context.
- The affected area involves station preview behavior, task overlays, and related operator controls.
- The current issue appears to be UX clarity rather than a purely visual polish problem.

Constraints:
- Preserve existing behavior unless the change directly addresses the identified confusion.
- Favor small, high-confidence changes over broad refactors.
- Keep the solution aligned with the current architecture and design system.

Deliverables:
- A short diagnosis of the likely UX failure.
- A concrete implementation plan.
- The code changes needed.
- Any focused tests or validation steps required.

Quality bar:
- The result should be actionable, minimal, and easy to review.
- Explain trade-offs only where they materially affect the solution.
```
