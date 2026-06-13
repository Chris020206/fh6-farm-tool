# R15 PySide6 Shell Prototype

## Purpose

This prototype validates whether PySide6 can represent the existing FH6 Farm Tool shell architecture.

It is intentionally narrow and reversible.

## What It Renders

- App window.
- Stable sidebar destinations:
  - Home
  - Profiles
  - History
  - Help
  - Settings
- Placeholder screen area.
- Basic navigation between placeholder screens.
- Primary, secondary, and tertiary content zones as placeholders.
- Automation Environment prototype screen opened from Home.
- Automation Environment six-section structure:
  - Overview
  - Profile
  - Readiness
  - Contextual Warnings
  - Advanced / Refinement
  - Run

The prototype reads from the existing non-visual shell descriptors in `ui/shell.py`.
The Automation Environment prototype uses existing product-facing screen structure and a prepared preview plan without execution wiring.

## How To Run

Install PySide6 in your local environment, then run:

```powershell
python -B -m desktop.pyside6_shell_prototype
```

If PySide6 is not installed, the prototype exits with a readable message.

From the Home placeholder screen, use the Automation Environment prototype button to inspect the six-section structure.

## Non-Goals

This prototype does not include:

- Final styling.
- Visual polish.
- Automation execution.
- Runner calls.
- Real input.
- Profile editing.
- Persistence.
- Licensing.
- Payment or paywall logic.
- Companion mode implementation.

## Safety Boundary

The prototype is UI-only.

It does not connect to automation runners, real keyboard input, timings, CLI commands, or safety gates.
