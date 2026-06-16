# Auto1 Operator Runbook

## Purpose

Auto1 runs the validated FH6 race farming flow.

It restarts the target race, confirms the required prompts, holds throttle for
the configured race duration, and repeats for a finite number of cycles.

Auto1 is part of the Controlled MVP. It is guarded/manual execution for a
developer/operator. It is not unattended automation and is not a public
customer workflow.

---

## Required FH6 Baseline State

Before running Auto1, FH6 must be in the validated race restart state.

Required baseline:

- FH6 is focused and ready to receive keyboard input.
- The user is on the post-race restart screen where pressing `x` restarts the
  event.
- Restart is available from the current screen.
- Confirm prompts accept `enter`.
- Throttle is bound to `w`.
- The selected car/race setup matches the validated Auto1 path.
- The operator is present and watching the run.
- F8 is ready to stop the command if FH6 state drifts.

Do not start Auto1 from the map, garage, pause menu, festival menu, or any
screen where `x`, `enter`, or `w` could trigger unrelated behavior.

Validated key assumptions:

- `x` = restart
- `enter` = confirm
- `w` = throttle

The current validated behavior depends on conservative profile timings, not on
adaptive FH6 state detection.

---

## Command To Run

Official guarded Auto1 command:

```powershell
python -B -m automation.auto1_race.run_auto1 25 --confirm
```

`25` is the finite cycle count. One cycle means one Auto1 race restart and
drive sequence.

`--confirm` is required. It confirms that the operator understands Auto1 will
send real keyboard input.

Optional profile usage:

```powershell
python -B -m automation.auto1_race.run_auto1 25 --confirm --profile auto1_safe_slow
```

If `--profile` is omitted, the official Auto1 profile is used.

---

## Desktop UI Execution

Auto1 may also be launched through the validated PySide6 desktop UI for
controlled/manual use.

Desktop execution includes:

- FH6 focus handoff before execution
- fail-closed behavior if focus handoff or preparation fails
- F8 stop availability
- Auto1 runtime race duration adjustment
- finite loop count handling
- completion-state reporting

The race duration adjustment is intentionally Auto1-only. Use it only when the
validated race timing changes.

If FH6 focus handoff fails, Auto1 must not start. Return to preparation, restore
the required FH6 baseline, and retry only when the operator can supervise the
run.

Desktop execution does not remove the supervision requirement. Keep F8 ready
and watch FH6 throughout the run.

---

## Expected Behavior

Normal Auto1 behavior:

- startup delay gives the operator time to focus FH6
- Auto1 presses the restart key
- Auto1 waits after restart
- Auto1 presses confirm
- Auto1 waits for the FH6 transition
- Auto1 presses confirm again
- Auto1 holds throttle for the configured race duration
- Auto1 releases held input
- Auto1 waits for the post-cycle delay
- Auto1 continues until the finite cycle count is complete or F8 stop is
  requested

This is behaving normally if FH6 remains focused, the race restarts as
expected, the car accelerates during the throttle hold, and cycle progress
continues without unexpected menus.

---

## Success Condition

A successful Auto1 run:

- completes the requested finite cycle count, or stops safely when F8 is used
- releases held keys
- reports a clear final status
- leaves FH6 in an expected post-cycle/restart-ready state
- does not require manual keyboard cleanup afterward

---

## Stop Immediately If

Press `F8` immediately if:

- the wrong menu opens
- FH6 loses focus
- Auto1 desynchronizes from the race flow
- an unexpected prompt or screen appears
- the race does not restart correctly
- the car does not accelerate when expected
- throttle appears stuck
- any key appears to affect the wrong FH6 state

After pressing F8, keep watching until input cleanup completes. If needed,
manually return FH6 to a safe state before running Auto1 again.

---

## Common Failure Modes

Incorrect FH6 starting state

- Likely cause: Auto1 was started from the wrong screen.
- Corrective action: press F8, stop the command, return to the post-race
  restart screen, and verify `x` restarts the event before retrying.

Focus issues

- Likely cause: FH6 was not the active window when the startup delay ended.
- Corrective action: press F8 if the run started in the wrong application or
  wrong FH6 state. Refocus FH6 before the next attempt.

Timing drift

- Likely cause: FH6 menu/loading timing differs from the validated timing
  assumptions.
- Corrective action: press F8, review the selected profile timings, and only
  adjust timing through custom profile workflow after backing up profiles.

Unexpected menu state

- Likely cause: FH6 opened a different prompt than the validated race restart
  flow.
- Corrective action: press F8, restore the known restart baseline, and do not
  rerun until the prompt sequence is understood.

---

## Current Boundaries

Auto1 current boundaries:

- guarded/manual only
- validated desktop UI execution for controlled/manual use only
- finite execution only
- no unattended mode
- no startup automation
- no timing optimization in the official profile
- profile-driven conservative timing
- official profile used by default
- runtime adjustment remains narrow and Auto1-specific
- custom profile timing edits only through the profile tooling

Auto1 is Controlled MVP behavior, not broad production release behavior.

---

## Safety Notes

Auto1 should be run only by a developer/operator who is actively supervising
FH6.

The safety model is trust-first:

- use explicit confirmation
- keep F8 ready
- monitor the run
- stop on unexpected behavior
- keep execution finite
- preserve validated conservative timings

Do not run Auto1 unattended. Do not increase speed or change timings casually.
Do not rerun after a failure until FH6 is back in the required baseline state.
