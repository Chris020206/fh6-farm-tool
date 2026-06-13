# FH6 Farm Tool — Repository Reconciliation Plan v1

## Purpose

This document translates the FH6 Farm Tool frontend/product architecture into a practical repository evolution plan.

Its purpose is not to implement UI immediately.

Its purpose is to answer:

> What does the current repository need in order to support the future frontend architecture without breaking the product philosophy?

This document bridges:

```text
Frontend Architecture Readiness Specification v1
↓
Repository Reconciliation Planning
↓
Phased Implementation
↓
Frontend/UI Development
```

---

# 1. Current Repository Role

The Git repository should be treated as:

> validated implementation baseline

not:

> current product direction.

The repository is intentionally behind the UX/product architecture.

This is by design.

The repo currently represents:

- validated automation behavior
- current command surface
- safety systems
- profile tooling
- real-input guardrails
- implementation constraints
- modular backend foundation

The new UX/product architecture represents:

- future product direction
- launch-facing UX logic
- frontend architecture needs
- operational coherence
- trust-facing software behavior

The reconciliation goal is:

> evolve the repo intentionally toward the product architecture.

Not:

> force the product architecture to fit the current repo.

---

# 2. Reconciliation Principle

All repo evolution should follow this sequence:

```text
Preserve validated safety baseline
↓
Add product-facing structure
↓
Expose frontend-safe data
↓
Create UI-ready architecture
↓
Implement frontend gradually
```

Important:

No existing safety boundary should be casually removed.

Especially:

- guarded real-input commands
- confirmation requirements
- finite execution boundaries
- F8 stop behavior
- isolated real keyboard backend
- safe `main.py` startup behavior
- profile validation
- dangerous command refusal logic

---

# 3. Main Gap Between Repo and Product Direction

The current repo is automation-command oriented.

The future product needs to become product-state oriented.

Current repo emphasis:

```text
commands
runners
profiles
validation reports
manual execution
dangerous test harnesses
```

Future frontend needs:

```text
automation definitions
profile metadata
readiness models
run sessions
operational history
frontend-safe state vocabulary
companion-mode state
system settings separation
```

This is not a contradiction.

It is the natural next maturity step.

---

# 4. Required Repository Evolution Areas

## 4.1 Automation Definition Layer

The frontend needs a structured way to understand each automation.

Recommended future model:

```text
AutomationDefinition
```

Should include:

- automation id
- display name
- short purpose
- long purpose
- risk level
- validated scope
- expected baseline
- available profiles
- supported modes
- package availability: Basic / Plus
- current maturity status
- contextual warnings
- suggested next step logic

Example purpose:

```text
Auto3 helps unlock skill-tree rewards using a validated controlled execution path.
```

Why needed:

The UI should not hardcode automation explanations in screen components.

The product needs a single structured source for automation identity and confidence context.

---

## 4.2 Profile Metadata Expansion

The current profile system is a strong foundation, but future UI needs richer product-facing metadata.

Recommended future model:

```text
ProfileMetadata
```

Should include:

- profile id
- profile name
- automation type
- recommendation status
- package tier
- behavior summary
- reliability posture
- intended user/environment
- validation confidence
- customization status
- editable fields
- hidden technical timing data

Important rule:

Technical timing values should not be exposed as the primary UI language.

User-facing profile explanations should describe behavior.

Good:

```text
Reliability-first execution with conservative timing.
```

Bad:

```text
wait_after_menu_confirm = 7.0
```

---

## 4.3 Readiness Model

The future UI needs structured readiness information.

Recommended future model:

```text
ReadinessModel
```

Should include:

- expected FH6 baseline
- manual positioning assumption
- recommended setup
- focus requirement
- cursor requirement, if relevant
- risk-weighted acknowledgement level
- confidence notes
- blocked/refused conditions
- user-facing readiness wording

Important rule:

Do not imply fake verification.

Avoid:

```text
Verified
```

unless the system truly verifies state.

Prefer:

```text
Expected
Assumed
Recommended
Validated baseline
```

---

## 4.4 Product State Vocabulary

The frontend needs shared state meaning.

Recommended shared states:

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

Each state should define:

- user-facing meaning
- tone
- allowed actions
- recovery path
- summary message
- frontend emphasis behavior

Why needed:

Inconsistent state handling will weaken trust.

State behavior should be product-wide, not screen-specific.

---

## 4.5 Run Session Model

The current repo has command results and logs, but the future product needs structured operational sessions.

Recommended future model:

```text
RunSession
```

Should include:

- session id
- automation id
- profile id
- requested count
- completed count
- status
- start time
- end time
- duration
- warnings encountered
- stop/interruption reason
- user-facing summary
- suggested next step
- raw technical reference, optional/internal only

Why needed:

Operational History should not be built from raw logs.

It should be built from meaningful run sessions.

---

## 4.6 Operational History Model

History should present:

> operational memory

not:

> developer logs.

Recommended future model:

```text
OperationalHistoryEntry
```

Derived from RunSession.

Should include:

- automation name
- outcome
- concise summary
- meaningful context
- profile used
- timestamp
- expandable details
- confidence/recovery note

Avoid:

- raw keypress streams
- internal runner messages
- technical debug logs
- terminal-style output

---

## 4.7 Settings / Profiles Separation

This is one of the most important anti-drift rules.

Execution behavior belongs in:

```text
Profiles
```

System behavior belongs in:

```text
Settings
```

Settings should include:

- theme
- startup behavior
- notifications
- window behavior
- companion mode preference
- safety preferences
- update behavior, future

Settings should not include:

- timing profiles
- automation tuning
- navigation counts
- execution strategy
- profile editing duplication

This separation protects the product from settings gravity.

---

## 4.8 Companion Mode Support

Running-state UI should be treated as core product architecture.

The repo/frontend will eventually need:

```text
CompanionModeState
```

Should include:

- active automation
- running status
- current progress summary
- stop availability
- confidence message
- interruption message, if relevant
- reduced-footprint UI data

Important:

Companion mode should be a reduced state of the same automation environment.

Not a separate mini-app.

---

## 4.9 Frontend-Safe Command Interface

The current repo has manual guarded commands.

Future frontend should not directly execute dangerous automation without product-facing safety mediation.

Recommended future abstraction:

```text
FrontendAutomationController
```

Responsibilities:

- validate requested automation
- validate profile
- validate run count
- check confirmation/acknowledgement requirements
- produce readiness state
- start execution safely
- update run session
- expose stop control
- produce completion/interruption summary

This should sit above automation runners.

It should not bypass existing safety systems.

---

# 5. Suggested Future Module Areas

Potential future repo structure additions:

```text
product/
  automation_definitions.py
  product_states.py
  readiness_models.py
  risk_levels.py

sessions/
  run_session.py
  session_store.py
  operational_history.py

frontend/
  view_models/
  controllers/
  state_adapters/

ui/
  app_shell/
  screens/
  components/

settings/
  app_settings.py
  settings_schema.py
```

This is conceptual.

Final structure should be adapted to the actual repository style.

The key principle:

> Add product-facing structure before visual UI.

---

# 6. Phased Repository Reconciliation Plan

## Phase R1 — Product Data Layer

Goal:

Create product-facing definitions without changing automation behavior.

Deliverables:

- AutomationDefinition model
- ProductState enum
- RiskLevel model
- basic automation metadata for Auto1, Auto2, Auto3
- placeholder for future Auto4 as conditional / disabled

Why first:

This creates a safe bridge between current backend and future frontend.

No automation behavior changes required.

Risk:

Low.

---

## Phase R2 — Profile Metadata Layer

Goal:

Expand profiles so they can support frontend trust language.

Deliverables:

- profile behavior summaries
- recommendation status
- package tier metadata
- validation confidence labels
- intended usage descriptions
- hide technical timing values from normal UI layer

Why second:

Profiles are central to execution confidence.

Risk:

Low–Medium.

Need to preserve existing profile validation.

---

## Phase R3 — Readiness & Risk Model

Goal:

Create structured readiness data per automation.

Deliverables:

- baseline expectation model
- readiness text per automation
- acknowledgement level rules
- warning/risk language
- no-fake-verification wording

Why third:

This supports Automation Environment UI later.

Risk:

Medium.

Must avoid pretending the software can verify FH6 state.

---

## Phase R4 — Run Session & Operational History

Goal:

Create session-oriented run records.

Deliverables:

- RunSession object
- session status lifecycle
- completed/stopped/interrupted summaries
- operational history entries
- layered detail support
- raw logs remain separate/internal

Why fourth:

History should be structured before UI is built.

Risk:

Medium.

Must avoid mixing developer logs with user-facing history.

---

## Phase R5 — Frontend-Safe Controller Layer

Goal:

Create a mediation layer between future UI and automation runners.

Deliverables:

- validation before run
- confirmation/acknowledgement handling
- readiness state
- run session creation
- stop handling
- completion/interruption summaries

Why fifth:

Prevents UI from directly wiring into dangerous commands.

Risk:

Medium–High.

Must preserve existing safety boundaries.

---

## Phase R6 — UI Shell Skeleton

Goal:

Introduce UI architecture without full visual design.

Deliverables:

- AppShell structure
- Sidebar destinations
- placeholder screens
- weighted content zone layout
- state-aware automation screen skeleton
- no final visual polish yet

Why sixth:

Only after product-facing backend structures exist.

Risk:

Medium.

Avoid visual-first drift.

---

## Phase R7 — Automation Environment Screen

Goal:

Implement first real product screen using the architecture.

Suggested first target:

> Auto1 Automation Environment

Reason:

Auto1 is lowest risk and most mature.

Deliverables:

- Overview
- Profile
- Readiness
- Contextual warnings
- Advanced placeholder
- Run commitment area
- companion running state

Risk:

Medium.

Good proof of system.

---

## Phase R8 — History / Profiles / Help / Settings Screens

Goal:

Implement secondary screens according to locked structure.

Order recommendation:

1. History
2. Profiles
3. Help
4. Settings

Reason:

This follows trust architecture before system control.

Risk:

Medium.

---

# 7. Implementation Rules

## Rule 1

Do not wire UI directly to dangerous automation runners.

Use a frontend-safe mediation layer.

---

## Rule 2

Do not expose raw technical settings by default.

Behavioral explanations come first.

---

## Rule 3

Do not move execution behavior into Settings.

Profiles own execution behavior.

---

## Rule 4

Do not implement UI before product-facing data exists.

Otherwise the frontend will hardcode philosophy into screens.

---

## Rule 5

Do not remove current safety gates casually.

The repo’s safety posture is an asset.

---

## Rule 6

Start with Auto1 for UI proof.

It is the safest first automation environment.

---

## Rule 7

Every repo change should answer:

> Which product architecture requirement does this support?

If unclear, defer it.

---

# 8. Recommended First Concrete Repo Milestone

## Milestone R1 — Product Definition Foundation

Goal:

Create a product-facing metadata layer without changing automation execution.

Suggested tasks:

1. Create product module.
2. Define ProductState enum.
3. Define RiskLevel enum.
4. Define AutomationDefinition dataclass.
5. Add definitions for Auto1, Auto2, Auto3.
6. Mark Auto4 as future/conditional, not active.
7. Add simple tests for metadata integrity.
8. Do not alter runners.
9. Do not alter real-input behavior.
10. Do not add UI yet.

Why this is the right first milestone:

- safe
- low risk
- aligns repo with product architecture
- does not disturb validated automation
- prepares future frontend
- creates a clear implementation bridge

---

# 9. What Not To Do Next

Do not start with:

- visual UI
- final styling
- theme system
- React/WPF component details
- licensing
- public packaging
- Auto4 implementation
- multi-cycle Auto2 production mode
- advanced customization
- timing optimization

Those are either later phases or separate milestones.

The next correct step is:

> product-facing backend structure.

---

# 10. Closing Recommendation

The repository should now evolve from:

> validated automation command system

toward:

> product-facing controlled automation platform.

But this must happen gradually.

The correct next move is not:

> build UI.

The correct next move is:

> create the structured product layer the UI will depend on.

This protects:

- safety
- trust
- implementation clarity
- product coherence
- future frontend quality

Final principle:

> The frontend should never have to invent product meaning locally.

The repo should provide product meaning structurally.
