# Auto1 Reliability Validation Report

This report records the current validated Auto1 behavior before further
development. It documents manual real-input testing only. This is not
production mode.

## Tested Scenarios

- 1-cycle real-input FH6 test
- 2-cycle real-input FH6 test
- F8 stop during `w` hold
- F8 stop during post-cycle wait
- 10-cycle real-input FH6 validation
- 25-cycle real-input FH6 validation attempt with manual F8 stop during cycle
  16
- Official guarded manual Auto1 command validation with 2 requested cycles

## Confirmed Working Behavior

- Startup delay works.
- Restart key works.
- Confirm timing works.
- `w` hold duration works.
- `w` release works.
- Post-cycle delay works.
- F8 stop works during hold.
- F8 stop works during wait.
- Cleanup works after completion and stop.
- 10/10 cycles completed successfully during real-input FH6 validation.
- During the 25-cycle validation attempt, 15 cycles completed successfully
  before manual F8 stop during cycle 16.
- F8 stop triggered correctly during the extended validation attempt.
- Final status was `stopped`.
- `completed_cycles` reported `15`.
- No stuck keys were observed.
- Stop cleanup executed successfully.
- Official command tested with 2 requested cycles.
- F8 stop triggered during cycle 2.
- `completed_cycles` reported `1`.
- Final status was `stopped`.
- No stuck `w` was observed.

## Official Manual Command

`run_auto1.py` has been created as the official guarded manual Auto1 command.

Command:

```powershell
python -B -m automation.auto1_race.run_auto1 <cycles> --confirm
```

Current command rules:

- A finite cycle count is required.
- `--confirm` is required.
- F8 stop is available during execution.
- Startup delay is profile-driven.
- The official Auto1 profile is used.
- `dangerous_auto1_real_input_test.py` remains debug/test-only.

## Current Official Auto1 Profile Values

Profile: `profiles/official/auto1_race_default.json`

Keys:

- `restart_key`: `x`
- `confirm_key`: `enter`
- `throttle_key`: `w`

Timings:

- `startup_delay`: `5.0`
- `wait_after_restart`: `2.0`
- `wait_after_first_confirm`: `10.0`
- `race_duration`: `40.0`
- `post_cycle_delay`: `3.0`

## Known Minor Issues

- Duplicate cleanup logs can appear because cleanup is intentionally called in
  multiple safe exit paths.
- `completed_cycles` may undercount if stop occurs during the final post-cycle
  wait, because the cycle is not counted complete until the full action list has
  returned.

## Current Limitations

- Auto1 real-input execution is available through guarded manual commands only.
- This is controlled manual operation, not broad production release.
- No UI exists yet.
- No F7 start hotkey exists yet.
- No packaged app exists yet.
- Real keyboard execution is not wired into normal startup.
- Auto2 and Auto3 now have their own guarded validation commands and remain
  separate from Auto1.
- Auto4 is postponed.

## Current Safety Boundary

The guarded real-input test requires:

- explicit finite cycle count
- `--confirm-real-input`
- manual launch from the terminal

Normal `main.py` startup does not run Auto1 or send keyboard input.
