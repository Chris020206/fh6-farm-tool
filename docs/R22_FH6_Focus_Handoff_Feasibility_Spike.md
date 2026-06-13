# R22 FH6 Focus Handoff Feasibility Spike

## Purpose

This spike tests whether FH6 Farm Tool can safely attempt to focus the FH6 game window before automation begins.

This is a feasibility spike only.

It does not run automation, press automation keys, change timings, or modify safety gates.

## Why This Matters

Current guarded real-input operation assumes the user manually focuses FH6 during the startup countdown.

If focus handoff proves reliable, future UI can reduce friction by clearly communicating:

- Focusing FH6...
- Run starts in 3...

This could support:

- calmer handoff
- less layout pressure
- reduced operator scrambling
- a more refined companion-utility feel

Automatic focus must remain visible and understandable. It should be refinement, not invisible magic.

## Expected FH6 Display Modes To Test

Future manual validation should test:

1. FH6 windowed mode.
2. FH6 borderless/windowed fullscreen.
3. FH6 fullscreen, if applicable.

No fullscreen success is assumed.

## Implementation Boundaries

The spike is isolated in:

- `integrations/windows_focus_handoff.py`
- `tools/focus_handoff_smoke_test.py`

The implementation:

- uses Windows-only focus APIs through `ctypes`
- avoids adding pywin32 or pywinauto for now
- lists likely FH6 windows
- refuses on non-Windows systems
- refuses if no likely FH6 window is found
- refuses if multiple likely windows are found without an exact title
- refuses focus attempts without explicit confirmation
- never presses automation keys

## Manual Smoke Test

List likely FH6 windows without attempting focus:

```powershell
python -B -m tools.focus_handoff_smoke_test
```

Attempt focus only after explicit confirmation:

```powershell
python -B -m tools.focus_handoff_smoke_test --confirm-focus
```

If multiple likely windows are found, provide the exact title:

```powershell
python -B -m tools.focus_handoff_smoke_test --target-title "Forza Horizon 6" --confirm-focus
```

## Possible Outcomes

### 1. Works Reliably In All Modes

If focus handoff works in windowed, borderless/windowed fullscreen, and fullscreen, future UI may reduce reliance on manual focus during countdown.

Layout strategy impact:

- Run flow can include a clear focus-handoff status.
- The app can remain compact without asking the user to race the countdown.

### 2. Works Only In Windowed / Borderless

If focus handoff works only in windowed or borderless modes, the future UI should communicate that requirement clearly.

Layout strategy impact:

- Readiness guidance should mention the supported display mode.
- Manual countdown handoff may remain necessary for unsupported modes.

### 3. Unreliable

If focus handoff is inconsistent, the feature should remain out of execution flow.

Layout strategy impact:

- Preserve manual focus assumptions.
- Keep startup delay/readiness guidance visible.
- Do not design the run flow around automatic focus.

## Current Status

This spike is implemented but not validated against FH6 display modes yet.

No automation command uses focus handoff.

No UI behavior has been changed based on this spike.
