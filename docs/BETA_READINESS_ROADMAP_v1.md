# FH6 Farm Tool - Beta Readiness Roadmap v1

## Purpose

This roadmap exists to:

- prevent reactive development
- reduce scope creep
- align engineering with launch goals
- maintain trust-first product development
- define what beta ready actually means

This roadmap is the decision filter for new work.

If a task is outside the current phase, it is postponed unless explicitly
approved.

---

## Product Philosophy

FH6 Farm Tool should remain:

- trust-first
- safety-first
- reliability over cleverness
- supervised automation
- controlled/manual operation
- clarity over feature quantity
- small, intentional milestones
- legitimacy-focused
- launch trust before launch scale

The first 10 users are founding testers, not normal customers.

The goal is not fast scaling. The goal is a controlled, trustworthy,
small-scale beta before broader monetization.

---

## Phase 1 - Controlled MVP Stabilization

Status: Mostly complete.

Purpose: freeze the validated automation foundation.

Included baseline:

- Auto1 validated
- Auto2 validated
- Auto3 validated
- desktop execution validated
- documentation realignment completed
- anti-regression baseline established
- repo coherence improved
- execution architecture cleanup completed

Remaining work:

- minor stability work
- consistency checks
- documentation alignment
- anti-regression cleanup

Exit condition:

Core automation is stable enough that changes become intentional rather than
reactive.

---

## Phase 2 - Beta Readiness

Status: Active priority phase.

Purpose: turn validated internal software into something trustworthy enough for
external supervised use.

No new automation capability during this phase.

Explicitly frozen during this phase:

- Auto4
- new automation systems
- speculative features
- over-polish
- advanced customization
- growth or scaling work
- website work
- Plus overengineering

### Track A - Packaging & Install

Goal: download -> launch -> success.

Included work:

- executable packaging
- dependency handling
- startup verification
- install guidance
- Defender guidance if required
- clean startup/shutdown behavior
- proper branding assets
- lightweight legitimacy pass
- minimal tray icon support, strictly scoped

Allowed tray scope:

- open app
- hide/show
- exit
- optional simple ready status

Not allowed tray scope:

- hidden automation
- background execution
- automation start from tray
- notification system
- startup-with-Windows
- complexity creep

Exit condition:

A non-technical FH player can install and launch successfully.

---

### Track B - Trust & Legitimacy

Goal: software feels legitimate.

Included work:

- Discord trust architecture
- `#how-it-works`
- `#download-and-install`
- `#security-and-transparency`
- `#known-issues`
- transparency messaging

Trust concerns around automation software are expected and must be handled
openly.

Preserve this messaging:

- supervised automation
- keyboard input only
- no cheats
- no memory editing
- no DLL injection
- no account access
- F8 emergency stop

Exit condition:

A reasonable trust threshold is reached for external testers.

---

### Track C - Onboarding UX

Goal: users understand how to succeed.

Included work:

- baseline state clarity
- automation explanations
- stop behavior
- expectations
- completion behavior
- simple onboarding guidance

Exit condition:

Most testers can succeed without founder intervention.

---

### Track D - Failure Recovery

Goal: failure does not destroy trust.

Included work:

- actionable failure messaging
- recommended next steps
- recovery guidance
- understandable stop states

Exit condition:

Failure feels understandable and recoverable.

---

### Track E - Founding Tester Operations

Goal: the 10-person founding tester beta is manageable.

Included work:

- Discord structure
- tester intake
- support process
- rollout process
- feedback structure
- issue collection

Quality of testers matters more than quantity.

Exit condition:

10 testers can be supported intentionally.

---

## Phase 2 Exit Condition - Definition of Beta Ready

Beta ready means a new FH player can:

- install the software
- understand how it works
- understand required FH6 baseline states
- run Auto1, Auto2, and Auto3 successfully
- recover from common issues
- trust the software
- operate mostly without founder intervention

Beta ready does not mean:

- public launch ready
- polished software
- website ready
- large-scale ready
- unattended automation ready

---

## Phase 3 - Founding Tester Beta

Purpose: reality validation.

Scope: about 10 lifetime-access founding testers.

Goals:

- trust
- feedback
- bug discovery
- onboarding validation
- support understanding
- usage patterns

This phase is for learning, not revenue optimization.

Success indicators:

- testers remain active
- onboarding friction decreases
- repeated failures become rare
- support burden becomes manageable
- trust improves
- bug reports become narrower rather than foundational

Exit condition:

Real-world confidence is achieved.

---

## Phase 4 - Paid Beta

Purpose: controlled monetization.

This phase begins only after the founding tester beta stabilizes.

Potential scope:

- Basic
- Plus
- gated Discord access

There is no rush toward scale. Small controlled growth is preferred.

Example scale: 25-50 users before broader expansion.

Exit condition:

Trust, onboarding, and support become repeatable.

---

## Decision Filter

Before starting new work, ask:

1. Which roadmap phase does this belong to?
2. Does this improve trust, onboarding, reliability, or beta readiness?
3. Is this solving a real problem or a speculative future problem?

If the answer is unclear, postpone the work.

---

## Roadmap Override Rule

New work may enter the active phase only if it:

- removes friction for beta readiness
- improves trust
- improves onboarding
- improves reliability
- fixes validated user pain

Interesting ideas alone are not sufficient justification.

---

## Final Principle

The biggest risk to FH6 Farm Tool is not lack of ideas.

The biggest risk is scope creep before trust and legitimacy are earned.

This roadmap exists to preserve disciplined execution.
