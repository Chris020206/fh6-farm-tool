# Auto3 Multi-Car Unlock Validation Report

This report records the current guarded real-input validation state for Auto3
multi-car unlock behavior.

## Tested Scenario

- Command: `dangerous_auto3_multi_car_unlock_test`
- Mode: `multi-car-unlock-test`
- Cars: `4`
- Profile: `auto3_skill_tree_default`
- Final status: `completed`

## Confirmed Traversal

The guarded real-input 4-car unlock validation confirmed this traversal:

```text
A1 -> B1 -> C1 -> A2
```

Confirmed movement logic:

- `A1 -> B1`: `down`
- `B1 -> C1`: `down`
- `C1 -> A2`: `right`, `up`, `up`

## Confirmed Unlock Behavior

The 4-car validation confirmed:

- A1 first-car exception path works.
- Later-car get-in flow works.
- 12-second post-get-in recovery delay works.
- Later-car post-get-in recovery path works:

```text
wait 12s
esc
up x6
down
enter
down x7
enter
```

- Locked perk unlock path works.
- Reset-to-grid baseline works after each car.
- Final sequence terminates cleanly after the fourth car.

## Safety Behavior

The validated path preserved the current safety boundaries:

- Uses a guarded real-input command.
- Requires `--confirm-real-input`.
- Requires `--confirm-unlock`.
- F8 stop is available.
- Finite hard max remains in place.
- No Auto4 behavior exists.
- No delete/remove-car behavior exists.

## Remaining Limitations

Current limitations:

- Unlock mode has only been validated through 4 cars.
- Higher car counts are not approved yet.
- Timing optimization remains postponed.
- The start row A assumption remains in effect.
- The real-input unlock count limit remains conservative.
- Auto4/remove-car behavior remains explicitly excluded.

## Current Recommendation

Freeze Auto3 core logic temporarily.

Do not increase the real-input unlock car limit yet. The next step should be
MVP hardening and review before adding new capability or expanding validation
counts.
