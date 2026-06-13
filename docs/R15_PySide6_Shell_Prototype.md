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

The prototype reads from the existing non-visual shell descriptors in `ui/shell.py`.

## How To Run

Install PySide6 in your local environment, then run:

```powershell
python -B -m desktop.pyside6_shell_prototype
```

If PySide6 is not installed, the prototype exits with a readable message.

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
