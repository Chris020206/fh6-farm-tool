# Auto3 Grid Traversal Rules

## Purpose

This document locks the Auto3 My Cars grid traversal model before loop or index
behavior is implemented.

This is documentation only. No Auto3 loop behavior exists yet.

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

Exact FH6 behavior must be validated before real-input use.

## Postponed Work

Auto3 loop and grid traversal are postponed until this rule is implemented and
tested.

Do not add real-input loop behavior until:

- same-column movement is implemented safely
- column transition behavior is implemented separately
- the `right`, `up`, `up` transition concept is validated
- test-mode validation confirms traversal without spending skill points
