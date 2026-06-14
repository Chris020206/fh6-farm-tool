# FH6 Farm Tool — Project State

## Project Status

Controlled MVP Ready — Developer/Manual Use

This means the validated command surface is ready for careful, supervised
developer/operator use.

This does not mean broad public/customer release readiness. The project is not
packaged, the desktop UI is not public launch-ready, and the project is not
ready for unattended automation.

---

## Current Phase

MVP Hardening & Polish

Current priorities:

- operator runbooks
- CLI polish
- desktop UI foundation hardening
- safety hardening
- documentation consistency
- additional refusal/profile tests
- packaging strategy planning only

Not current priorities:

- Auto4
- new automation capability
- timing optimization
- expanding Auto3 boundaries

Strategic note:

M11 doctrine treats UI as trust infrastructure. The PySide6 desktop UI
foundation now exists for controlled developer/manual use, but it must be
hardened before public paid launch.

---

## Current Validated Systems

### Auto1 — Race Automation

Status: Validated

- guarded/manual
- F8 stop
- finite cycles
- profile-driven timing
- no unattended mode

---

### Auto2 — Buy Car Automation

Status: Validated (Controlled Scope)

- test-mode navigation validation
- one-car purchase validation
- spending-risk protection
- guarded/manual
- no promoted production multi-cycle mode

---

### Auto3 — Skill Tree Automation

Status: Validated

Current hard limits:

- max cars = 4
- start row = A

Validated traversal:

```text
A1 → B1 → C1 → A2
```

Boundaries:

- dangerous/manual/test-only
- no production command
- no unattended mode

Validated behavior includes:

- first-car exception
- later-car get-in flow
- validated 12-second later-car recovery
- reset-to-grid baseline after each car
- clean termination after the fourth car

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
- Auto4 in the current hardening scope
- unattended automation
- timing optimization
- destructive/remove-car behavior
- startup automation

Auto3's 4-car limit is the current validated boundary, not a final launch
ceiling. Future scaling must be validation-based and explicitly milestoned.

Auto4 is a conditional pre-launch candidate under M11 doctrine, but remains
outside current MVP hardening until a dedicated safety milestone justifies it.

---

## Repository State

- GitHub active
- default branch = main
- Controlled MVP baseline established
- recommended milestone tag: `v0.1-controlled-mvp`

---

## Next Recommended Milestone

M11.6 - Command Surface Hardening

Focus:

- refusal message clarity
- command consistency
- operator visibility
- pre-flight validation
- safety hardening

No new automation capability before hardening.

---

## Source of Truth Priority

1. Current code
2. Current docs
3. Validation reports
4. Recent implementation context
5. Older assumptions
