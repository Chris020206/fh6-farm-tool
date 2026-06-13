# R32 Visual Composition Pass

## Purpose

This checkpoint records a more noticeable presentation-layer pass on the PySide6 vertical companion prototype.

The goal was to make the prototype feel more intentionally composed and less like arranged default Qt widgets.

This is still prototype work.

This is not final styling or branding.

## Goal

Improve visible composition while preserving:

- vertical companion layout
- hover overlay navigation
- stable main content
- no scrolling
- Home as philosophy-first launchpad
- Automation Environment as orientation -> confidence -> commitment
- calm focused premium companion identity

## Refinements Applied

The prototype now uses lightweight custom card surfaces for Home and Automation Environment instead of default-looking group boxes.

Home now has:

- a warmer hero-style launch surface
- calmer card grouping
- a more intentional primary action treatment
- clearer separation between primary, secondary, and tertiary information

Automation Environment now has:

- softer section cards
- quieter secondary and tertiary treatments
- a distinct but calm commitment treatment for Run
- reduced default-widget feel
- clearer visual hierarchy across the six-section structure

The main content canvas now uses a warm companion background rather than a plain default surface.

## Visual Composition Contract

Current prototype contract:

- custom cards are used for the main designed surfaces
- Home hero treatment: `warm quiet launch surface`
- standard card treatment: `soft raised utility card`
- secondary treatment: `muted contextual support`
- commitment treatment: `deliberate calm action`
- background treatment: `warm companion canvas`

Composition principle:

> designed surface over default widgets

## Preserved Boundaries

R32 does not introduce:

- navigation behavior changes
- window size changes
- scrolling
- animation changes
- execution wiring
- runner calls
- real input behavior
- automation logic changes
- safety gate changes
- `main.py` changes
- final branding or logo work

## Current Status

The prototype should now look meaningfully more intentional at first glance.

Further refinement should evaluate:

- whether the card surfaces feel premium enough without becoming decorative
- whether Run needs a stronger affordance later
- whether secondary sections are quiet enough
- whether the Home hero surface should become the visual anchor for the final design direction
