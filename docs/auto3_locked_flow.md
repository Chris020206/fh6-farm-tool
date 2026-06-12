# Auto3 Locked Flow

## Purpose

This document records the corrected Auto3 Skill Tree Automation flow.

Auto3 now has in-memory validation modes, guarded real-input test-mode
navigation, a guarded one-car unlock harness, and guarded/manual multi-car
unlock validation within the current 4-car boundary.

## Corrected Baseline

Auto3 starts from:

- Garage -> Cars -> My Cars
- default manufacturer sorting
- user seated in A1 Subaru
- target Subarus arranged through A1, B1, C1, A2, B2, C2...
- 3 fixed rows
- variable columns

The baseline assumes the user is already in the correct Garage / My Cars context before Auto3 begins.

## Initial Sorting Setup

The initial sorting setup is:

1. `x`
2. `down` x6
3. `enter`

This sorts by Recently Added and returns the seated car as the active baseline.

## First-Car Exception Path

A1 is already seated.

For A1:

- do not execute the get-in-car sequence
- start from the active seated-car baseline
- execute the reusable unlock sequence
- execute the return/reset sequence

## Normal Next-Car Get-In Sequence

For cars after A1, the normal get-in sequence is:

1. `down`
2. `enter`
3. `enter`

This selects the next target car and seats the user in it before the unlock sequence begins.

## Reusable Unlock Sequence

The reusable unlock sequence is:

1. `esc`
2. `down` to Upgrades & Tuning
3. `enter`
4. `down` to Car Mastery
5. `enter`
6. `enter`
7. `right`
8. `enter`
9. `up`
10. `enter`
11. `up`
12. `enter`
13. `up`
14. `enter`
15. `left`
16. `enter`
17. `esc`
18. `esc`

The perk unlock path is:

1. `enter`
2. `right`
3. `enter`
4. `up`
5. `enter`
6. `up`
7. `enter`
8. `up`
9. `enter`
10. `left`
11. `enter`

## Return / Reset Sequence

After unlocking, the return/reset sequence is:

1. `up` x7
2. `enter`
3. `x`
4. `down` x6
5. `enter`

This returns Auto3 to the sorted baseline for the next target.

## Auto3 Paths

Auto3 has two planned paths:

- first-car exception path
- normal next-car path

The first-car exception path is for A1 only. Normal next-car handling begins after A1.

## Postponed Work

The following work is explicitly postponed:

- production Auto3 command
- Auto3 counts greater than 4
- B/C start-row support
- additional grid traversal beyond `A1 -> B1 -> C1 -> A2`
- Auto4 car removal in the current hardening scope

UI is not part of the current controlled/manual command surface, but M11
strategic doctrine requires a restrained premium desktop UI before public paid
launch.

## Current Status

This document is the locked flow reference for current Auto3 behavior. Auto3
test-mode real-input validation, the one-car unlock harness, and guarded 4-car
multi-car unlock validation exist. Current real-input Auto3 remains
dangerous/manual/test-only, finite, and guarded by confirmation flags.
