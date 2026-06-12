# Profile Editing Plan

## Philosophy

Official profiles are read-only baseline profiles. They must not be edited
directly by profile editing commands or future UI features.

Profile editing should create and modify custom profiles stored under
`profiles/custom/`. Official profiles remain the known-good reference point for
recovery, validation, and comparison.

Backups should be created or recommended before any profile editing operation.
Validation must run after editing so broken profiles fail clearly before they
can be used.

## First Editing Scope

The first supported editing surface should be timings only.

Timings-only editing is the safest first scope because it supports conservative
timing tuning without changing automation structure. It lets users adjust wait
values for their own hardware while avoiding changes that could break menu
navigation logic or key behavior.

## Explicitly Postponed

- Key editing.
- Navigation count editing.
- Profile import/export.
- UI profile editing.
- Profile marketplace or sharing.

## Future Command Direction

The intended future command flow is:

1. Duplicate an official profile into a custom profile.
2. Edit one timing value on the custom profile.
3. Validate the custom profile.
4. Use custom profiles in automation later, after profile selection is designed.

Automation should continue to use official profiles until custom profile
selection is explicitly implemented.

## Safety Rules

- Never overwrite official profiles.
- Never skip validation after editing.
- Never edit profile files during automation execution.
- Create or recommend a backup before editing.
- Keep timing edits profile-driven and local to custom profiles.

## Accepted Boundary

Profile editing is not implemented yet. This plan defines the safe direction so
future write behavior does not accidentally weaken the current validated
official profiles.
