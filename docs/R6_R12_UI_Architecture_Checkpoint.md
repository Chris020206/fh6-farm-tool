# R6-R12 UI Architecture Checkpoint

## Summary

The R6-R12 milestones establish a coherent non-visual UI architecture skeleton for FH6 Farm Tool.

- R6 App Shell: stable sidebar destinations, screen descriptors, and weighted content zones.
- R7 Automation Environment: six-section confidence and commitment structure.
- R8 App Flow: calm transitions from orientation through preparation, running, outcomes, and recovery.
- R9 Profiles: product-facing profile selection structure centered on trusted execution behavior.
- R10 History: recency-first operational memory built from session-oriented history entries.
- R11 Help: question-oriented confidence support.
- R12 Settings: quiet application-level system control.

## Current Architecture Verdict

The non-visual UI architecture skeleton is coherent and ready for:

> R13 - UI Architecture Integration Review

It is not ready for visual design, final frontend styling, or framework implementation yet.

The current layer defines product structure, screen responsibility, and safety-preserving UI data shapes without introducing visual UI or execution wiring.

## Structurally Locked

- Stable sidebar destinations: Home, Profiles, History, Help, Settings.
- Automations are not sidebar tabs.
- Weighted content zones remain primary, secondary, and tertiary.
- Automation Environment uses the six-section structure:
  - Overview
  - Profile
  - Readiness
  - Contextual Warnings
  - Advanced / Refinement Layer
  - Run
- Companion mode is tied to the running state.
- Profiles represent trusted execution behavior.
- History represents operational memory, not raw logs.
- Help represents confidence support, not a documentation center.
- Settings represents quiet system control, not automation tuning.

## Carry-Forward Notes

Operational history currently assumes valid automation/profile IDs.

Future work should add safe handling for invalid or refused previews before history rendering hardens.

Auto1 acknowledgement may be too heavy.

Revisit friction level once interaction and UI behavior exist.

Naming consistency needs review.

Normalize or clearly map automation IDs versus profile automation types before frontend display logic hardens.

## Preserved Hard Boundaries

- No visual UI.
- No styling.
- No frontend framework.
- No automation execution wiring.
- No runner changes.
- No timing changes.
- No real input changes.
- No CLI behavior changes.
- No safety gate changes.

## Recommended Next Milestone

R13 - UI Architecture Integration Review
