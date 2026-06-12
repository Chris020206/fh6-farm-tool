# Auto3 Multi-Car Unlock Design

This document records the implemented and validated Auto3 multi-car unlock
behavior after guarded 4-car real-input validation.

Auto3 multi-car unlock remains dangerous/manual/test-only. It is not a
production command and is not wired into `main.py`.

## Implemented Boundary

The current implemented boundary is:

- profile-driven sequence generation
- finite car count only
- guarded real-input command only
- hard max of 4 cars
- start row assumption: `A`
- validated traversal: `A1 -> B1 -> C1 -> A2`
- no Auto4/delete behavior

The guarded real-input command is:

```powershell
python -B -m automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test --cars 4 --confirm-real-input --confirm-unlock
```

## Validated Multi-Car Unlock Flow

For the current validated `A`-start path, Auto3 processes cars in this order:

```text
A1 -> B1 -> C1 -> A2
```

For car index `0` / `A1`, Auto3 uses the first-car exception path:

1. Sort setup.
2. First-car Car Mastery navigation.
3. Locked perk unlock path.
4. Return/reset to the My Cars grid baseline.

For later cars, Auto3 uses the grid movement planner:

- `A1 -> B1`: `down`
- `B1 -> C1`: `down`
- `C1 -> A2`: `right`, `up`, `up`

After moving to a later car, Auto3:

1. Gets into the currently hovered car.
2. Waits for the post-get-in transition.
3. Runs the post-get-in recovery path.
4. Runs the locked perk unlock path.
5. Returns/resets to the My Cars grid baseline.

## Later-Car Recovery Path

The later-car post-get-in recovery path is:

```text
wait 12s
esc
up x6
down
enter
down x7
enter
```

This path is required after the new-car transition/cutscene before the locked
perk unlock path can safely run.

## Locked Perk Unlock Path

All multi-car unlock actions use the existing locked perk unlock path:

```text
enter
right
enter
up
enter
up
enter
up
enter
left
enter
```

`skill_tree_key_delay` applies only inside this locked perk unlock path.

## Safety Rules

Auto3 multi-car unlock must preserve these rules:

- finite `car_count` only
- hard max remains 4 cars
- no infinite loop
- no Auto4 behavior
- no delete/remove-car behavior
- no production command
- real-input unlock requires `--confirm-real-input`
- real-input unlock requires `--confirm-unlock`
- F8 stop remains available in guarded real-input paths
- `main.py` remains safe

## Known Boundaries

The current validated behavior does not include:

- counts greater than 4
- start rows other than `A`
- production/unattended Auto3 execution
- UI/dashboard control
- Auto4/remove-car cleanup
- timing optimization

## Current Recommendation

Freeze Auto3 core logic temporarily.

Do not increase the car limit, add start-row flexibility, or promote a
production Auto3 command until MVP hardening and review are complete.
