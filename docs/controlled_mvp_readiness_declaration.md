# Controlled MVP Readiness Declaration

The FH6 Farm Tool is Controlled MVP Ready for developer/manual use.

This means the current validated command surface is ready for careful,
supervised use by a developer/operator who understands the required FH6
baseline states and command safety boundaries.

This does not mean the project is ready for broad public/customer release.

## Included Controlled MVP Systems

The controlled MVP includes:

- Auto1 guarded manual race automation.
- Auto2 guarded test-mode validation.
- Auto2 guarded one-car purchase validation.
- Auto3 guarded multi-car unlock validation up to 4 cars.
- Profile summary and filtering.
- Profile backup and restore.
- Custom profile creation.
- Timing-only custom profile editing.
- Profile selection in supported manual commands.
- F8 stop support in guarded real-input commands.
- Refusal-path tests for dangerous/manual commands.
- Safe `main.py` startup that loads configuration, logs startup, and exits
  without running automation.

## Current Hard Boundaries

The controlled MVP has these hard boundaries:

- Auto3 hard max: 4 cars.
- Auto3 start row assumption: `A`.
- No Auto4/remove-car behavior.
- No UI/dashboard.
- No packaging/installer.
- No production/unattended automation mode.
- No F7 start hotkey.
- No pause/resume.
- No timing optimization yet.
- No profile key editing.
- No profile navigation-count editing.

These boundaries should not be expanded without a separate milestone, review,
and validation pass.

## Conditions For Use

Controlled MVP use requires:

- Correct FH6 baseline state before running any automation command.
- Manual/developer operation of real-input commands.
- Required confirmation flags for real-input and spend-risk commands.
- Active user monitoring during execution.
- F8 stop kept available and ready during guarded real-input runs.
- Conservative profile timings preserved unless a specific profile-tuning
  validation justifies a change.

Real-input commands can spend credits or skill points. They should be run only
when the user is prepared to supervise and stop the command if FH6 state drifts
from the expected baseline.

## What Ready Means

Controlled MVP Ready means:

- Auto1, Auto2, and Auto3 core MVP loop behavior has been validated within the
  documented manual boundaries.
- Dangerous commands refuse without required confirmation flags.
- Startup remains safe.
- Shared systems remain centralized.
- Current documentation identifies the validated behavior and known limits.

## What Ready Does Not Mean

Controlled MVP Ready does not mean:

- Public/customer release ready.
- Unattended automation ready.
- Packaged app ready.
- UI workflow ready.
- Safe to increase Auto3 beyond 4 cars.
- Safe to add Auto4/remove-car behavior.
- Safe to optimize timings without validation.

## Next Recommended Phase

The next recommended phase is MVP polish and hardening.

Priority should go to:

- documentation cleanup and runbooks
- command usability polish
- additional refusal/profile-selection tests
- clearer baseline-state guidance
- packaging/release planning only after the manual command surface is stable

The next phase should not add new automation capability until the current
controlled MVP surface has been hardened further.
