# R19 Home Screen Philosophy & Prototype Review

## Purpose

This checkpoint records the current Home direction before deeper frontend expansion continues.

Primary question:

> What should opening FH6 Farm Tool feel like?

## Decision

Home should be a philosophy-first launch environment, not an automation dashboard.

Preferred direction:

> Quiet launchpad with a slight premium control-room feeling.

Home should make the product feel calm, intentional, and trustworthy before the operator enters a specific Automation Environment.

## Home Role

Home is responsible for:

- Calm orientation.
- Subtle guidance.
- A small number of relevant next signals.
- Quick path into focused automation preparation.
- Quiet confidence before operational commitment.

Home is not responsible for:

- Detailed readiness review.
- Full automation preparation.
- Live monitoring.
- Dense dashboard status.
- Broad operational analytics.
- Assistant-like coaching.

## Prototype Structure

The PySide6 prototype now represents Home as a single-frame launchpad.

The current Home concept includes:

- Recommended Next Step.
- Quick Automation Access.
- Relevant Activity.
- Quiet Status.

These are intentionally lightweight placeholders. Their purpose is to test hierarchy and feel, not final content or final styling.

## Relationship To Automation Environment

Home and Automation Environment should feel meaningfully different.

Home:

- Broad orientation.
- Product philosophy.
- Calm launch intent.

Automation Environment:

- Specific automation preparation.
- Readiness confidence.
- Profile and warning review.
- Deliberate run commitment.

This separation should prevent Home from becoming a dashboard while preserving a clear path into automation preparation.

## Current Verdict

The current Home prototype direction is viable enough to continue.

It preserves:

- Non-scrollable single-frame intent.
- Quiet confidence.
- Subtle guidance.
- No dashboard energy.
- No execution behavior.

## Hard Boundaries Preserved

- No automation execution wiring.
- No runner calls.
- No real input.
- No timing changes.
- No companion mode implementation.
- No persistence.
- No licensing or paywall behavior.
- No `main.py` changes.
- No safety gate changes.

## Carry-Forward Notes

- Home content should remain sparse.
- Sidebar proportionality and closure still need later review.
- Final visual refinement is still postponed.
- Home should not absorb Automation Environment responsibilities.

## Recommended Next Step

Continue frontend expansion only if Home remains calm, non-dashboard-like, and structurally distinct from Automation Environment.
