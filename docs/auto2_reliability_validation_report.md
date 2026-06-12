# Auto2 Reliability Validation Report

## Summary

Auto2 Buy Car automation has been validated through controlled in-memory tests,
guarded real-input test mode, and a guarded one-car purchase test. The current
implementation remains profile-driven and runs through the shared systems:
SequenceRunner, TimingSystem, InputController, StopManager, and the isolated
RealKeyboardBackend.

This report records the validated behavior, current limitations, and accepted
timing decisions before moving to the next phase.

## Tested Scenarios

- Auto2 test mode real-input validation using the dangerous/manual test-mode
  harness.
- Navigation validation without purchase actions.
- Subaru manufacturer selection using 18 down-key presses from the expected
  Autoshow baseline.
- Car selection navigation using 3 right-key presses.
- One-car purchase validation using the guarded purchase-test harness.
- Baseline reset validation through the post-purchase Esc and final Enter flow.
- F8 stop validation through StopManager.
- Stop during sequence validation, including cleanup through InputController.

## Confirmed Working Behavior

- Auto2 navigation is profile-driven through
  `profiles/official/auto2_buy_car_default.json`.
- `menu_key_delay` is applied between menu navigation key presses.
- The full purchase flow executes through shared actions and SequenceRunner.
- The reset flow returns the menu to the expected Autoshow baseline for the
  next cycle.
- Cleanup behavior releases tracked input through InputController.
- StopManager integration is active for guarded real-input harnesses.
- SequenceRunner remains the only execution path for Auto2 action lists.
- RealKeyboardBackend remains isolated in `core/input/`.
- F8 stop requests stop through StopManager and releases input safely through
  existing cleanup paths.

## Official Full Sequence Flow

The current intended full Auto2 flow is:

1. Wait `startup_delay`.
2. Press `back_key` (`backspace`).
3. Wait `menu_key_delay`.
4. Press `down_key` (`down`) `manufacturer_down_presses` times.
5. Wait `menu_key_delay` between each down press.
6. Press `confirm_key` (`enter`) to select the manufacturer.
7. Wait `menu_key_delay`.
8. Press `right_key` (`right`) `car_right_presses` times.
9. Wait `menu_key_delay` between each right press.
10. Press `confirm_key` (`enter`) to select the car.
11. Wait `menu_key_delay`.
12. Wait `wait_after_menu_confirm`.
13. Wait `wait_after_car_selection`.
14. Press `purchase_key` (`y`).
15. Wait `menu_key_delay`.
16. Press `confirm_key` (`enter`).
17. Wait `menu_key_delay`.
18. Press `confirm_key` (`enter`).
19. Wait `menu_key_delay`.
20. Press `confirm_key` (`enter`).
21. Wait `wait_after_purchase_confirm`.
22. Press `escape_key` (`esc`).
23. Wait `menu_key_delay`.
24. Press `confirm_key` (`enter`).
25. Wait `post_cycle_delay`.

Current official profile values:

- `manufacturer_down_presses`: 18
- `car_right_presses`: 3
- `startup_delay`: 1.0
- `menu_key_delay`: 1.5
- `wait_after_menu_confirm`: 1.0
- `wait_after_car_selection`: 3.0
- `wait_after_purchase_confirm`: 13.0
- `post_cycle_delay`: 1.0

## Known Limitations

- Timings are intentionally conservative and may be slower than necessary.
- Profile timing optimization is postponed until profile settings and profile
  editing are tested.
- `estimated_cost_per_car` is currently not finalized.
- There is no multi-cycle purchase production mode.
- There is no UI or profile editor.
- Dangerous real-input harnesses remain manual validation tools, not production
  automation.

## Accepted Design Decision

Too slow is safer than too fast.

Auto2 timing favors reliability over speed because FH6 menu transitions,
loading states, and input acceptance timing can vary. User hardware variation
also matters: a timing profile that works on one system may fail on a slower
system or under temporary load.

The current reliability-first approach accepts conservative waits as an
explicit limitation. Future optimization should remain profile-driven so timing
can be tuned per user and per machine without changing automation code.

## Safety Boundaries

- Dangerous Auto2 harnesses are manual only.
- Normal startup remains safe and does not run Auto2.
- Real-input harnesses require explicit confirmation flags.
- The one-car purchase harness requires both `--confirm-real-input` and
  `--confirm-purchase`.
- The one-car purchase harness allows exactly one cycle.
- F8 stop is available in guarded real-input harnesses.
- RealKeyboardBackend is not used by default and remains isolated behind
  InputController.

## Recommendation

Auto2 is ready to proceed beyond one-car purchase validation only with the
existing safety boundaries preserved. Multi-cycle purchase behavior should not
be promoted until it receives its own guarded milestone, validation plan, and
reliability review.
