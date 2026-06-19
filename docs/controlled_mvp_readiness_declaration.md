# Controlled MVP Readiness Declaration

Forza Automation Assist is Controlled MVP Ready for developer/manual use.

This means the current validated desktop UI and guarded command surface are
ready for careful, supervised use by a developer/operator who understands the
required FH6 baseline states and command safety boundaries.

This does not mean the project is ready for broad public/customer release.

## Included Controlled MVP Systems

The controlled MVP includes:

- Auto1 guarded manual race automation.
- Auto1 validated desktop UI execution.
- Auto1 focus handoff and fail-closed behavior.
- Auto1 runtime adjustment.
- Auto1 F8 stop and completion behavior.
- Auto2 guarded test-mode validation.
- Auto2 validated desktop UI execution.
- Auto2 guarded purchase mode with purchase count greater than 1 validated.
- Auto2 spending-risk protections and completion behavior.
- Auto3 validated desktop UI execution.
- Auto3 first-car exception, safety reset navigation, and Recently Added
  re-sort.
- Auto3 guarded multi-car unlock validation up to 4 cars.
- Auto3 row 3 / column 1 -> row 1 / column 2 transition.
- Auto3 corrected timing model and completion behavior.
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
- No public launch-ready UI.
- No packaging/installer.
- No production/unattended automation mode.
- No startup automation.
- No F7 start hotkey.
- No pause/resume.
- No timing optimization without validation.
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
- Auto1, Auto2, and Auto3 desktop execution has been validated for
  controlled/manual use.
- Completion behavior has been validated.
- Dangerous commands refuse without required confirmation flags.
- Startup remains safe.
- Shared systems remain centralized.
- Current documentation identifies the validated behavior and known limits.
- Anti-regression boundaries are documented in `VALIDATED_BEHAVIOR.md`.

## What Ready Does Not Mean

Controlled MVP Ready does not mean:

- Public/customer release ready.
- Unattended automation ready.
- Packaged app ready.
- Public launch-ready UI workflow.
- Safe to increase Auto3 beyond 4 cars.
- Safe to add Auto4/remove-car behavior.
- Safe to optimize timings casually or without validation.

## Next Recommended Phase

The next recommended phase is documentation and desktop hardening.

Priority should go to:

- documentation realignment
- desktop UI hardening
- launch-facing UX refinement
- maintainability and architecture cleanup
- anti-regression discipline
- packaging planning only

The next phase should not add new automation capability until the current
controlled MVP surface has been hardened further.
