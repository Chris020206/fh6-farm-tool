# MVP Scope Lock

This document locks the current MVP boundary for the Forza Automation Assist.

The MVP is in controlled/manual validation and hardening. It is not a broad
production release. Automation is run only through explicit guarded commands,
and normal `main.py` startup remains safe.

## Included MVP Systems

The following systems are included in the MVP scope:

- Auto1 Race Automation.
- Auto2 Buy Car Automation.
- Auto3 Skill Tree Automation.
- Auto3 guarded multi-car unlock validation up to 4 cars from start row `A`.
- Profile summary and filtering.
- Profile backup and restore.
- Custom profile creation.
- Timing-only profile editing for custom profiles.
- Profile selection in manual commands.
- F8 stop safety in guarded real-input commands.
- Guarded real-input manual commands with explicit confirmation flags.

## Excluded / Postponed Systems

The following systems are explicitly outside the current MVP scope:

- Auto4 Remove Cars.
- Public installer and signed release packaging.
- F7 start hotkey.
- Pause/resume.
- Auto3 production/unattended command.
- Auto3 counts greater than 4.
- Auto3 flexible `--start-row` behavior.
- Auto2 production multi-cycle purchase command.
- Profile key editing.
- Profile navigation-count editing.
- Timing optimization.

The guarded desktop UI is part of the current controlled developer/manual MVP
surface. It is not public launch-ready. Public paid launch still requires
further desktop hardening, packaging, and release validation.

## Why Auto3 Is Included

Auto3 is included because it completes the core farming loop:

1. Auto1 earns race rewards.
2. Auto2 buys target cars.
3. Auto3 unlocks skill-tree rewards from those cars.

Without Auto3, the MVP would validate only earning and buying, not the full
intended farming flow.

Auto3 currently includes guarded/manual multi-car unlock validation through the
validated traversal:

```text
A1 -> B1 -> C1 -> A2
```

The current hard max is 4 cars, and the current start-row assumption is row
`A`. Production/unattended Auto3 behavior remains excluded.

## Why Auto4 Is Not Current Scope

Auto4 Remove Cars is not part of the current controlled MVP hardening scope
because it carries destructive risk.

Removing cars changes the user's garage state and has a higher trust
requirement than racing, buying, or unlocking a known skill-tree path. Auto4
should not be added until the existing MVP systems are stable, well documented,
and easier to supervise.

M11 strategic doctrine treats Auto4 as a conditional pre-launch candidate, not
as a launch blocker and not as rejected scope. It should only move forward if a
future milestone proves it can be strongly guarded, clearly explained, and safe
enough to protect trust.

## Current MVP Stage

The current stage is:

- controlled manual operation
- guarded real-input validation
- safety and documentation hardening
- profile-driven timing support

The current stage is not:

- broad production release
- unattended automation
- packaged consumer app
- public paid UI workflow

The MVP should continue to prioritize reliability, explicit user confirmation,
safe refusal behavior, and clear recovery paths over speed or convenience.
