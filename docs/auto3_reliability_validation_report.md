# Auto3 Reliability Validation Report

This report records the current Auto3 Skill Tree Automation validation status.
Auto3 is in controlled/manual validation. Auto3 one-car logic and guarded
multi-car unlock logic have been validated through in-memory execution and
guarded real-input testing within the current Controlled MVP boundaries.

Current hard limits:

- max cars: `4`
- start row: `A`
- validated traversal: `A1 -> B1 -> C1 -> A2`
- real-input Auto3 remains dangerous/manual/test-only
- no unattended or unguarded Auto3 command exists
- no unattended Auto3 mode exists
- no Auto4/remove-car behavior exists

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
- Multi-car test-mode real-input traversal validation across 4 cars.
- Multi-car guarded real-input unlock validation across 4 cars.

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
- Later-car unlock paths require a validated 12-second post-get-in recovery
  delay before menu recovery/navigation.

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
- Multi-car grid traversal is implemented and validated within the guarded
  4-car boundary:
  - `A1 -> B1`
  - `B1 -> C1`
  - `C1 -> A2`
- Multi-car movement uses the validated grid rules:
  - `A1 -> B1`: `down`
  - `B1 -> C1`: `down`
  - `C1 -> A2`: `right`, `up`, `up`
- Multi-car unlock validation works through the guarded dangerous/manual harness
  for up to 4 cars.
- Later-car unlock recovery works with:
  - 12-second wait
  - `esc`
  - `up` x6
  - `down`
  - `enter`
  - `down` x7
  - `enter`
- Reset-to-grid baseline works between validated car visits.
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
- `wait_after_get_in_next_car`: `12.0`
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
- The multi-car unlock harness may spend skill points when confirmed.
- Multi-car unlock validation is limited to 4 cars.
- Start row `A` is assumed for current validated traversal.
- Auto3 does not include Auto4/remove-car behavior.

## Known Limitations

- No Auto3 production command exists yet.
- Auto3 real-input unlock remains dangerous/manual/test-only.
- Multi-car unlock validation is limited to 4 cars.
- Start rows B and C are not supported in the current validated flow.
- Traversal beyond `A1 -> B1 -> C1 -> A2` is future work.
- Conservative timings are intentionally not optimized.
- The user must start from the correct FH6 baseline.
- Skill points can be spent in guarded unlock harnesses when confirmed.

## Postponed Work

- Auto3 production command.
- Unattended Auto3 mode.
- Auto3 traversal beyond the 4-car validated boundary.
- Start-row flexibility for B/C start rows.
- Larger-count guarded validation.
- Timing optimization.
- Auto4 car removal.

## Current Recommendation

Auto3 one-car and guarded 4-car multi-car unlock logic are ready for Controlled
MVP developer/manual use within the documented boundaries. Keep Auto3 frozen at
the current hard limits while MVP hardening continues. Do not increase the car
limit, add unattended behavior, add a production command, or add Auto4 behavior
without a future explicit milestone and validation path.
