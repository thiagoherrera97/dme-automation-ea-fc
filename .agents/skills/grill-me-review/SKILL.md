---
name: grill-me-review
description: Aggressive review skill that stress-tests plans and code. Use when the user wants hard criticism, edge cases, failure modes, or a devil's-advocate review.
---

# Grill-me review

Use this skill when the user wants the plan challenged.

## Default workflow

1. Assume the proposed idea will fail unless proven otherwise.
2. Identify the weakest assumption first.
3. List the top failure modes.
4. Look for scope creep, fragility, and hidden dependencies.
5. Challenge whether the solution matches the real user need.
6. Recommend the smallest safer alternative if needed.

## Questions to ask

- What breaks first?
- What is hard to maintain?
- What requires manual recovery?
- What will change when the UI shifts?
- Is this the right level of automation?

## Tone

- Direct.
- Specific.
- No vague praise.
- No generic "best practices" filler.

## Output

- Top risks.
- Wrong assumptions.
- Concrete fixes or simplifications.
