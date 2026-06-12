# Auto3 Operator Runbook

## Purpose

Auto3 automates the FH6 skill-tree menu flow for the current validated wheelspin/perk path. It navigates from the My Cars baseline into Car Mastery, follows the locked perk unlock path, and returns to the My Cars grid baseline.

Auto3 is part of the Controlled MVP, but current real-input usage remains guarded, manual, and test-only. It is not a production command, not unattended automation, and not a broad-release feature. Confirmed unlock commands can spend skill points.

## Required FH6 Baseline State

Before running Auto3, confirm:

* FH6 is focused and ready to receive keyboard input.
* The operator is supervising the entire run.
* The user is in the Garage -> Cars -> My Cars context.
* The current validated start-row assumption is row A.
* The first target car is the active/seated A1 baseline where applicable.
* The target cars are arranged in the validated traversal order: A1 -> B1 -> C1 -> A2.
* The operator understands confirmed unlock commands may spend skill points.
* F8 is kept ready before and during execution.

Do not run Auto3 from an unknown menu state, an unknown sort state, a different start row, or a car grid position that has not been validated.

## Commands To Run

### In-Memory CLI Validation

```powershell
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode first-car-test
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode normal-next-car-test
```

These commands do not send real keyboard input and do not spend skill points. Use them to verify command routing, profile loading, and generated sequence behavior before any real-input validation.

Optional profile example:

```powershell
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode first-car-test --profile auto3_skill_tree_default
```

### Test-Mode Real-Input Validation

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_test_mode_real_input_test --mode first-car-test --confirm-real-input
python -B -m automation.auto3_skill_tree.dangerous_auto3_test_mode_real_input_test --mode normal-next-car-test --confirm-real-input
```

These commands send real keyboard input. They use Auto3 test-mode paths, exclude perk unlock actions, and are intended to validate real FH6 menu navigation without spending skill points. F8 stop is available after the command is confirmed and started.

### One-Car Unlock Validation

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_one_car_unlock_test --mode first-car --confirm-real-input --confirm-unlock
```

This command sends real keyboard input and may spend skill points. It is limited to the first-car path and requires both confirmation flags. Use test-mode validation first if the baseline is uncertain.

### Multi-Car Unlock Validation

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test --cars 4 --confirm-real-input --confirm-unlock
```

This command sends real keyboard input and may spend skill points. The current guarded hard max is 4 cars. The validated traversal is A1 -> B1 -> C1 -> A2, starting from row A. Both confirmation flags are required. This remains dangerous/manual/test-only and is not a production Auto3 command.

## Expected Behavior

### First-Car Path

The first-car path uses the first-car exception. A1 is already active/seated, so Auto3 does not perform a next-car get-in movement before opening the menu path.

Expected behavior:

* Auto3 performs the validated sort/menu setup.
* Auto3 navigates to Upgrades & Tuning.
* Auto3 navigates to Car Mastery.
* Unlock commands follow the locked perk path only when an unlock command is confirmed.
* Auto3 returns/resets to the My Cars grid baseline after the visit.

### Later-Car Path

Later-car behavior starts after the grid baseline has been restored.

Expected behavior:

* Auto3 moves through the validated grid traversal.
* Auto3 gets into the currently hovered car.
* Auto3 waits through the validated 12-second later-car recovery delay.
* Auto3 uses the validated recovery path: esc, up x6, down, enter, down x7, enter.
* Unlock commands follow the locked perk path only when an unlock command is confirmed.
* Auto3 returns/resets to the My Cars grid baseline after each visited car.

### Multi-Car Flow

The validated multi-car path is:

* A1 -> B1
* B1 -> C1
* C1 -> A2

Movement logic is:

* A1 -> B1: down
* B1 -> C1: down
* C1 -> A2: right, up, up

The run is finite and should terminate cleanly after the requested validated count.

## Success Condition

For test-mode real-input validation, success means Auto3 reaches the expected Car Mastery navigation point without executing perk unlock actions, spending skill points, or losing alignment.

For one-car unlock validation, success means A1 follows the first-car exception path, completes the locked perk unlock path, resets to the My Cars grid baseline, and terminates cleanly.

For multi-car unlock validation, success means Auto3 processes the requested count within the validated limit, follows A-start traversal correctly, resets after each car, and terminates cleanly without stuck inputs.

## Stop Immediately If

Press F8 immediately if:

* the wrong car is selected.
* the wrong grid position is reached.
* the wrong menu opens.
* FH6 loses focus.
* Car Mastery does not open as expected.
* an unexpected skill-tree path occurs.
* the game loads slower than expected and inputs appear desynchronized.
* the operator is unsure whether the command is still aligned.
* skill point spending risk becomes unclear.

After stopping, verify FH6 focus, menu state, held inputs, car position, and baseline before running any Auto3 command again.

## Common Failure Modes

Incorrect My Cars baseline state:

Likely cause: Auto3 was started from the wrong garage/menu position or the selected car was not the expected A1 baseline.

Corrective action: Stop with F8, manually return to the validated My Cars baseline, and restart only after confirming row A and active/seated A1 assumptions.

Wrong sorting or grid position:

Likely cause: My Cars sorting or selected position does not match the validated traversal assumptions.

Corrective action: Stop with F8 and manually restore the expected My Cars baseline before retrying.

Focus loss:

Likely cause: FH6 was not focused or another window received keyboard input.

Corrective action: Stop the command if needed, refocus FH6, and only restart from a known safe baseline.

Timing drift or loading variance:

Likely cause: FH6 menu/loading behavior took longer than the conservative profile timing expected.

Corrective action: Stop with F8. Do not immediately rerun from the drifted state. Restore baseline first.

Grid traversal desync:

Likely cause: movement from A1 -> B1, B1 -> C1, or C1 -> A2 did not land on the expected target.

Corrective action: Stop with F8 and manually inspect the selected car. Do not continue if the selected target is uncertain.

Missing skill points:

Likely cause: the target car does not have enough points for the locked unlock path.

Corrective action: Stop or let the command finish only if it remains safe. Recheck the car state and skill-point availability before another unlock run.

Unexpected FH6 menu/layout change:

Likely cause: FH6 state, menu layout, or game flow differs from the validated assumptions.

Corrective action: Stop with F8 and treat the run as invalid. Do not adapt manually mid-run.

Reset-to-grid failure:

Likely cause: the return/reset sequence did not restore the My Cars grid baseline.

Corrective action: Stop with F8, restore the grid baseline manually, and avoid multi-car commands until the cause is understood.

## Current Boundaries

Auto3 current boundaries:

* hard max: 4 cars.
* start row: A.
* validated traversal: A1 -> B1 -> C1 -> A2.
* guarded/manual/test-only real-input commands.
* no production Auto3 command.
* no unattended mode.
* no Auto4 or remove-car behavior.
* no expansion beyond validated traversal without a future milestone.
* profile-driven conservative timing.
* confirmation flags required for real-input and unlock paths.

These boundaries are frozen unless a future milestone explicitly changes them.

## Safety Notes

Auto3 unlock commands can spend skill points. Use test-mode commands before unlock commands whenever baseline, menu state, or traversal alignment is uncertain.

Auto3 must be supervised. F8 stop is available in guarded real-input commands, but it is not a substitute for correct FH6 baseline setup or operator attention.

Do not increase car count, start from row B/C, add Auto4 behavior, or treat Auto3 as unattended production automation without a future validated milestone. The current philosophy remains trust-first, safety-first, and reliability before speed.
