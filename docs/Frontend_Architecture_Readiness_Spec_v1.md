# FH6 Farm Tool — Frontend Architecture Readiness Specification v1

## Purpose

This document defines the frontend architecture readiness layer for FH6 Farm Tool.

Its purpose is not to design visual UI yet.

Its purpose is to translate the established product/UX architecture into an implementable frontend direction without breaking the product philosophy.

This document acts as a bridge between:

```text
Product Constitution
↓
Frontend Translation Principles
↓
Engineering-Aware Frontend Architecture
↓
Repository Reconciliation
↓
Implementation
```

The central question this document answers is:

> How do we implement FH6 Farm Tool without losing what makes FH6 Farm Tool coherent?

---

# 1. Source-of-Truth Hierarchy

Current hierarchy:

## 1. UX/Product Architecture Documents

These are the active strategic direction.

They define:

- product philosophy
- UX principles
- behavioral architecture
- information architecture
- workflow architecture
- structural direction
- launch-facing UX logic

They represent:

> where the product is going.

---

## 2. Git Repository

The repository is the validated implementation baseline.

It defines:

- what currently exists
- what has been validated
- current technical boundaries
- safety systems
- implementation constraints
- reusable abstractions

The repository is intentionally behind the UX/product architecture.

This is by design.

The repository should constrain fantasy, but it should not override the product direction.

---

# 2. Current Phase

The project is currently in:

> Frontend / Implementation Translation Readiness

This means:

We are not yet implementing UI.

We are not yet building frontend screens.

We are defining the frontend architecture required to preserve:

- trust
- coherence
- execution confidence
- restrained complexity
- premium desktop utility feeling
- safety-first automation behavior
- implementation realism

---

# 3. Product Identity Constraints

All frontend decisions must preserve the locked identity of FH6 Farm Tool:

- Premium desktop utility
- Controlled automation software
- Trust-first system
- Reliability over cleverness
- Safety before speed
- Professional feeling
- Gaming-adjacent, not childish

The emotional target remains:

> Nothing feels off.

Supporting targets:

- calm confidence
- crispness
- coherence
- refinement
- intentionality
- purposefulness
- control without anxiety

---

# 4. Frontend Architecture Goal

The frontend architecture should optimize for:

> product-coherent implementation.

Not:

- fastest possible implementation
- maximum abstraction
- visual novelty
- generic component reuse
- technical cleverness

The frontend should preserve:

- consistency
- predictability
- calm confidence
- scalable refinement
- restrained complexity
- execution trust

Implementation should protect the product.

---

# 5. Global App Shell

## Recommended Architecture

> Operational Shell Architecture

The application should have:

### Stable elements

- sidebar
- window identity
- navigation familiarity
- consistent application frame

### Adaptive elements

- center emphasis
- screen responsibility
- state weighting
- running-state reduction
- contextual confidence layers

The app should feel like:

> a composed operational environment

not:

> fragmented pages inside a generic app.

---

# 6. Navigation Model

Top-level navigation should remain restrained.

Recommended top-level structure:

```text
Home
Profiles
History
Help
Settings
```

Important rule:

> Automations are not a separate sidebar tab.

Reason:

> Automations are the product.

Automations should live primarily inside Home as first-class operational destinations.

Navigation should support intention, never dominate attention.

The sidebar should feel:

- quiet
- stable
- supportive
- predictable
- desktop-native

It should not feel:

- SaaS-like
- heavy
- dominant
- exploratory
- feature-driven

---

# 7. Screen Types

The frontend should avoid treating every screen as a unique invention.

Instead, screens should map to product responsibilities.

## Screen Type A — Operational Focus Screen

Used for:

- Home
- Automation Environment

Purpose:

> launch intent and execution confidence.

---

## Screen Type B — Operational Memory Screen

Used for:

- History

Purpose:

> trust recovery and post-run clarity.

---

## Screen Type C — Trust Selection Screen

Used for:

- Profiles

Purpose:

> choosing trusted execution behavior.

---

## Screen Type D — Confidence Support Screen

Used for:

- Help

Purpose:

> reducing uncertainty through calm guidance.

---

## Screen Type E — System Control Screen

Used for:

- Settings

Purpose:

> quiet control over application-level behavior.

---

# 8. Center Content Structure

The main content area should use:

> weighted content zones.

Conceptually:

```text
AppShell
├─ Sidebar
└─ MainContent
   ├─ PrimaryZone
   ├─ SecondaryZone
   └─ TertiaryZone
```

This is not necessarily final code structure.

It is a structural principle.

Each screen should have:

## Primary Zone

The dominant operational focus.

## Secondary Zone

Supporting confidence information.

## Tertiary Zone

Refinement, filters, advanced controls, or lower-priority settings.

Hard rule:

> One primary intention per screen.

Avoid:

- equal visual democracy
- dashboard equality
- competing regions
- feature pileups

Premium software feels premium because it knows what matters.

---

# 9. Screen Structural Responsibilities

## 9.1 Home

Philosophy:

> Focused launch environment.

Primary role:

> show automations as the product.

Dominant focus:

- Auto1
- Auto2
- Auto3
- future Auto4 only if justified by safety milestone

Secondary role:

> operational reassurance.

Possible secondary context:

- recent run summary
- last relevant profile
- light readiness reminder
- trusted current system state

Avoid:

- metrics dashboard
- XP/hour focus
- CR/hour focus
- statistics-heavy homepage
- news feed
- software update clutter

Emotional target:

> I know exactly what this software is for.

---

## 9.2 Automation Environment

Philosophy:

> execution confidence environment.

The automation environment is not primarily:

- a configuration screen
- a command launcher
- a settings page

Its job is:

> build confidence before execution.

Soft-locked structure:

```text
1. Overview
2. Profile
3. Readiness
4. Contextual Warnings
5. Advanced / Refinement Layer
6. Run
```

Spatial flow:

```text
Orientation
↓
Confidence Formation
↓
Commitment
```

### Overview

Responsibility:

> situational confidence.

It should explain:

- what automation this is
- what it does
- current validated scope
- expected starting context

It should be:

> environmental, but context-bound.

---

### Profile

Responsibility:

> behavioral assumptions.

It explains how the automation behaves.

It should communicate:

- execution posture
- timing philosophy
- reliability posture
- profile purpose

It should not become a technical settings panel.

---

### Readiness

Responsibility:

> quiet baseline confirmation.

It should surface:

- expected FH6 positioning
- baseline assumptions
- common alignment requirements

Important rule:

Readiness should be assumption-based, not fake verification-based.

Avoid:

> Verified

unless actual verification exists.

Prefer:

- Expected
- Assumed
- Recommended
- Validated baseline

---

### Contextual Warnings

Responsibility:

> rare, contextual, confidence-preserving caution.

Warnings should be proportional.

No warning fatigue.

No permanent concern signaling.

No panic language.

---

### Advanced / Refinement Layer

Responsibility:

> controlled refinement.

Default posture:

> secondary and collapsed.

Advanced should be available but should never become the emotional center.

If Advanced changes execution behavior, the change must reflect back into Overview, Readiness, Warnings, or Run.

---

### Run

Responsibility:

> deliberate commitment.

Run should feel:

- earned
- calm
- confident
- restrained

Avoid:

- giant CTA energy
- excitement
- hype
- post-click confirmation popups

The confidence should be built before commitment.

---

## 9.3 Running State / Companion Mode

Philosophy:

> peripheral, but confidently available.

Real usage context:

- FH6 likely runs windowed
- FH6 Farm Tool sits beside the game
- user attention shifts to FH6 during execution

Therefore, during execution, the software should step back.

Running state should emphasize only:

- what is running
- current status
- safe stop control
- calm confidence signal
- meaningful interruption if needed

Running state should not become:

- live dashboard
- telemetry feed
- technical console
- flashy progress UI

The running interface should reduce itself intentionally.

This is:

> adaptive simplicity.

Not:

> disappearing UI.

The software remains respectfully present.

---

## 9.4 History

Recommended name direction:

> Operational History

Philosophy:

> recency-weighted operational memory.

Primary role:

> trust recovery.

Question answered:

> What happened?

Dominant focus:

- most recent run sessions

Session model:

> session-oriented, not timestamp-stream oriented.

Default structure:

- most recent first
- spacious but relevant session summaries
- layered expansion for meaningful details

Avoid:

- raw logs
- keypress streams
- developer console output
- live monitoring
- forensic UI

History should feel:

> calm post-run clarity.

---

## 9.5 Profiles

Philosophy:

> execution confidence system.

Profiles are not primarily technical presets.

Profiles represent:

> trusted execution behavior.

Basic:

> curated trusted recommendations.

Plus:

> controlled profile library.

Selection model:

> intentional, but subtle.

Custom profiles:

> earned, not encouraged.

Profile information should explain:

> behavioral expectations

not:

> technical mechanics.

Good:

> Reliability-first execution with conservative timing.

Bad:

> wait_after_menu_confirm = 7.0

Profiles structure should be:

```text
Recommended Profiles
↓
Alternative Validated Profiles
↓
Custom / Advanced Profiles
```

Dominant focus:

> profiles users can trust.

Avoid:

- profile chaos
- endless variants
- raw timing exposure
- configuration anxiety

---

## 9.6 Help

Philosophy:

> confidence reinforcement layer.

Help should not feel like:

- documentation center
- giant wiki
- support ticket system
- required manual

Primary behavior:

> contextual first, destination second.

Dedicated Help screen should be:

> question-oriented.

Dominant focus:

- common uncertainty points
- baseline expectations
- automation expectations
- profile understanding
- result meanings
- validated boundaries

Tone:

> operational warmth.

Meaning:

- restrained
- clear
- human
- calm
- not robotic
- not chatty

Help should feel:

> available, not necessary.

---

## 9.7 Settings

Philosophy:

> expectation-weighted quiet system control.

Settings should answer:

> How should FH6 Farm Tool behave as a system?

Settings should not answer:

> How should automation execution behave?

Execution behavior belongs in Profiles.

Dominant focus:

- appearance
- theme
- notifications
- startup behavior
- window behavior

Secondary focus:

- safety preferences
- confirmation preferences
- emergency stop behavior

Tertiary focus:

- advanced system preferences
- update behavior
- future environment detection

Settings should feel:

> stable and rarely visited.

Avoid:

- settings sprawl
- execution tuning
- profile duplication
- power-user chaos
- miscellaneous dumping ground

---

# 10. Component Philosophy

Components should be organized by behavioral role, not only by visual shape.

The goal of components is not maximum reuse.

The goal is:

> consistency that preserves product coherence.

Recommended conceptual components:

## AppShell

Stable application frame.

Includes sidebar and main content structure.

---

## OperationalScreen

Base structure for screens centered around operational focus.

---

## AutomationEnvironment

Container for pre-run, running, and completion states.

---

## ConfidenceCard

Used for:

- readiness
- baseline expectations
- profile confidence
- run summaries
- contextual operational clarity

---

## OperationalStatus

Used for:

- ready
- running
- completed
- stopped
- interrupted
- refused
- warning
- focus uncertain

---

## RiskNotice

Used for:

- contextual warnings
- risk-sensitive acknowledgements
- commitment-related caution

---

## RecommendationItem

Used for:

- recommended profiles
- suggested next steps
- contextual continuity

---

## RunCommitmentArea

Used for:

- final run action
- acknowledgement threshold
- transition into running state

---

## CompanionStatus

Used for:

- reduced running state
- low-attention execution awareness
- stop control visibility

---

## SessionSummary

Used for:

- operational history run sessions
- completion/stopped/interrupted summaries
- layered expansion

---

# 11. Product State Vocabulary

States should be product-wide behaviors.

Do not define state meaning separately per screen.

Shared states:

```text
READY
RUNNING
COMPLETED
STOPPED
INTERRUPTED
REFUSED
WARNING
FOCUS_UNCERTAIN
FAILURE
```

Each state should have:

- user-facing meaning
- tone rules
- allowed actions
- confidence message style
- emphasis behavior
- recovery path if relevant

## READY

Meaning:

> conditions appear prepared enough to run.

Tone:

> calm confidence.

---

## RUNNING

Meaning:

> automation is executing.

Tone:

> peripheral, calmly available.

---

## COMPLETED

Meaning:

> execution ended as expected.

Tone:

> quiet reassurance.

---

## STOPPED

Meaning:

> user intentionally stopped automation.

Tone:

> controlled return.

---

## INTERRUPTED

Meaning:

> automation did not complete because something changed or stopped.

Tone:

> calm clarity.

---

## REFUSED

Meaning:

> execution was blocked to protect quality or safety.

Tone:

> protective clarity.

---

## WARNING

Meaning:

> meaningful risk or context requires attention.

Tone:

> calm seriousness.

---

## FOCUS_UNCERTAIN

Meaning:

> software cannot confidently proceed because focus or baseline is uncertain.

Tone:

> guided readiness.

---

## FAILURE

Meaning:

> execution failed unexpectedly.

Tone:

> composed recovery.

---

# 12. Data Requirements for Future Repo Evolution

The frontend will need structured product-facing data.

Raw logs are not enough.

Likely future data models:

## Automation Definition

Includes:

- automation id
- display name
- purpose
- validated scope
- expected baseline
- risk level
- available profiles
- supported run modes

---

## Profile Metadata

Includes:

- profile id
- profile name
- automation type
- recommendation status
- behavior summary
- reliability posture
- package availability: Basic / Plus
- customization availability
- technical timing data hidden from normal UI

---

## Readiness Model

Includes:

- expected baseline assumptions
- recommended setup
- confidence notes
- acknowledgement requirement level
- risk-weighted friction level

---

## Run Session

Includes:

- session id
- automation id
- status
- started at
- completed/stopped/interrupted at
- profile used
- requested count
- completed count
- meaningful outcome summary
- user-facing notes
- warnings encountered
- suggested next step

---

## Operational History Entry

Should be derived from Run Session.

Not raw technical logs.

---

## Settings Model

Must stay separate from Profile execution behavior.

Includes:

- theme
- startup behavior
- notification preferences
- safety preferences
- window / companion behavior
- future update preferences

---

# 13. Implementation Guardrails

## Guardrail 1

> Product Constitution overrides implementation convenience.

If an easier implementation breaks the product philosophy, reject it.

---

## Guardrail 2

> Execution behavior belongs in Profiles, not Settings.

Critical anti-drift rule.

---

## Guardrail 3

> Components should preserve behavioral consistency.

Do not build one-off interactions unless strongly justified.

---

## Guardrail 4

> Do not expose raw technical details by default.

Technical details may exist deeper for debugging, but they are not the primary UX.

---

## Guardrail 5

> Never imply certainty the software does not possess.

No fake verification.

No false confidence.

---

## Guardrail 6

> More power without philosophical drift.

Especially for Plus.

Plus should add controlled depth, not visible complexity.

---

## Guardrail 7

> Every new feature must strengthen an existing user intention.

If the intention is unclear, the feature is likely bloat.

---

## Guardrail 8

> Reduce before adding.

When the UI feels crowded, first ask what can disappear.

---

# 14. What This Document Does Not Do

This document does not define:

- final visual design
- color palette
- typography
- exact component styling
- pixel-level layout
- frontend framework
- implementation language
- final repo changes
- pricing logic
- licensing implementation
- public release readiness

Those come later.

---

# 15. Next Recommended Step

The next phase should be:

> Repository Reconciliation Planning

Goal:

Identify what the existing repo needs in order to support the future frontend architecture.

Likely areas:

- UI module structure
- product-facing state model
- structured run session data
- profile metadata expansion
- operational history model
- settings/profile separation
- automation definitions
- frontend-safe command interfaces
- companion mode state support

This should happen before actual UI implementation.

---

# Closing Principle

The frontend should not merely display the software.

It should preserve the product.

FH6 Farm Tool should continue to feel like:

> a refined, trustworthy, intentionally designed desktop utility for controlled automation where nothing feels off.
