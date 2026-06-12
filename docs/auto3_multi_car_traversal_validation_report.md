# Auto3 Multi-Car Traversal Validation Report

This report records the guarded real-input Auto3 multi-car test-mode traversal
validation.

This validation covers traversal and Car Mastery navigation only. It does not
validate a multi-car unlock loop.

## Tested Scenario

- Scenario: Auto3 multi-car test-mode real-input traversal.
- Cars: `4`.
- Profile: `auto3_skill_tree_default`.
- Perk unlock actions included: no.
- Final status: `completed`.
- Total action count: `265`.

## Confirmed Traversal

The guarded real-input test confirmed traversal through:

1. `A1 -> B1`
2. `B1 -> C1`
3. `C1 -> A2`

## Confirmed Movement Logic

The confirmed movement logic was:

- `A1 -> B1`: `down`
- `B1 -> C1`: `down`
- `C1 -> A2`: `right`, `up`, `up`

The duplicate-down issue was corrected before this validation. Grid movement
selects the target car, and the get-in step then presses `enter`, `enter` for
the currently hovered car.

## Confirmed Safety Behavior

- No skill points were spent.
- Test mode did not include perk unlock actions.
- Reset-to-grid baseline worked between cars.
- F8 stop has been validated separately.
- The real-input command remains guarded by `--confirm-real-input`.
- The command remains dangerous/manual/test-only.

## Known Limitations

- Test mode only.
- No multi-car unlock loop exists yet.
- No production Auto3 command exists yet.
- The max real-input test limit remains conservative.
- Timing optimization is postponed.

## Next Recommended Step

Design the in-memory multi-car unlock sequence before any real-input unlock
loop is considered.

That design should preserve:

- finite car counts
- reset-to-grid behavior between cars
- F8 stop in guarded real-input paths
- no Auto4 behavior
- no production command until in-memory unlock sequencing is reviewed

## Current Recommendation

Auto3 multi-car traversal is validated for guarded real-input test mode across
four cars. Unlock behavior remains postponed and must be designed and validated
separately.
