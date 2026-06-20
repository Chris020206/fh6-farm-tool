# Auto3 Grid Traversal Design

This document defines the Auto3 multi-car grid traversal model. It began as a
pre-implementation design spec and now also records the current implemented and
validated boundary.

Current validated boundary:

- max cars: `4`
- start row: `A`
- validated traversal: `A1 -> B1 -> C1 -> A2`
- guarded/manual real-input validation exists
- no unattended or unguarded Auto3 command exists
- no unattended Auto3 mode exists

## Grid Model

The FH6 My Cars grid for the current Auto3 plan is modeled as:

- 3 fixed rows: `A`, `B`, `C`
- variable number of columns

Traversal moves down each column before moving to the next column:

```text
A1 -> B1 -> C1 -> A2 -> B2 -> C2 -> A3 -> B3 -> C3
```

Rows:

- `A` = row index `0`
- `B` = row index `1`
- `C` = row index `2`

Columns:

- `1` = column index `0`
- `2` = column index `1`
- `3` = column index `2`
- and so on

## Position Model

Auto3 should use a simple zero-based position model:

- row index: `0`, `1`, `2`
- column index: `0`, `1`, `2`, ...
- linear car index starts at `0`

Examples:

| Linear index | Grid position | Row index | Column index |
| --- | --- | --- | --- |
| `0` | `A1` | `0` | `0` |
| `1` | `B1` | `1` | `0` |
| `2` | `C1` | `2` | `0` |
| `3` | `A2` | `0` | `1` |
| `4` | `B2` | `1` | `1` |
| `5` | `C2` | `2` | `1` |

## Index-To-Position Mapping

For a zero-based linear car index:

```text
row = index % 3
column = index // 3
```

Examples:

- index `0`: row `0`, column `0` = `A1`
- index `1`: row `1`, column `0` = `B1`
- index `2`: row `2`, column `0` = `C1`
- index `3`: row `0`, column `1` = `A2`

## Movement Rules

Movement from the current target to the next target follows the row position:

- from row `0` to row `1`: press `down`
- from row `1` to row `2`: press `down`
- from row `2` to next column row `0`: press `right`, then `up`, then `up`

The row `2` to next-column transition must be treated as a separate movement
sequence, not as a normal down press.

The likely column transition is:

```text
right
up
up
```

This behavior has been validated for `C1 -> A2` within the current 4-car
guarded traversal. Additional column transitions beyond the current boundary
must still be validated before real-input use.

## MVP Start-Row Assumption

Current MVP Auto3 traversal assumes the user starts on row `A`.

The validated traversal path is:

```text
A1 -> B1 -> C1 -> A2
```

Starting on row `B` or row `C` would require adjusted traversal logic because
the first movement and column-transition assumptions would change.

`--start-row` is a future enhancement, not current MVP scope. It is
intentionally postponed to avoid expanding traversal complexity beyond the
validated row-`A` unlock boundary.

## First-Car Exception

Index `0` / `A1` is already seated at the locked Auto3 baseline.

For index `0`:

- do not move to another grid cell
- do not run the get-in-next-car sequence
- run the first-car exception unlock path
- return and resort afterward

## Normal-Car Behavior

For every target after index `0`, Auto3 should:

1. Move from the current grid position to the target car.
2. Get in the selected car.
3. Run the unlock sequence.
4. Return and resort to the known baseline.

Normal same-column movement uses the existing next-car get-in path after moving
down. The `C1 -> A2` column transition is validated; additional transitions
remain future validation work.

## Test-Mode Baseline Reset Requirement

Every car visit in multi-car test mode must end by returning to the My Cars grid
baseline before moving to the next car.

This is required because test mode navigates to Car Mastery and stops before
unlocking. Grid movement does not make sense while the user is still inside Car
Mastery. Movement such as `down`, `right`, or `up` is only valid from the My
Cars grid baseline.

The current unsafe assumption is:

```text
first-car test path
grid movement
normal-next-car test path
```

That is not safe for real-input traversal because the first-car test path ends
inside Car Mastery.

The required safe structure is:

```text
navigate to Car Mastery
stop before unlock
return/reset to My Cars grid
move to next target
navigate to Car Mastery
stop before unlock
return/reset to My Cars grid
repeat
```

## Expected Reset Sequence

The expected reset sequence from Car Mastery back to the My Cars grid is based
on the existing return/reset concept:

```text
esc
esc
up x7
enter
x
down x6
enter
```

This should return to:

- the sorted Recently Added My Cars grid
- the currently seated car as the active baseline

After this reset, next movement should occur from the grid baseline:

- from `A1` to `B1`: `down`
- from `B1` to `C1`: `down`
- from `C1` to `A2`: `right`, `up`, `up`

The reset sequence has been implemented and validated for the current guarded
4-car traversal. Larger traversal ranges must continue to prove
reset-before-movement behavior before real-input use.

## Loop Boundary

Auto3 loop execution must process a finite number of cars only.

The loop must refuse:

- missing car count
- non-integer car count
- car count less than or equal to `0`
- infinite loop requests

The loop should track:

- requested cars
- completed cars
- final status: `completed`, `stopped`, or `failed`

## Validation Progression

The original planned progression was:

1. In-memory movement sequence generation.
2. Unit tests for index-to-position mapping.
3. Unit tests for movement rules:
   - A to B
   - B to C
   - C to next-column A
4. In-memory baseline reset sequence generation.
5. Tests proving each multi-car segment returns to the My Cars grid baseline
   before next movement.
6. In-memory Auto3 test-mode traversal without unlock actions.
7. Guarded real-input test-mode traversal without unlock actions.
8. Only after traversal validation, consider guarded unlock loop behavior.

Current status:

- in-memory movement generation exists
- reset-to-grid sequencing exists
- guarded real-input test-mode traversal exists
- guarded 4-car unlock validation exists for `A1 -> B1 -> C1 -> A2`

Future scaling should repeat this validation ladder before increasing limits.

## Safety Boundaries

Auto3 grid traversal must preserve the current safety boundaries:

- no Auto4
- no destructive deletion
- no unattended infinite loop
- no production loop
- no expansion beyond 4 cars without a dedicated validation milestone
- no B/C start-row behavior without adjusted traversal validation
- no `main.py` startup automation
- real-input traversal must require explicit confirmation
- F8 stop must remain available in guarded real-input traversal

## Current Recommendation

Treat the current 4-car row-`A` traversal as the validated baseline. Future
scaling should be validation-based, not treated as permanently blocked or
automatically safe.
