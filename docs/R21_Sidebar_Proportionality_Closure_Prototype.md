# R21 Sidebar Proportionality & Closure Prototype

## Purpose

This checkpoint records the sidebar proportionality and closure experiment inside the PySide6 desktop prototype.

The goal was not to redesign navigation.

The goal was:

> proportional refinement and compositional completion.

## Context

The current prototype appears height-constrained in practice.

Because users should not be expected to resize vertically, sidebar proportionality must work within the actual fixed window height.

Observed issues before R21:

- Navigation occupied too little of the sidebar height.
- Empty vertical space felt unresolved.
- Sidebar lacked a quiet ending element.

## Prototype Adjustment

The sidebar prototype now uses:

- A compact navigation block.
- Stable existing destinations.
- A quiet footer closure.
- Low-emphasis product/system status.

Current footer:

- Controlled MVP.
- Manual operation ready.

This is intended as compositional closure, not filler content.

## Preserved Boundaries

R21 did not introduce:

- Collapse or toggle behavior.
- Navigation redesign.
- Dashboard widgets.
- Assistant-like elements.
- New branding system.
- Execution behavior.
- Runner calls.
- Safety gate changes.
- `main.py` changes.

## Current Verdict

The sidebar now has a clearer beginning, middle, and end.

The compact navigation block should reduce the feeling of deadspace while preserving calmness and stable navigation.

The footer is intentionally restrained and should remain low-emphasis.

## Carry-Forward Notes

- Final visual styling is still postponed.
- Sidebar footer content may need refinement once production status language stabilizes.
- Avoid using sidebar closure as a place for dashboard information.
- Behavioral sidebar features remain deferred.
