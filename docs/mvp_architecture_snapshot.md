# MVP Architecture Snapshot

This snapshot freezes the current FH6 Farm Tool architecture after guarded
Auto3 4-car real-input unlock validation.

The project is in controlled/manual validation and MVP hardening. It is not
ready for broad production release.

## Current System Architecture

The project is organized around separated modules:

- `automation/` contains Auto1, Auto2, and Auto3 automation-specific sequence
  and runner modules.
- `core/` contains shared runtime systems:
  - action model
  - timing system
  - input controller and input backends
  - stop manager
  - sequence runner
  - state machine
- `profiles/` contains official/custom JSON profiles, validation, selection,
  backup/restore, summary, and safe custom timing tools.
- `app/commands/` contains shared manual command helpers.
- `app_logging/` contains centralized logging.
- `docs/` contains scope, validation, command, and engineering documentation.
- `main.py` loads configuration, logs startup, and exits safely.

Auto1, Auto2, and Auto3 form the MVP core loop:

1. Auto1 Race Automation earns rewards.
2. Auto2 Buy Car Automation buys target cars.
3. Auto3 Skill Tree Automation unlocks skill-tree rewards.

Auto4 Remove Cars is not part of the current controlled MVP hardening scope.
Per M11 strategic doctrine, it remains a conditional pre-launch candidate only
if it can be made strongly guarded, clearly explained, and safe enough to
protect trust.

## Auto1 Status

Auto1 is the most mature real-input automation.

Current status:

- profile-driven
- finite-cycle controlled manual command exists
- F8 stop supported
- official and custom profiles supported
- startup delay supported
- conservative timings accepted
- real-input validation documented

Primary command:

```powershell
python -B -m automation.auto1_race.run_auto1 <cycles> --confirm
```

Auto1 remains manual/guarded. It is not wired into `main.py`.

## Auto2 Status

Auto2 supports safe validation and guarded one-car purchase testing.

Current status:

- profile-driven
- in-memory CLI validation exists
- real-input test-mode navigation exists
- one-car purchase harness exists
- full purchase/reset flow is documented
- F8 stop supported in guarded real-input commands
- production multi-cycle purchase command is not promoted

Important commands:

```powershell
python -B -m automation.auto2_buy_car.auto2_cli_test 1 --fast --test-mode
python -B -m automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test 1 --confirm-real-input
python -B -m automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test 1 --confirm-real-input --confirm-purchase
```

Auto2 remains controlled/manual and should not be converted into unattended
multi-cycle purchase behavior without a separate review.

## Auto3 Status

Auto3 completes the MVP core loop and now includes guarded/manual multi-car
unlock validation.

Current status:

- profile-driven
- in-memory test and full modes exist
- guarded real-input test-mode navigation exists
- guarded one-car unlock harness exists
- guarded multi-car unlock harness exists
- traversal is implemented for the validated start-row `A` path
- guarded real-input unlock is validated through 4 cars
- validated traversal: `A1 -> B1 -> C1 -> A2`
- current real-input hard max is 4 cars
- current start-row assumption is row `A`
- no-unlock test modes stop before perk unlock
- F8 stop supported in guarded real-input commands
- no production Auto3 command exists

Important commands:

```powershell
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode first-car-test
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode normal-next-car-test
python -B -m automation.auto3_skill_tree.auto3_cli_test --mode multi-car-unlock --cars 4
python -B -m automation.auto3_skill_tree.dangerous_auto3_test_mode_real_input_test --mode first-car-test --confirm-real-input
python -B -m automation.auto3_skill_tree.dangerous_auto3_one_car_unlock_test --mode first-car --confirm-real-input --confirm-unlock
python -B -m automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test --cars 4 --confirm-real-input --confirm-unlock
```

Auto3 remains controlled/manual only. Counts greater than 4, flexible
`--start-row` behavior, and production/unattended operation are postponed.

## Profile System Status

Profiles are local JSON files.

Current model:

- official profiles live in `profiles/official/`
- custom profiles live in `profiles/custom/`
- official profiles are protected from timing edits
- custom profiles can be created from official profiles
- custom timing values can be edited after validation
- profile summary/filtering is read-only
- backup/restore commands exist
- automation commands can select profiles where supported

Current profile commands:

```powershell
python -B -m profiles.profile_summary
python -B -m profiles.profile_summary --type auto3_skill_tree
python -B -m profiles.profile_backup
python -B -m profiles.profile_restore <backup_timestamp> --confirm-restore
python -B -m profiles.profile_create_custom --source auto1_race_default --name auto1_safe_slow
python -B -m profiles.profile_edit_timing --profile auto1_safe_slow --timing startup_delay --value 7.0
```

Profile key editing, navigation-count editing, and import/export are
postponed. Profile UI editing is not part of the current controlled/manual MVP
surface, but UI work is required before public paid launch under the M11
strategic doctrine.

## Command Framework Status

Shared command helpers live in `app/commands/`.

They centralize:

- confirmation checks
- cycle-count validation
- command intro formatting
- refusal output
- run summary formatting

Dangerous commands still own their specific execution wiring. Execution logic
must remain in runners/shared systems, not in command wrappers.

## Safety Boundaries

Current safety boundaries:

- `main.py` does not run automation.
- Real input requires explicit confirmation flags.
- F8 stop is available in guarded real-input commands.
- RealKeyboardBackend remains isolated inside `core/input/`.
- Input goes through `InputController`.
- Waiting goes through `TimingSystem`.
- Stop state goes through `StopManager`.
- Automation execution goes through `SequenceRunner`.
- Refusal-path tests cover dangerous commands without confirmation flags.

Commands that may spend credits or skill points must stay guarded.

## Validated Real-Input Behavior

Validated behavior includes:

- Auto1 race cycle execution and F8 stop.
- Auto2 test-mode navigation.
- Auto2 one-car purchase/reset flow.
- Auto3 first-car and normal-next-car test-mode navigation.
- Auto3 one-car unlock path.
- Auto3 guarded 4-car unlock path:
  - `A1 -> B1`
  - `B1 -> C1`
  - `C1 -> A2`
- F8 stop behavior during guarded real-input testing.
- Cleanup behavior through shared input release paths.

The validation boundary is manual and controlled. It does not imply broad
production readiness.

## Conservative Timing Strategy

Auto1, Auto2, and Auto3 use conservative profile-driven timings.

This is accepted intentionally:

- slower timing improves reliability
- FH6 menu/loading behavior can vary
- user hardware can vary
- profile-driven timing supports future tuning

Timing optimization is postponed. Do not replace validated conservative values
with faster defaults casually.

## Postponed Systems

Systems outside the current controlled/manual MVP surface include:

- Auto4 Remove Cars, except as a future conditional pre-launch candidate after
  a dedicated safety milestone.
- UI/dashboard for current CLI/manual operation. A restrained premium desktop
  UI is required before public paid launch.
- Packaging/installer.
- F7 start hotkey.
- Pause/resume.
- Auto3 production command.
- Auto3 counts greater than 4.
- Auto3 flexible start-row support.
- Auto2 production multi-cycle purchase command.
- Profile key editing.
- Profile navigation-count editing.
- Timing optimization.
- Import/export and profile marketplace concepts.

## Areas Not To Casually Change

The following areas should not be changed without a clear milestone and review:

- `main.py` startup safety.
- RealKeyboardBackend isolation.
- Confirmation requirements on dangerous commands.
- F8 stop registration boundaries.
- Official profile protection.
- SequenceRunner generic behavior.
- TimingSystem cancellation behavior.
- InputController held-key cleanup behavior.
- Auto1, Auto2, and Auto3 validated profile timings.
- Auto3 first-car and normal-next-car path differences.
- Auto3 later-car post-get-in recovery path.
- Auto3 guarded 4-car hard max.
- Auto3 start-row `A` assumption.
- Auto3 no-unlock test-mode safety.
- Auto2 one-car purchase cycle limit.

## Next Design Target

The next design target is MVP hardening around the validated command surface.

Do not expand Auto3 counts above 4, add start-row flexibility, or promote an
Auto3 production command without a separate milestone and review.

In parallel strategic planning, preserve the M11 direction that public paid
launch requires a restrained premium desktop UI. The PySide6 desktop UI
foundation now exists, but it remains an operator/developer hardening surface
until a future milestone validates it for public launch.
