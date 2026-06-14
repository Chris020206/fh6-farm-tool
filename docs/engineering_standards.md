# Engineering Standards

These standards define the baseline rules for future FH6 Farm Tool work.

## Naming Conventions

- Use `snake_case` for file names, function names, and variable names.
- Use `PascalCase` for class names.
- Prefer explicit names over vague names.
- Names should describe the responsibility of the code they identify.

## Architecture Rules

- Keep files small and focused. Do not create monolithic files.
- Keep `main.py` minimal. Do not put automation logic in `main.py`.
- Do not put UI logic in core systems.
- Shared runtime systems belong in `core/`.
- Automation modules belong in `automation/`.
- Configuration files belong in `config/`.
- Configuration loading belongs in dedicated configuration-loading modules.
- Logging remains centralized in the project logging module.
- Keep responsibilities separated by module.

## Code Quality Rules

- Prefer readability over cleverness.
- Use small, focused functions.
- Do not hardcode behavior that should come from configuration.
- Do not add speculative architecture.
- Add only the structure needed for the current milestone.
- Keep future behavior easy to review before it is implemented.

## Current Boundaries

- Auto1, Auto2, and Auto3 automation modules exist and must remain separated.
- Shared runtime systems exist for input control, timing, sequence execution,
  stop handling, logging, settings, profiles, product metadata, readiness, and
  session/history modeling.
- The PySide6 desktop UI foundation exists under `desktop/` and launches via
  `python -B -m desktop.app`.
- Normal `main.py` startup remains safe and must not run automation or send
  keyboard input.
- Real input remains guarded. Do not instantiate real keyboard input or register
  hotkeys from ordinary import paths.
- Auto1 has a guarded desktop UI execution path. Preserve focus handoff, F8
  stop behavior, fail-closed handling, and the Auto1-only race drive duration
  runtime adjustment.
- Auto2 and Auto3 must not execute from the desktop UI until a future milestone
  explicitly wires and validates them.
- Official profiles remain protected. Runtime UI adjustments must stay narrow,
  explicit, and automation-specific.
- Auto4/remove-car behavior remains outside current implementation boundaries.
