# Command Index

This document lists the current command-line surface for the FH6 Farm Tool.

`main.py` is safe: it loads configuration, logs startup, and exits. It does not
run automation.

## Command Output

Manual commands use structured operator output for refusals and run summaries.
The CLI remains the primary guarded/manual automation surface. The PySide6
desktop UI foundation now uses the same status, reason, risk, required-action,
and summary concepts for warning cards, preparation panels, supervision states,
and completion summaries, but it is not public launch-ready.

Refusals are expected to show:

- command
- reason
- relevant details
- required action
- suggested next step where useful
- risk level

## Desktop UI Foundation

Launches the PySide6 desktop UI foundation:

```powershell
python -B -m desktop.app
```

Current boundary:

- Home, Automation Environment, commitment, Companion Mode, and completion
  states are represented.
- Auto1 has a guarded UI execution path.
- Auto2 and Auto3 do not execute from the desktop UI.
- Normal startup through `main.py` remains safe.
- The desktop UI is not public launch-ready.

## Auto1 Official Manual Run

Runs Auto1 with real keyboard input through the guarded manual command.

```powershell
python -B -m automation.auto1_race.run_auto1 25 --confirm
```

Required:

- finite cycle count
- `--confirm`

Optional profile selection:

```powershell
python -B -m automation.auto1_race.run_auto1 25 --confirm --profile auto1_safe_slow
```

Safety notes:

- Sends real keyboard input.
- F8 is available to request stop during execution.
- Uses official Auto1 profile by default.
- `--profile` must point to an `auto1_race` profile.

## Auto2 Test-Mode Real-Input Validation

Runs Auto2 menu navigation with real keyboard input, but excludes purchase
actions.

```powershell
python -B -m automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test 1 --confirm-real-input
```

Optional fast timing validation:

```powershell
python -B -m automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test 1 --confirm-real-input --fast
```

Optional profile selection:

```powershell
python -B -m automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test 1 --confirm-real-input --profile auto2_safe_slow
```

Required:

- finite cycle count greater than 0
- `--confirm-real-input`

Safety notes:

- Sends real keyboard input.
- Does not include purchase actions.
- F8 is available to request stop during execution.
- `--profile` must point to an `auto2_buy_car` profile.

## Auto2 One-Car Purchase Test

Runs exactly one full Auto2 purchase/reset cycle with real keyboard input.

```powershell
python -B -m automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test 1 --confirm-real-input --confirm-purchase
```

Optional profile selection:

```powershell
python -B -m automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test 1 --confirm-real-input --confirm-purchase --profile auto2_safe_slow
```

Required:

- cycle count must be exactly 1
- `--confirm-real-input`
- `--confirm-purchase`

Safety notes:

- Sends real keyboard input.
- Will spend credits.
- F8 is available to request stop during execution.
- This is a dangerous/manual/test-only command, not production mode.
- `--profile` must point to an `auto2_buy_car` profile.

## Profile Summary

Lists official profiles and their values.

```powershell
python -B -m profiles.profile_summary
```

Filter by profile type:

```powershell
python -B -m profiles.profile_summary --type auto1_race
python -B -m profiles.profile_summary --type auto2_buy_car
python -B -m profiles.profile_summary --type auto3_skill_tree
```

Safety notes:

- Read-only.
- Does not run automation.

## Profile Backup

Creates a timestamped backup of `profiles/official/` and `profiles/custom/`.

```powershell
python -B -m profiles.profile_backup
```

Output includes:

- backup location
- number of files copied

Safety notes:

- Does not modify profile source files.
- Does not run automation.

## Profile Restore

Restores profiles from a timestamped backup.

```powershell
python -B -m profiles.profile_restore 20260611_045210 --confirm-restore
```

Required:

- backup timestamp folder under `backups/profiles/`
- `--confirm-restore`

Safety notes:

- Refuses without `--confirm-restore`.
- Creates an automatic safety backup before restoring.
- Restores both `profiles/official/` and `profiles/custom/`.
- Does not delete backups.
- Does not run automation.

## Custom Profile Creation

Creates a custom profile by copying an official profile.

```powershell
python -B -m profiles.profile_create_custom --source auto1_race_default --name auto1_safe_slow
python -B -m profiles.profile_create_custom --source auto2_buy_car_default --name auto2_safe_slow
python -B -m profiles.profile_create_custom --source auto3_skill_tree_default --name auto3_safe_slow
```

Safety notes:

- Does not modify official profiles.
- Refuses duplicate custom profile names/files.
- Created profiles are validated.
- Does not run automation.

## Timing Editing

Edits one timing value on a custom profile only.

```powershell
python -B -m profiles.profile_edit_timing --profile auto1_safe_slow --timing startup_delay --value 7.0
python -B -m profiles.profile_edit_timing --profile auto2_safe_slow --timing menu_key_delay --value 2.0
python -B -m profiles.profile_edit_timing --profile auto3_safe_slow --timing menu_key_delay --value 1.25
```

Safety notes:

- Custom profiles only.
- Official profiles are refused.
- Timing key must already exist.
- Value must be a finite non-negative number.
- Profile validation runs before saving.
- A backup is recommended before editing.
- Does not run automation.

## Auto3 In-Memory CLI Test

Runs one Auto3 sequence using the in-memory input backend only.

```powershell
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode first-car-test
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode normal-next-car-test
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode full-first-car
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode full-normal-next-car
```

Optional fast timing validation:

```powershell
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode first-car-test --fast
```

Optional profile selection:

```powershell
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode first-car-test --profile auto3_skill_tree_default
```

Safety notes:

- In-memory only.
- Does not send real keyboard input.
- Does not register F8.
- Does not run automatically from `main.py`.
- `--profile` must point to an `auto3_skill_tree` profile.

## Auto3 Test-Mode Real-Input Validation

Runs Auto3 menu navigation with real keyboard input, but excludes perk unlock
actions.

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_test_mode_real_input_test --mode first-car-test --confirm-real-input
python -B -m automation.auto3_skill_tree.dangerous_auto3_test_mode_real_input_test --mode normal-next-car-test --confirm-real-input
```

Optional fast timing validation:

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_test_mode_real_input_test --mode first-car-test --confirm-real-input --fast
```

Optional profile selection:

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_test_mode_real_input_test --mode first-car-test --confirm-real-input --profile auto3_skill_tree_default
```

Required:

- `--confirm-real-input`
- `--mode first-car-test` or `--mode normal-next-car-test`

Safety notes:

- Sends real keyboard input.
- Does not include perk unlock actions.
- F8 is available to request stop during execution.
- This is dangerous/manual/test-only.
- `--profile` must point to an `auto3_skill_tree` profile.

## Auto3 One-Car Unlock Test

Runs exactly one guarded Auto3 first-car unlock test with real keyboard input.

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_one_car_unlock_test --mode first-car --confirm-real-input --confirm-unlock
```

Optional profile selection:

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_one_car_unlock_test --mode first-car --confirm-real-input --confirm-unlock --profile auto3_skill_tree_default
```

Required:

- `--mode first-car`
- `--confirm-real-input`
- `--confirm-unlock`

Safety notes:

- Sends real keyboard input.
- May spend skill points.
- F8 is available to request stop during execution.
- Only the first-car path is supported.
- This is dangerous/manual/test-only, not broad production mode.
- `--profile` must point to an `auto3_skill_tree` profile.

## Auto3 Multi-Car Unlock Test

Runs guarded Auto3 multi-car unlock validation with real keyboard input.

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test --cars 4 --confirm-real-input --confirm-unlock
```

Optional profile selection:

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test --cars 4 --confirm-real-input --confirm-unlock --profile auto3_skill_tree_default
```

Required:

- `--cars <count>`
- `--confirm-real-input`
- `--confirm-unlock`

Current limits:

- Maximum cars: `4`
- Start row assumption: `A`
- Validated traversal: `A1 -> B1 -> C1 -> A2`

Safety notes:

- Sends real keyboard input.
- Will spend skill points.
- F8 is available to request stop during execution.
- This is dangerous/manual/test-only, not a production command.
- Counts greater than 4 are refused.
- `--profile` must point to an `auto3_skill_tree` profile.

## Current Product Boundary

The project is in controlled/manual validation and MVP hardening. It is not a
broad production release. Real-input commands require explicit confirmation
flags, and `main.py` does not run automation.

Auto4 is postponed. Timing values are intentionally conservative and may be
optimized later through profile tuning.
