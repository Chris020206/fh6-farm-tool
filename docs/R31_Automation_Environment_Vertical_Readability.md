# R31 Automation Environment Vertical Readability

## Purpose

This checkpoint records readability refinement for the Automation Environment screen inside the vertical companion prototype.

This is not a redesign.

This is not final styling.

## Goal

Improve the ability to scan:

- Overview
- Profile
- Readiness
- Contextual Warnings
- Advanced / Refinement
- Run

while preserving the trust-first structure:

> Orientation -> Confidence Formation -> Commitment

## Refinements Applied

The prototype now reduces equal-weight text by limiting visible supporting details per section.

The primary sections remain:

- Overview
- Profile
- Readiness
- Run

Warnings remain contextual and secondary.

Advanced remains tertiary and collapsed-feeling.

Visible card titles were simplified by removing structural role prefixes from Automation Environment section headings. The underlying section metadata still preserves primary, secondary, and tertiary weighting.

## Readability Treatments

Current treatments:

- Overview: `primary orientation`
- Profile: `primary behavior summary`
- Readiness: `primary confidence check`
- Contextual Warnings: `secondary contextual support`
- Advanced / Refinement: `tertiary collapsed refinement`
- Run: `primary deliberate commitment`

These treatments are prototype metadata only. They do not change automation behavior.

## Preserved Direction

R31 preserves:

- vertical companion layout
- fixed window size
- hover overlay navigation
- stable main content
- no scrolling
- six-section Automation Environment structure
- Advanced as secondary/collapsed-feeling
- Warnings as contextual
- Run as deliberate but not aggressive

## Non-Goals

R31 does not introduce:

- navigation behavior changes
- window size changes
- scrolling
- execution wiring
- runner calls
- real input behavior
- automation logic changes
- safety gate changes
- `main.py` changes
- final styling

## Current Status

The Automation Environment should now feel less text-heavy and easier to read top-to-bottom.

Further refinement should evaluate:

- whether the Run section needs stronger visual affordance later
- whether Readiness needs progressive disclosure
- whether Warnings should remain hidden when empty
- whether Advanced should become a true collapsed control in a later UI milestone
