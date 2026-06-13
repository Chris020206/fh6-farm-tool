# R14 Desktop Frontend Technology Decision

## Purpose

This document records the desktop frontend technology direction for FH6 Farm Tool and defines a reversible experiment plan.

This is a planning checkpoint only.

PySide6 is not implemented in this milestone.

## Product Requirements

The frontend technology must support:

- Windows-first desktop app behavior.
- A premium utility feel.
- Stable sidebar shell architecture.
- Existing Python product architecture.
- Companion or reduced running mode.
- Future licensing and paywall support.
- Local settings.
- Controlled automation safety.
- Eventual commercial packaging.
- Frontend adaptability and backtracking.

The frontend must preserve the established non-visual architecture:

- Home, Profiles, History, Help, Settings.
- Automations as product destinations, not sidebar tabs.
- Weighted primary, secondary, and tertiary content zones.
- Automation Environment confidence flow.
- Safety boundaries around execution.

## Options Reviewed

### PySide6 / Qt

PySide6 is the leading candidate.

It is a mature Python desktop UI option with strong layout control, good native desktop potential, and enough depth for a refined commercial utility.

### CustomTkinter

CustomTkinter is a faster and simpler option.

It may be useful for quick internal tooling, but it is weaker for the long-term product direction.

### Web Frontend Wrapper

Electron/Tauri-style wrappers remain possible, but are deferred.

They introduce more stack complexity than the current project needs at this stage.

## Recommendation

Use PySide6 / Qt as the leading candidate for the first desktop frontend prototype.

This is a soft lock, not a final irreversible commitment.

Final commitment should happen only after a small prototype proves viability against the current architecture.

## Why PySide6 Fits

PySide6 fits the current product direction because it supports:

- Stronger long-term desktop polish.
- Good shell, sidebar, and layout control.
- Direct Python integration with the existing product layer.
- Companion window flexibility.
- A more commercial desktop utility feel than lightweight macro-tool UI libraries.

PySide6 also fits the current repository shape because the product-facing data layer, frontend-safe controller, and non-visual UI models already exist in Python.

## PySide6 Risks

PySide6 carries real implementation risks:

- Learning curve.
- Styling complexity.
- Packaging complexity.
- Risk of overbuilding too early.

The first experiment must stay narrow to prevent framework exploration from becoming visual design or product expansion.

## Why CustomTkinter Is Weaker

CustomTkinter is attractive for speed, but weaker for the intended product identity.

Main concerns:

- Faster initial progress, but less premium.
- Higher risk of feeling like macro utility software.
- Less long-term polish and layout flexibility.
- More likely to constrain the final desktop experience.

CustomTkinter remains a fallback only if PySide6 proves too costly or unsuitable during the prototype spike.

## Why Web / Electron / Tauri Is Deferred

A web frontend wrapper is deferred because it would add:

- Stack complexity.
- Python integration overhead.
- More packaging and communication surface.
- Heavier infrastructure than needed for the next step.

This option should be reconsidered only if PySide6 cannot support the desired desktop polish, companion behavior, or future commercial packaging path.

## Frontend Adaptability Rule

The frontend must be able to absorb product and backend changes without requiring broad rewrites.

The implementation must allow:

- Backtracking.
- Restructuring.
- New backend fields.
- Changed screen structures.
- New product states.
- Evolving automation data.
- Evolving profile metadata.
- Evolving readiness and history models.

The frontend must not hardcode product meaning locally when the repository already provides product-facing structure.

## Experiment Plan

The first PySide6 experiment should render only:

- App window.
- Stable sidebar.
- Placeholder screens.
- Basic navigation.
- Weighted content zones as placeholders.

The experiment should prove:

- PySide6 can represent the existing shell architecture cleanly.
- Navigation can map to current screen descriptors.
- Primary, secondary, and tertiary zones can be represented without visual clutter.
- The UI can consume product-facing structures without touching automation execution.

## Explicit Non-Goals For First Experiment

The first PySide6 experiment must not include:

- Final styling.
- Visual polish.
- Automation execution.
- Runner calls.
- Real input.
- Profile editing.
- Persistence.
- Licensing.
- Payment or paywall logic.
- Companion mode implementation.

## Decision Status

PySide6 / Qt is soft-locked as the leading candidate.

Final commitment depends on prototype viability.

If the prototype shows structural or packaging risk that conflicts with the product direction, the frontend choice remains reversible.

## Recommended Next Milestone

R15 - PySide6 Shell Prototype Spike

Goal:

Create a narrow, reversible PySide6 prototype that renders the shell, sidebar, placeholder screens, and weighted content zones without adding execution behavior or final visual design.
