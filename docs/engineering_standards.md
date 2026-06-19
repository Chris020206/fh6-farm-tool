# Engineering Standards

These standards define the baseline rules for future Forza Automation Assist work.

## Naming Conventions

- Use `snake_case` for file names, function names, and variable names.
- Use `PascalCase` for class names.
- Prefer explicit names over vague names.
- Names should describe the responsibility of the code they identify.

## Architecture Rules

- Keep files small and focused. Do not create monolithic files.
- Keep `main.py` minimal. Do not put automation logic in `main.py`.
- Do not put UI logic in core systems.
- Desktop UI orchestration belongs under `desktop/`.
- Desktop execution adapters belong under `desktop/execution/`.
- UI code must not directly import dangerous/manual automation harnesses when
  an adapter boundary exists.
- Real keyboard input must remain lazily imported only inside guarded execution
  paths.
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
- Auto1, Auto2, and Auto3 each have guarded desktop UI execution paths validated
  for controlled/manual use only.
- Preserve Auto1 focus handoff, F8 stop behavior, fail-closed handling, runtime
  adjustment, loop count handling, and completion-state behavior.
- Preserve Auto2 test mode, purchase mode, purchase count handling,
  spending-risk protection, and completion-state behavior.
- Preserve Auto3 first-car exception, safety reset navigation, Recently Added
  re-sort, multi-car traversal, timing model, row/column transition behavior,
  and completion-state behavior.
- Do not regress validated desktop execution behavior without explicit approval.
- Official profiles remain protected. Runtime UI adjustments must stay narrow,
  explicit, and automation-specific.
- Auto4/remove-car behavior remains outside current implementation boundaries.
- Dangerous/manual harnesses must not become ordinary startup or import paths.
- No unattended automation.
- Validated behavior is a source-of-truth boundary. Any change affecting
  Auto1, Auto2, or Auto3 execution must preserve the validated baseline unless
  explicitly approved.
