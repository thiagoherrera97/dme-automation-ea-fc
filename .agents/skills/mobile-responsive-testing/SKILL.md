---
name: mobile-responsive-testing
description: Mobile-first testing for iPhone-sized screens, Safari behavior, and responsive layouts. Use when the product must work well on phone-sized viewports or when validating PWA/mobile UX.
---

# Mobile responsive testing

Use this skill when the project must work well on iPhone or other phone-sized devices.

## Default workflow

1. Test the UI at an iPhone-sized viewport first.
2. Verify top-level navigation, buttons, dialogs, and scroll areas.
3. Check that no content is clipped, hidden, or overlapping.
4. Confirm that the layout still works after rotation or viewport changes when relevant.
5. Capture screenshots of important mobile states.

## Important rules

- Prefer mobile web or PWA flows over native-only assumptions.
- Keep the UI usable in Safari.
- Watch for keyboard overlap, sticky bars, and off-screen controls.
- Treat small screen width as the primary constraint.

## Good use cases

- Validate that the EA FC automation UI is usable on iPhone.
- Check that dashboards, lists, and action buttons fit on small screens.
- Make sure a bookmarklet or shortcut only acts as an entry point, not the core system.

## Output

- Mobile layout issues found.
- Screenshot evidence.
- Short notes on whether the flow is usable on iPhone.
