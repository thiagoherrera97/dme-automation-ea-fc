# FUTGenie / EA FC functional requirements

## Scope

The project should support analysis and automation planning for the EA FC web app using the FUTGenie extension as a reference implementation.

## Explicit constraints from the user

- Do not perform transfers.
- Do not sell players.
- Do not complete or submit any DME/SBC unless the user explicitly authorizes a specific action.
- Exploration is allowed.

## FUTGenie areas already observed

### Main areas

- `SBC Solver`
- `Club Insights`
- `Locked Players`
- `Settings`
- `Patch Notes`
- `Upgrade your plan`

### SBC solver controls

- `Auto Complete`
- `Exchange Players`
- `Use Squad Builder`
- `Clear Squad`
- `More FUTGenie Options`
- `Work Area`
- `Submit`

### SBC list controls

- `Quick complete`
- `Search SBCs...`
- category tabs:
  - `All`
  - `Favourites`
  - `Players`
  - `Upgrades`
  - `Challenges`
  - `Icons`
  - `Foundations`
  - `Swaps`

## Observed solver information

- Challenge requirements are shown before interaction.
- Challenge reward is shown in the side panel.
- Chemistry, rating, and total squad price are exposed in the solver view.
- Repeatability and expiry time are shown on challenge cards.

## Functional requirements for our project

1. Read the current challenge before any automation step.
2. Preserve the club state and never consume assets without explicit approval.
3. Support exploration mode that only inspects UI state.
4. Separate safe inspection from destructive actions.
5. Record the exact screen, challenge, and controls observed.
6. Be usable from iPhone-first workflows.

## Suggested next implementation layer

- UI state parser
- challenge metadata reader
- action planner
- approval gate for any destructive step
- audit log of all explored screens
