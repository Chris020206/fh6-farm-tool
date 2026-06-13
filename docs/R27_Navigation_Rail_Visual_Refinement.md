# R27 Navigation Rail Visual Refinement

## Purpose

This checkpoint records visual refinement to the vertical companion navigation rail and hover overlay.

This is not final styling.

The navigation behavior remains unchanged.

## Locked Behavior Preserved

R27 preserves:

- vertical companion layout
- hover-only navigation
- miniature rail
- reserved collapsed rail space
- expanded navigation overlay
- stable main content
- no main content resize, compression, reflow, or shift
- controlled `200ms` expansion/collapse

## Refinements Applied

The prototype now uses:

- narrower collapsed rail: `64px`
- wider expanded overlay: `184px`
- calmer rail item spacing
- clearer active destination state
- quiet floating panel treatment
- restrained footer/status treatment
- low-emphasis rail appearance

The goal is to make the rail feel:

- intentional
- quiet
- premium
- companion-like
- less placeholder-like

## Design Philosophy

Navigation should remain occasional, not dominant.

The rail should support orientation without making the product feel like:

- a dashboard
- an admin app
- a gamer overlay
- a generic workspace

The current direction favors:

> focused premium companion

over:

> persistent software sidebar

## Non-Goals

R27 does not introduce:

- final visual design
- full styling system
- new navigation behavior
- toggle mode
- execution wiring
- runner calls
- real input behavior
- automation logic changes
- safety gate changes
- `main.py` changes

## Current Status

The rail now has a clearer visual hierarchy and active state while preserving the R25 overlay model.

Further refinement should evaluate:

- vertical rhythm
- typography hierarchy
- Home composition
- Automation Environment readability
