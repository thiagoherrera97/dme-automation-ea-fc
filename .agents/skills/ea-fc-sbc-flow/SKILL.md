---
name: ea-fc-sbc-flow
description: EA FC SBC workflow guidance for the specific automation project. Use when navigating SBC lists, reading requirements, building squads, and validating completion states.
---

# EA FC SBC flow

Use this skill when the task is about SBCs, Auto Complete, Squad Builder, or repeating DME-like flows in the EA FC web app.

## Default workflow

1. Open the EA FC web app and confirm the user is already authenticated.
2. Navigate to SBC and identify the exact challenge.
3. Read the challenge requirements before taking any action.
4. Inspect the active squad, solver options, and available filters.
5. Prefer deterministic steps over blind clicking.
6. Verify the final squad state before confirming completion.
7. Capture a screenshot or note the exact state reached.

## Important rules

- Stop at login, 2FA, expired session, or any manual confirmation step.
- Do not assume the same SBC names, prices, or requirements stay stable.
- Treat the UI as dynamic and check the current screen before every critical action.
- When a challenge has multiple solution paths, document the chosen path.

## Good use cases

- Test the SBC list and challenge detail screens.
- Validate the Auto Complete flow.
- Check that requirements and squad score summaries are readable on mobile.
- Confirm that repeatable flows do not drift after a refresh or navigation change.

## Output

- Exact SBC touched.
- Current step reached.
- Any blockers or manual steps required.
- Screenshot evidence when useful.
