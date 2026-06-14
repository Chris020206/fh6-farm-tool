# FH6 Farm Tool

Modular FH6 Farm Tool implementation in controlled manual validation and MVP
hardening.

The project is organized as small modules with clear ownership boundaries. This
stage includes shared runtime systems, guarded manual operator commands,
profile tooling, a PySide6 desktop UI foundation, and documentation for
validated Auto1/Auto2/Auto3 behavior. It is not a broad production release.

The current command surface and desktop UI are for controlled developer/manual
operation. The desktop shell now provides the real UI foundation for Home,
Automation Environment, commitment, supervision, and completion states, but it
is not public launch-ready. M11 strategy still requires a restrained premium
desktop UI to be hardened before public paid launch.

Normal `main.py` startup remains safe: it loads configuration, logs startup,
and exits without running automation or sending keyboard input.

## Structure

- `app/` application coordination
- `automation/` Auto1, Auto2, and Auto3 automation modules
- `core/` shared runtime systems
- `profiles/` official/custom profile storage, validation, and commands
- `settings/` future configuration handling
- `app_logging/` application logging support
- `ui/` product-facing non-visual UI structure
- `desktop/` PySide6 desktop UI application foundation
- `assets/` static project assets
- `tests/` test suite
- `config/` configuration files
- `docs/` project documentation
- `main.py` minimal application entry point

## Configuration

Default configuration lives in `config/default_settings.json` and is loaded
through `settings/config_loader.py` during startup. Configuration is centralized
there so future modules can depend on one clear source of application defaults.

## Logging

Application logging is centralized in `app_logging/log_manager.py`. Startup and
configuration loading use the shared logger with a consistent timestamped
format. Shared systems can emit categorized events for `startup`, `config`,
`timing`, `input`, `stop`, `sequence`, `state`, `profile`, and `error`.

## Profiles

Local profile metadata lives under `profiles/official/` and `profiles/custom/`.
Profiles are JSON files loaded through `profiles/profile_manager.py` and
validated by `profiles/profile_validator.py`.

Profile commands are available for read-only summaries, backups, guarded
restores, custom profile creation, custom timing edits, and profile selection
for manual automation commands. Official profiles are protected from timing
edits; tuning is performed through custom profiles.

## Timing

Auto1, Auto2, and Auto3 currently use intentionally conservative
profile-driven timings for reliability across FH6 menu/loading variation and
user hardware differences. Some timings may be slower than necessary. Timing
optimization is postponed until profile tuning is hardened further. This
accepted limitation is documented in
`docs/conservative_timing_decision.md`.

## Input Backends

`InputController` uses the in-memory backend by default. An optional real
keyboard backend exists in `core/input/`, but it is not wired into normal
startup. Real input is available only through guarded manual commands that
require explicit confirmation flags.

A dangerous manual smoke test exists at
`core/input/dangerous_real_keyboard_smoke_test.py`. It refuses to run unless
called with `--confirm-real-input`, and it is not connected to `main.py` or
Auto1.

A dangerous manual Auto1 real-input test exists at
`automation/auto1_race/dangerous_auto1_real_input_test.py`. It requires an
explicit finite cycle count and `--confirm-real-input`; it is not connected to
normal startup. During that manual test only, `F8` is registered as a guarded
stop hotkey.

The official guarded manual Auto1 command is:

```powershell
python -B -m automation.auto1_race.run_auto1 25 --confirm
```

It still requires a finite cycle count and explicit confirmation, and it is not
connected to normal startup.

Auto2 currently provides guarded real-input commands for test-mode menu
validation and exactly one full purchase/reset validation. These commands
require explicit confirmation flags and support F8 stop.

Auto3 currently provides in-memory validation modes, guarded real-input
test-mode navigation, guarded one-car unlock validation, and guarded/manual
multi-car unlock validation. The validated multi-car traversal is:

```text
A1 -> B1 -> C1 -> A2
```

The current guarded Auto3 multi-car unlock hard max is 4 cars. Auto3 remains
dangerous/manual/test-only for real input, and no production Auto3 command
exists. These commands require explicit confirmation flags and support F8 stop
where real input is used.

Auto4 is not part of the current MVP hardening scope. M11 strategy treats it as
a conditional pre-launch candidate only if a future safety milestone proves it
can be strongly guarded, clearly explained, and trust-preserving.

## Desktop UI

The PySide6 desktop UI foundation can be launched with:

```powershell
python -B -m desktop.app
```

The desktop UI currently supports navigation through the Home launch surface,
Automation Environment preparation, commitment countdown, Companion Mode, and
post-run completion states. Visible controls either navigate/update UI state or
refuse unsupported execution calmly.

Real automation remains safety-bound. Auto1 has a guarded UI execution path
with focus handoff, F8 stop preservation, and an Auto1-only race drive duration
adjustment. Auto2 and Auto3 are not executable from the desktop UI. They remain
available only through their existing guarded/manual commands until a future
integration milestone explicitly changes that boundary.

## Engineering Standards

Baseline engineering standards are documented in
`docs/engineering_standards.md`. Future implementation work should follow those
rules unless a milestone explicitly changes them.
