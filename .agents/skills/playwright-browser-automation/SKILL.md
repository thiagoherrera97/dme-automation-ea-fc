---
name: playwright-browser-automation
description: Browser automation for the EA FC web app using Playwright or browser-driven scripts. Use for login flows, navigation, form filling, screenshots, and validating dynamic UI behavior.
---

# Playwright browser automation

Use this skill when the task involves automating or testing the EA FC web app in a browser.

## Default workflow

1. Open the target page in a visible browser.
2. Wait for the page to finish loading.
3. Inspect the DOM before interacting with controls.
4. Use stable locators and text-based selectors when possible.
5. Capture screenshots after major state changes.
6. Keep browser sessions alive so login state is preserved.

## Important rules

- Do not try to bypass login, 2FA, or account verification.
- Stop and ask for human input when the flow requires a verification code or another manual checkpoint.
- Prefer scripts that are small, repeatable, and easy to debug.
- Keep temporary automation code outside the repo unless it is meant to be reused.

## Good use cases

- Test the EA FC web app login flow.
- Verify page transitions and button behavior.
- Check that SBC-related screens render correctly.
- Capture screenshots for reference.

## Output

- Clear pass/fail summary.
- Notes about the exact screen reached.
- Screenshot paths when helpful.
