---
name: design-an-interface
description: Generate multiple radically different module/API interface designs using parallel sub-agents. Use when user wants to design an API, explore module shapes, compare caller surfaces, or mentions "design it twice". Not for user-facing UI screens — use prototype (UI branch) for those.
---

# Design an Interface

Based on "Design It Twice" from "A Philosophy of Software Design": your first idea is unlikely to be the best. Generate multiple radically different designs, then compare.

## Scope gate

This skill designs **module/API interfaces** (types, methods, what callers see) — **not** user-facing UI screens, layouts, or product copy.

If the user means a **pantalla / screen / layout / UX**, stop and pick by whether the screen exists
yet: a new screen goes to the **prototype** skill ([UI.md](../prototype/UI.md)); an existing screen that
feels off goes to [invisible-design](../invisible-design/SKILL.md) for audit and refactor. Keep
on-screen copy lean: labels and data, no internal-logic prose on the page.

## Workflow

### 1. Gather Requirements

Before designing, understand:

- [ ] What problem does this module solve?
- [ ] Who are the callers? (other modules, external users, tests)
- [ ] What are the key operations?
- [ ] Any constraints? (performance, compatibility, existing patterns)
- [ ] What should be hidden inside vs exposed?

Ask: "What does this module need to do? Who will use it?"

### 2. Generate Designs (Parallel Sub-Agents)

Spawn 3+ sub-agents simultaneously using Task tool. Each must produce a **radically different** approach.

```
Prompt template for each sub-agent:

Design an interface for: [module description]

Requirements: [gathered requirements]

Constraints for this design: [assign a different constraint to each agent]
- Agent 1: "Minimize method count - aim for 1-3 methods max"
- Agent 2: "Maximize flexibility - support many use cases"
- Agent 3: "Optimize for the most common case"
- Agent 4: "Take inspiration from [specific paradigm/library]"

Output format:
1. Interface signature (types/methods)
2. Usage example (how caller uses it)
3. What this design hides internally
4. Trade-offs of this approach
```

### 3. Present Designs

Show each design with:

1. **Interface signature** - types, methods, params
2. **Usage examples** - how callers actually use it in practice
3. **What it hides** - complexity kept internal

Present designs sequentially so user can absorb each approach before comparison.

### 4. Compare Designs

After showing all designs, compare them on:

- **Interface simplicity**: fewer methods, simpler params
- **General-purpose vs specialized**: flexibility vs focus
- **Implementation efficiency**: does shape allow efficient internals?
- **Depth**: small interface hiding significant complexity (good) vs large interface with thin implementation (bad)
- **Ease of correct use** vs **ease of misuse**

Discuss trade-offs in prose, not tables. Highlight where designs diverge most.

### 5. Synthesize

Often the best design combines insights from multiple options. Ask:

- "Which design best fits your primary use case?"
- "Any elements from other designs worth incorporating?"

## Evaluation Criteria

From "A Philosophy of Software Design":

**Interface simplicity**: Fewer methods, simpler params = easier to learn and use correctly.

**General-purpose**: Can handle future use cases without changes. But beware over-generalization.

**Implementation efficiency**: Does interface shape allow efficient implementation? Or force awkward internals?

**Depth**: Small interface hiding significant complexity = deep module (good). Large interface with thin implementation = shallow module (avoid).

## Anti-Patterns

- Don't let sub-agents produce similar designs - enforce radical difference
- Don't skip comparison - the value is in contrast
- Don't implement - this is purely about interface shape
- Don't evaluate based on implementation effort
- Don't treat this as a UI/mock skill — redirect screen work to prototype (UI)
- Don't leak internal module mechanics into the *public* signature or usage examples; the point of depth is hiding complexity behind a small surface
