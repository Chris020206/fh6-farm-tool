# Auto2 Operator Runbook

## Purpose

Auto2 automates the FH6 buy-car menu flow.

It is used for controlled validation of Autoshow navigation and exactly one
guarded purchase/reset cycle. Auto2 is controlled/manual only. It is not a
production multi-cycle purchasing system.

Auto2 has spending risk. The purchase command can spend credits and must be
treated more strictly than non-spending automation.

---

## Required FH6 Baseline State

Before running Auto2, FH6 must be in the expected Autoshow/menu baseline for
the official Auto2 profile.

Required baseline:

- FH6 is focused and ready to receive keyboard input.
- The operator is present and watching the run.
- The Autoshow/menu state matches the validated navigation path.
- The official profile navigation assumptions are valid:
  - `manufacturer_down_presses`: 18
  - `car_right_presses`: 3
- Keyboard controls match the Auto2 profile keys.
- Mouse/cursor activity should not interfere with menu selection.
- F8 is ready before execution starts.

Additional purchase-command requirements:

- Sufficient credits are available.
- The operator understands the purchase command can spend credits.
- The operator has validated navigation with test mode when there is any
  uncertainty.

Do not run Auto2 from an unknown FH6 menu state. Do not run purchase validation
if the selected manufacturer/car path is uncertain.

---

## Commands To Run

### Test-Mode Navigation Validation

```powershell
python -B -m automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test 1 --confirm-real-input
```

This command:

- sends real keyboard input
- does not include purchase actions
- validates menu navigation
- supports F8 stop
- can run a finite number of test-mode cycles

Optional fast timing validation:

```powershell
python -B -m automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test 1 --confirm-real-input --fast
```

Optional profile usage:

```powershell
python -B -m automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test 1 --confirm-real-input --profile auto2_safe_slow
```

Use test mode before purchase validation if the baseline, menu timing, or
profile selection is uncertain.

### One-Car Purchase Validation

```powershell
python -B -m automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test 1 --confirm-real-input --confirm-purchase
```

This command:

- sends real keyboard input
- will spend credits
- runs exactly one purchase/reset cycle
- requires `--confirm-real-input`
- requires `--confirm-purchase`
- supports F8 stop
- is not production multi-cycle mode

Optional profile usage:

```powershell
python -B -m automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test 1 --confirm-real-input --confirm-purchase --profile auto2_safe_slow
```

---

## Expected Behavior

### Test Mode

Normal test-mode behavior:

- startup delay gives the operator time to focus FH6
- menu navigation starts from the expected Autoshow/menu baseline
- manufacturer navigation uses the profile count
- car navigation uses the profile count
- purchase actions are excluded
- command completes without spending credits
- input cleanup runs at the end

Test mode is behaving normally if the menu follows the expected path and no
purchase confirmation path is triggered.

### One-Car Purchase

Normal one-car purchase behavior:

- menu navigation starts from the expected Autoshow/menu baseline
- manufacturer and car navigation follow the official profile counts
- purchase key is pressed after the validated car-selection delay
- purchase confirmation path occurs
- credits may be spent
- command performs exactly one cycle
- post-purchase wait occurs
- Esc and final confirm return the menu to the expected baseline
- input cleanup runs at the end

Purchase validation is behaving normally if one intended car is purchased and
the menu resets to the validated baseline afterward.

---

## Success Condition

### Test Mode

Successful test-mode operation:

- completes the requested finite test-mode cycle count
- never triggers purchase actions
- follows the expected manufacturer/car navigation path
- reports a clear final status
- releases tracked input

### One-Car Purchase Validation

Successful one-car purchase validation:

- completes exactly one purchase/reset cycle
- spends credits only for the intended purchase
- returns to the expected Autoshow baseline
- reports a clear final status
- releases tracked input

---

## Stop Immediately If

Press `F8` immediately if:

- the wrong manufacturer opens
- the wrong menu opens
- the wrong car appears selected
- an unexpected purchase confirmation appears during test mode
- FH6 loses focus
- menu navigation desynchronizes
- the operator is unsure whether the command is still aligned
- spending risk becomes unclear
- any input appears to affect the wrong FH6 state

After pressing F8, keep watching until cleanup completes. Do not rerun until
the FH6 baseline and selected profile are verified.

---

## Common Failure Modes

Wrong Autoshow/menu starting state

- Likely cause: Auto2 was launched from a menu state that does not match the
  validated baseline.
- Corrective action: press F8, return FH6 to the expected Autoshow/menu
  baseline, and rerun test mode before any purchase command.

Focus loss

- Likely cause: FH6 was not focused when input began.
- Corrective action: press F8 if input went to the wrong window or wrong FH6
  state. Refocus FH6 and verify baseline before retrying.

Menu timing drift

- Likely cause: FH6 menu/loading timing is slower than the selected profile.
- Corrective action: press F8, use conservative/custom profile timing only
  after profile backup and validation, and rerun test mode first.

Wrong navigation count assumption

- Likely cause: Autoshow ordering, manufacturer position, or car position does
  not match the official profile assumptions.
- Corrective action: press F8, verify `manufacturer_down_presses` and
  `car_right_presses`, and do not run purchase validation until test mode
  confirms the path.

Insufficient credits

- Likely cause: the account does not have enough credits for the intended
  purchase.
- Corrective action: stop the command if possible, restore the baseline, and do
  not rerun purchase validation until credits and expected cost are understood.

Unexpected FH6 menu/layout change

- Likely cause: FH6 state, sorting, event state, or menu layout differs from
  the validated path.
- Corrective action: press F8, document the observed state, and do not continue
  purchase validation until the path is revalidated in test mode.

---

## Current Boundaries

Auto2 current boundaries:

- guarded/manual only
- real-input commands require confirmation flags
- one-car purchase validation only
- no promoted production multi-cycle purchase mode
- no unattended mode
- no startup automation
- profile-driven conservative timing
- official profile used by default
- custom profile timing edits only through the profile tooling

Auto2 is Controlled MVP behavior, not broad production release behavior.

---

## Safety Notes

Auto2 can spend credits.

Use test mode before purchase validation whenever there is uncertainty about
FH6 state, profile selection, timing, or menu navigation.

The safety model is trust-first:

- keep F8 ready
- supervise the command
- require explicit confirmation
- keep execution finite
- stop on uncertainty
- preserve conservative profile timings

Do not run Auto2 purchase validation unattended. Do not promote Auto2 to
multi-cycle purchasing without a separate milestone, validation plan, and
review.
