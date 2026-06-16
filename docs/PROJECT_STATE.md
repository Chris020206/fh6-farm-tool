# FH6 Farm Tool - Project State

## Project Status

Controlled MVP Ready - Developer/Manual Use

This means the validated desktop UI and guarded command surface are ready for
careful, supervised developer/operator use. Auto1, Auto2, and Auto3 are
validated through the desktop execution surface within their current controlled
boundaries.

This does not mean broad public/customer release readiness. The project is not
packaged for public launch, not ready for unattended automation, and not safe to
operate without supervision.

---

## Current Phase

MVP Hardening & Polish

Current priorities:

- MVP hardening
- desktop execution hardening
- launch-facing UX foundation
- documentation realignment
- maintainability and architecture cleanup
- safety hardening
- packaging strategy planning only

Not current priorities:

- Auto4
- new automation capability
- unattended automation
- major timing optimization
- expanding Auto3 boundaries beyond validated limits

---

## Current Validated Systems

### Auto1 - Race Automation

Status: Validated

- guarded/manual desktop UI execution validated
- focus handoff
- fail-closed behavior
- F8 stop
- finite loop count handling
- race drive duration runtime adjustment
- profile-driven timing
- completion-state behavior
- no unattended mode

---

### Auto2 - Buy Car Automation

Status: Validated (Controlled Scope)

- guarded/manual desktop UI execution validated
- test-mode navigation validated
- purchase mode validated
- purchase count greater than 1 validated
- spending-risk protection
- F8 stop through guarded runner path
- completion behavior validated
- no unattended mode

---

### Auto3 - Skill Tree Automation

Status: Validated

Current validated limits:

- max validated cars = 4
- start row = A

Validated traversal:

```text
A1 -> B1 -> C1 -> A2
```

Validated behavior includes:

- guarded/manual desktop UI execution validated
- first-car exception
- safety reset navigation
- Recently Added re-sort
- multiple-car traversal
- row 3 / column 1 -> row 1 / column 2 transition
- current timing refinements
- completion behavior
- F8 stop through guarded runner path
- no unattended mode

---

## Locked Philosophy

### Product

- trust-first
- safety-first
- reliability over cleverness
- incremental milestones
- scope discipline

### Engineering

- modular architecture
- centralized shared systems
- automation isolation
- no automation from startup
- dangerous commands guarded

### Timing

- conservative timings
- slow > fragile
- profile-driven timing
- optimization postponed

### Safety

- F8 stop
- confirmation flags
- finite execution
- refusal-path tests
- cleanup on failure

---

## Current Hard Boundaries

These are frozen unless a future milestone explicitly changes them:

- Auto3 > 4 cars
- Auto3 B/C start rows
- Auto4 outside current scope
- unattended automation
- major timing optimization
- destructive/remove-car behavior
- startup automation

Auto3's 4-car limit is the current validated boundary, not a final ceiling.
Future scaling must be validation-based and explicitly milestoned.

---

## Repository State

- GitHub active
- default branch = main
- Controlled MVP baseline established
- desktop execution baseline established
- validated automation baseline established
- recommended milestone tag: `v0.1-controlled-mvp`

---

## Next Recommended Milestone

Documentation and Desktop Hardening Pass

Focus:

- documentation realignment
- launch-facing UX refinement
- desktop maintainability
- UI hardening
- anti-regression discipline

No new automation capability before hardening.

---

## Source of Truth Priority

1. Current code
2. Current docs
3. Validation reports
4. Recent implementation context
5. Older assumptions
