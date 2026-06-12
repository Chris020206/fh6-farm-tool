# Auto1 FH6 Manual Test Checklist

This checklist is for the first guarded FH6 real-input Auto1 test. This is not
production mode.

## Safety Warning

This test sends real keyboard input.

F8 stop is available for guarded Auto1 real-input execution, including the
official guarded command:

```powershell
python -B -m automation.auto1_race.run_auto1 25 --confirm
```

Keep F8 ready during execution. Auto1 remains supervised/manual and does not
provide unattended safety.

## Starting Location

Start on the post-race restart screen where pressing `x` restarts the event.

Do not start this test from the map, garage, festival menu, pause menu, or any
screen where `x`, `enter`, or `w` could trigger unrelated actions.

## Required FH6 Settings

- FH6 must be focused and ready to receive keyboard input.
- Keyboard controls must match the official Auto1 profile keys.
- Restart must be available from the current post-race screen.
- Confirm prompts must accept `enter`.
- Throttle must be bound to `w`.

## Required Keys

- `x` = restart
- `enter` = confirm
- `w` = throttle

## Command

Run one cycle only:

```powershell
python -B -m automation.auto1_race.dangerous_auto1_real_input_test 1 --confirm-real-input
```

Use `--fast` only outside FH6 for dry validation. Do not use `--fast` for real
race validation because it shortens timing values.

## Expected Behavior

The test should:

- press `x` to restart the event
- wait after restart
- press `enter`
- wait after confirm
- press `enter` again
- hold `w` for the configured race duration
- release held keys at the end
- report `completed_cycles: 1`
- report `final_status: completed`

## Watch For

- FH6 must stay focused while the test runs.
- Restart should happen only once.
- Confirm prompts should advance as expected.
- The car should accelerate only during the throttle hold.
- The terminal should report one completed cycle.
- No key should remain held after the test.

## Emergency Recovery

If behavior is not expected:

- Press F8 to request a safe stop.
- Alt-tab away from FH6 if needed.
- Stop the terminal process if needed.
- Manually release or press keys if needed.
- Check that `w`, `enter`, and `x` are not stuck.
- Do not rerun until the starting screen and key bindings are verified.

## Rollback Expectation

This test does not change project configuration, profiles, or FH6 settings. If
the behavior is wrong, stop the process and return FH6 to the required starting
location before trying again.
