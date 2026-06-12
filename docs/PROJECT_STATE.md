# FH6 Farm Tool — Project State

## Project Status

Controlled MVP Ready — Developer/Manual Use

This means the validated command surface is ready for careful, supervised
developer/operator use.

This does not mean broad public/customer release readiness. The project is not
packaged, not UI-driven, and not ready for unattended automation.

---

## Current Phase

MVP Hardening & Polish

Current priorities:

- operator runbooks
- CLI polish
- safety hardening
- documentation consistency
- additional refusal/profile tests
- packaging strategy planning only

Not current priorities:

- Auto4
- UI
- new automation capability
- timing optimization
- expanding Auto3 boundaries

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
- Auto4
- unattended automation
- timing optimization
- destructive/remove-car behavior
- startup automation

---

## Repository State

- GitHub active
- default branch = main
- Controlled MVP baseline established
- recommended milestone tag: `v0.1-controlled-mvp`

---

## Next Recommended Milestone

M11.5 — Operator Runbooks

Focus:

- Auto1 runbook
- Auto2 runbook
- Auto3 runbook

No new automation capability before hardening.

---

## Source of Truth Priority

1. Current code
2. Current docs
3. Validation reports
4. Recent implementation context
5. Older assumptions
