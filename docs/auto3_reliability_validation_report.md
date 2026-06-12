# Auto3 Reliability Validation Report

This report records the current Auto3 Skill Tree Automation validation status.
Auto3 is in controlled/manual validation. Auto3 one-car logic has been
validated through in-memory execution and guarded real-input testing. Auto3
multi-car logic is not implemented yet.

## Tested Scenarios

- In-memory Auto3 modes:
  - `first-car-test`
  - `normal-next-car-test`
  - `full-first-car`
  - `full-normal-next-car`
- First-car-test real-input navigation.
- Normal-next-car-test real-input navigation.
- F8 stop validation during Auto3 real-input testing.
- One-car unlock validation through the guarded first-car unlock harness.

## Corrections From Real-Input Testing

Real-input testing found several FH6-specific navigation details that were
corrected before locking the current Auto3 behavior.

- `down_to_upgrades` was corrected to `1`.
- `down_to_car_mastery` was corrected to `7`.
- The normal-next-car path must not use `esc` before navigating to Upgrades &
  Tuning.
- The normal-next-car real-input test must include sort setup before the
  get-in-next-car sequence.
- The skill-tree unlock path requires a dedicated `1.5` second key delay through
  `skill_tree_key_delay`.

## Confirmed Working Behavior

- Sort setup is profile-driven and follows:
  - `x`
  - `down` x6
  - `enter`
- First-car exception path works from the seated A1 baseline.
- Normal-next-car get-in path works as:
  - `down`
  - `enter`
  - `enter`
- Car Mastery navigation uses the corrected counts:
  - first-car path: `esc`, `down`, `enter`, `down` x7, `enter`
  - normal-next-car path: `down`, `enter`, `down` x7, `enter`
- No-unlock test modes stop before the first perk unlock confirm.
- One-car unlock path is available through the guarded first-car unlock harness.
- F8 stop works during guarded Auto3 real-input testing.
- Cleanup behavior releases held input through the shared cleanup path.

## Current Official Auto3 Profile Values

Profile: `profiles/official/auto3_skill_tree_default.json`

Keys:

- `sort_menu_key`: `x`
- `confirm_key`: `enter`
- `enter_key`: `enter`
- `escape_key`: `esc`
- `down_key`: `down`
- `up_key`: `up`
- `left_key`: `left`
- `right_key`: `right`
- `back_key`: `backspace`

Navigation counts:

- `sort_down_presses`: `6`
- `down_to_upgrades`: `1`
- `down_to_car_mastery`: `7`
- `return_up_to_my_cars`: `7`

Timings:

- `startup_delay`: `1.0`
- `menu_key_delay`: `1.0`
- `skill_tree_key_delay`: `1.5`
- `wait_after_get_in`: `3.0`
- `wait_after_menu_open`: `1.0`
- `wait_after_unlock`: `2.0`
- `post_cycle_delay`: `1.0`

## Safety Boundaries

- Real-input Auto3 commands are dangerous/manual/test-only.
- Real-input Auto3 commands require explicit confirmation flags.
- F8 stop is available in guarded real-input Auto3 commands.
- Normal `main.py` startup does not run Auto3 or send keyboard input.
- Test-mode real-input paths exclude perk unlock actions.
- The one-car unlock harness may spend skill points when confirmed.

## Known Limitations

- No grid traversal loop exists yet.
- No multi-car Auto3 run exists yet.
- No Auto3 production command exists yet.
- Conservative timings are intentionally not optimized.
- The user must start from the correct FH6 baseline.
- Skill points can be spent in the unlock harness when confirmed.

## Postponed Work

- Grid traversal implementation.
- C-row to next-column transition validation.
- Multi-car looping.
- Production Auto3 command.
- Auto4 car removal.

## Current Recommendation

Auto3 one-car logic is ready for continued guarded validation and MVP
hardening. Auto3 multi-car logic is not ready until grid traversal is
implemented, validated in test mode, and proven safe before any real-input
unlock loop is considered.
