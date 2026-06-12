M11.5.5 — Strategic Alignment Review
Part 2 — Forecast to Launch
Project: FH6 Farm Tool
Review Type: Founder / Lead Developer Strategic Forecast
Status Date: Post-M11.5 (Operator Runbooks Complete)
Purpose: Define the realistic, soft-locked path from current state to launch.
1. Guiding Principle
The FH6 Farm Tool should not pursue:
maximum capability before launch.
The project should pursue:
maximum trustworthiness within a constrained and valuable MVP.
This distinction matters.
The objective is not:
more features
more automation
more complexity
The objective is:
reliable
predictable
safe
premium-feeling
worth paying for
Launch should represent:
a trustworthy paid product
—not—
“everything we could eventually build.”
1
The roadmap below intentionally prioritizes:
trust
clarity
reliability
scope discipline
launch readiness
over:
feature accumulation
premature complexity
technical ambition for its own sake
2. Current Position
The project has completed the transition from:
exploratory prototype
to:
structured MVP hardening.
Current maturity:
Controlled MVP Ready — Developer/Manual Use
Meaning:
What exists
modular architecture
guarded automation
validation boundaries
GitHub repo
operational runbooks
reliability documentation
profile system
command surface
controlled scope
What does not yet exist
launch polish
external-user readiness
•
•
•
•
•
•
•
•
•
•
•
2
onboarding
packaging
trust-facing presentation
public support structure
controlled external testing
Current state is healthy.
The project is sufficiently mature that:
adding major capability now carries greater risk than value unless carefully justified.
3. Soft-Locked Milestone Forecast
This section defines:
the recommended path to launch
The milestones are:
soft-locked
Meaning:
They may adapt when reality changes.
But changes should be:
intentional and justified.
M11.6 — Command Surface Hardening
Purpose
Make the software feel:
professional, predictable, and trustworthy.
Primary goals:
Command consistency
Example:
Standardize confirmation logic.
•
•
•
•
•
3
Avoid:
--confirm
--confirm-purchase
--confirm-unlock
--confirm-real-input
feeling inconsistent or confusing.
Better refusal messaging
Move from:
Refused
toward:
Refused:
Auto3 multi-car unlock requires:
--confirm-real-input
--confirm-unlock
Reason:
This command may spend skill points.
Better operator visibility
Example:
Auto3 Multi-Car Unlock
Cars: 4
Traversal: A1 → B1 → C1 → A2
Profile: auto3_default
F8 stop available
Goal:
operator confidence.
4
Pre-flight validation
Refuse invalid operations before execution.
Example:
Requested cars: 7
Refused:
Current validated limit = 4.
Mandatory?
Yes
Launch blocker:
Yes
Reason:
Trust-first software must feel:
intentional and safe.
M11.7 — Reliability & Edge Case Audit
Purpose
Systematically pressure-test assumptions.
Question:
“How does this fail safely?”
Focus areas:
Auto1
desync
focus loss
timing failure
Auto2
menu drift
spending risk
wrong selection
•
•
•
•
•
•
5
Auto3
traversal desync
loading variance
skill point risk
reset failures
Global systems
F8 reliability
cleanup behavior
refusal paths
profile corruption
weird user inputs
Philosophy:
Safe failure > fragile success
Mandatory?
Yes
Launch blocker:
Yes
M11.8 — Packaging Readiness Planning
Purpose
Prepare future distribution architecture.
Important:
planning
—not—
overbuilding.
Questions answered:
Packaging direction
Basic / Plus.
•
•
•
•
•
•
•
•
•
6
Profile strategy
What differs?
Licensing assumptions
Minimal or none?
Install flow
How trustworthy should install feel?
Folder structure
Production-ready organization.
Logs
User-facing troubleshooting.
Update philosophy
Manual first?
No complex updater yet?
Mandatory?
Yes
Launch blocker:
Yes
But:
keep complexity intentionally bounded.
M12 — Controlled Internal Beta
Purpose
Use the software like:
an actual paying customer would.
Not:
7
developer testing.
Meaning:
Intentional real usage.
Examples:
2-hour sessions
repeat usage
misuse attempts
stress testing
breaking assumptions
Question:
“Would I trust this for real?”
This phase exists because:
internal theory eventually stops helping.
Reality matters.
Mandatory?
Yes
Launch blocker:
Yes
M12.5 — Business Foundation Pivot
Purpose
Transition gradually from:
software-only thinking
toward:
launch thinking.
Important:
Software still primary.
8
Business now becomes:
impossible to ignore.
Tier 1 — Development-Critical Decisions
Must happen.
Basic / Plus packaging
Soft-lock structure.
Recommended:
Basic
Core value proposition:
Auto1
Auto2
Auto3
These are:
non-negotiable foundation.
Plus
Selective premium additions only.
Candidate features:
Auto4
faster Auto2 method
advanced timing control
expanded profile flexibility
Rule:
fair additional value
—not—
artificial feature gatekeeping.
9
Trust Positioning
Soft-lock positioning:
Recommended:
Safe, Premium, Trustworthy Automation
Not:
aggressive exploit software.
This affects:
language
onboarding
Discord
branding
UX tone
Distribution Assumption
Soft-lock:
Discord-first controlled launch
Reason:
Trust advantage.
Benefits:
direct support
feedback loops
real developer presence
visible updates
stronger legitimacy
Website:
later
if validated demand emerges.
Mandatory?
Yes
•
•
•
•
•
•
•
•
•
•
10
Launch blocker:
Yes
M13 — Final Polish & Launch Readiness
Purpose:
intentional finishing.
This phase must exist.
Launch should not be:
code finished
→ ship
Instead:
code stable
→ polish
→ trust pass
→ launch
Product Polish
wording consistency
command clarity
UX consistency
operator confidence
Trust Polish
documentation cleanup
professionalism
onboarding clarity
warnings
Repo Polish
stale docs
naming consistency
cleanup
•
•
•
•
•
•
•
•
•
•
•
11
Launch Polish
Discord structure
support channels
install instructions
FAQ
trust messaging
Mandatory?
Yes
Launch blocker:
Yes
M14 — Controlled Public Launch
Recommended launch model:
Controlled Premium MVP
Meaning:
small
intentional
paid
supervised
trust-first
feedback-driven
Not:
mass market
viral
scale-first
Recommended:
Phase 1
Discord-first launch.
Small community.
Feedback-heavy.
•
•
•
•
•
12
Phase 2
Demand validation.
Support learning.
Bug fixing.
Phase 3
Website formalization (optional).
Only if:
demand validated
support burden grows
trust requirements increase
4. Auto4 Positioning
Current recommendation:
Conditional Pre-Launch Candidate
Meaning:
Not mandatory.
Not rejected.
Conditions:
safely bounded
heavy confirmations
explicit warnings
strong validation
clear Plus positioning
Reasoning:
Risk
High.
13
Core necessity
Low.
User value
Real.
Premium differentiation
Strong.
Conclusion:
build only if safely justified.
Not because:
“might as well.”
5. Complexity Budgeting Philosophy
The project should not ask:
“Is this too complex?”
Instead ask:
Can complexity be bounded?
Can we fail safely?
Can we learn through it?
Is value worth complexity?
Will this create momentum or overload?
Reject unmanaged complexity
Bad:
payments
licensing
website
installer
cloud backend
advanced updater
all at once.
14
Accept bounded complexity
Good:
Discord-first launch
Basic/Plus
Auto4
faster Plus Auto2
trust systems
when:
safely testable.
Complexity is:
allowed when intentionally managed.
6. Deferred Scope Register
Deferred ≠ forgotten.
Deferred
Website
Reason:
Not development-critical yet.
Trigger:
Validated demand.
Deferred
Pricing optimization
Reason:
Too early.
Trigger:
15
Launch preparation.
Deferred
Advanced licensing
Reason:
Complexity too high.
Trigger:
Demand validation.
Deferred
Advanced updater
Reason:
Premature.
Trigger:
Support burden.
Deferred
Broad UI/Desktop expansion
Reason:
CLI currently sufficient.
Trigger:
Post-launch maturity.
Deferred
Advanced Auto3 scaling
Reason:
4-car validation sufficient.
16
Trigger:
Future milestone.
7. Launch Threshold Criteria
Launch should happen when:
Software
 stable
 predictable
 documented
 failure-safe
 trustable
Product
 understandable
 installable
 premium-feeling
 expectation-meeting
Support
 Discord structure exists
 onboarding exists
 troubleshooting path exists
Founder Confidence
 respectful of complexity
 realistic expectations
 willingness to iterate
Important:
Launch threshold is:
good enough to deserve payment
—not—
perfection.
17
8. Failure Modes To Avoid
Failure Mode 1
Scope creep.
Biggest danger.
Failure Mode 2
Perfectionism delay.
“Just one more thing.”
Failure Mode 3
Premature business complexity.
Website, payments, licensing too early.
Failure Mode 4
Overbuilding Plus.
Keep Plus selective.
Failure Mode 5
Trust failure.
Biggest commercial risk.
Trust matters more than capability.
9. Realistic Launch Window
Current assessment:
Strong possibility of launch readiness if milestone discipline remains high.
Risk:
18
Not technical inability.
Risk is:
drift.
Meaning:
too many features
too much complexity
too much delay
Momentum matters.
10. Final Recommendation
Recommended path:
M11.6
↓
M11.7
↓
M11.8
↓
M12
↓
M12.5
↓
M13
↓
M14
Current recommendation:
Stay disciplined. Finish intentionally. Launch conservatively. Learn from reality.
