# Auto3 Grid Traversal Rules

## Purpose

This document records the Auto3 My Cars grid traversal model that was first
defined before loop/index behavior existed and is now implemented within the
current guarded/manual validation boundary.

Current validated boundary:

- max cars: `4`
- start row: `A`
- validated traversal: `A1 -> B1 -> C1 -> A2`
- real-input usage remains dangerous/manual/test-only
- no production Auto3 command exists
- no unattended Auto3 mode exists

## Grid Model

The Auto3 My Cars grid has:

- 3 fixed rows
- variable columns depending on the number of cars

Grid notation:

- rows: `A`, `B`, `C`
- columns: `1`, `2`, `3`, ...

Example positions:

- `A1`
- `B1`
- `C1`
- `A2`
- `B2`
- `C2`

## Traversal Order

Auto3 traversal order is:

1. `A1`
2. `B1`
3. `C1`
4. `A2`
5. `B2`
6. `C2`
7. `A3`
8. `B3`
9. `C3`

This means Auto3 moves down within a column first, then transitions to the next
column.

## Normal Down Movement

Normal `down` movement works from:

- `A` -> `B`
- `B` -> `C`

These movements can be treated as normal next-car movement within the same
column.

## Column Transition

Moving from `Cn` to `A(n+1)` requires a column transition.

This must be treated as a separate sequence, not as a normal `down` press.

Likely transition concept:

1. `right` once
2. `up` twice

This transition has been validated for the current `C1 -> A2` guarded
real-input traversal. Future transitions beyond the current 4-car boundary must
still be validated before real-input use.

## Current Boundary And Future Work

Auto3 grid traversal is implemented and validated only within the current
4-car, row-`A` boundary.

Future scaling remains validation-based. Do not expand real-input traversal
beyond the current boundary until:

- the larger movement range is implemented safely
- additional column transitions are validated
- test-mode validation confirms traversal without spending skill points
- guarded unlock validation proves the larger count remains trustworthy
