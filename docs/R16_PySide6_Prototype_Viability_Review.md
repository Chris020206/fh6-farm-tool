# R16 PySide6 Prototype Viability Review

## Purpose

This document evaluates whether the R15 PySide6 shell prototype validates PySide6 as the leading desktop frontend direction for FH6 Farm Tool.

This is a checkpoint and decision review.

No execution behavior, automation wiring, styling system, or production frontend work is introduced in this milestone.

## Evaluation Summary

The R15 prototype successfully validates the following:

- PySide6 can represent the existing shell architecture.
- Sidebar destinations can map cleanly to placeholder screens.
- Weighted content zones can be represented structurally.
- Existing UI architecture models can be consumed without execution coupling.
- The prototype remained narrow and reversible.

Verdict:

> Prototype viability is acceptable.

PySide6 remains the leading frontend candidate.

## Shell Representation Viability

The R15 prototype demonstrates that PySide6 can represent:

- App shell structure.
- Stable sidebar destinations.
- Placeholder screens.
- Primary, secondary, and tertiary content zones.

The prototype aligned with the existing `ui/shell.py` architecture rather than inventing local frontend structure.

This preserves architectural coherence.

## Reversibility Review

The prototype stayed reversible.

Reasons:

- Prototype code is isolated in the `desktop/` package.
- Existing `main.py` behavior was untouched.
- No automation execution was connected.
- No persistence system was introduced.
- No licensing or payment assumptions were added.
- No production styling system was introduced.

The project remains free to:

- Backtrack.
- Replace UI structures.
- Change layouts.
- Adjust navigation.
- Revisit framework direction if necessary.

## Lazy Import Stability

Lazy PySide6 imports successfully preserved test stability.

This means:

- Repository tests do not require a GUI environment.
- PySide6 is not required for standard test execution.
- CI or local verification remains safe.

This is considered a successful architectural decision for the current phase.

## Dependency Handling Review

Dependency handling remains acceptable for the current phase.

Reason:

The repository does not yet have a formal dependency-management structure.

Prematurely introducing one solely for PySide6 would add process overhead before prototype viability was proven.

Carry-forward note:

> Dependency management should be formalized before packaging or broader desktop rollout.

## Safety & Boundary Review

The prototype successfully preserved all major boundaries.

Still excluded:

- Automation execution.
- Runner calls.
- Real input.
- Timing logic.
- CLI behavior changes.
- Safety gate changes.
- Companion mode implementation.
- Licensing and paywall behavior.
- Persistence.
- Final styling.
- Visual polish.

The prototype remained structural rather than behavioral.

## Remaining Risks

PySide6 still introduces real implementation risks:

- Learning curve.
- Styling complexity.
- Packaging complexity.
- Risk of overbuilding too early.

These risks are currently acceptable because implementation scope remains intentionally narrow.

## Carry-Forward Notes

### 1. Operational History Invalid Rendering

Operational history still assumes valid automation/profile IDs.

Future handling should be added before history rendering hardens.

### 2. Auto1 Friction Review

Auto1 acknowledgement level may still be slightly heavy.

Revisit once interaction behavior exists.

### 3. Naming Consistency

Automation IDs and profile automation types still require normalization or clear mapping before frontend display logic hardens.

### 4. Dependency Management

Dependency management still requires formalization before packaging or broader desktop rollout.

## Decision Status

PySide6 remains:

> The leading frontend candidate.

This remains a soft lock.

Final commitment depends on:

- Continued prototype progression.
- Structural viability.
- Packaging viability.
- Maintainability.
- Product coherence.

## Recommended Next Milestone

> R17 — PySide6 Automation Environment Prototype

Goal:

Render the R7 Automation Environment structure using PySide6 while still avoiding execution wiring, automation behavior, or production styling.
