---
name: architecture-and-planning
description: Architecture and implementation planning for the EA FC automation project. Use when choosing approaches, defining components, sequencing work, or reviewing tradeoffs before coding.
---

# Architecture and planning

Use this skill when deciding how the project should be structured.

## Default workflow

1. Restate the user goal in one sentence.
2. Identify the constraints that matter most.
3. Propose the simplest architecture that can work.
4. Split the system into clear components.
5. Call out risks, dependencies, and unknowns.
6. Recommend the next concrete implementation step.

## What to optimize for

- iPhone access first.
- Stable browser automation.
- Clear separation between UI, automation, and persistence.
- Easy debugging.
- Minimal moving parts.

## What to avoid

- Overengineering.
- Native-only solutions when mobile web is enough.
- Hidden assumptions about login or 2FA.
- Large refactors before the first working flow exists.

## Output

- Recommended architecture.
- Short rationale.
- Risks and tradeoffs.
- Next step.
