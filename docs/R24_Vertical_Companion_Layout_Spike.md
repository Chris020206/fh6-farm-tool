# R24 Vertical Companion Layout Spike

## Purpose

This spike tests whether FH6 Farm Tool feels more like itself as a vertical companion utility.

This is a prototype spike only.

It is not a redesign commitment.

## Context

Automatic FH6 focus handoff now works reliably enough to weaken the earlier layout assumption that FH6 Farm Tool must physically sit beside the game for manual focus handoff.

This gives the product more freedom to prioritize:

- focus
- digestibility
- intentionality
- calmness
- subtle guidance
- companion identity
- product uniqueness

## Hypothesis

A vertical companion layout may better express:

> focused premium companion

rather than:

> generic software workspace

The goal is not maximum content density.

The goal is:

> restrained, digestible operation inside an intentional companion window.

## Prototype Direction

The PySide6 prototype now uses:

- fixed vertical window: `640 x 768`
- miniature navigation rail
- toggle-to-expand navigation by default
- hover-to-expand navigation as a comparison mode
- existing Home philosophy-first launchpad
- existing Automation Environment structure

The layout remains intentionally simple and structural.

## Navigation Rail

The persistent sidebar experiment has been replaced by a miniature navigation rail for this spike.

Default behavior:

> toggle-to-expand

Reason:

Toggle is more predictable and trust-first.

Alternative prototype behavior:

> hover-to-expand

Reason:

Hover is included only for comparison. It is not assumed to be the preferred direction.

## How To Run

Default toggle mode:

```powershell
python -B -m desktop.pyside6_shell_prototype
```

Hover comparison mode:

```powershell
python -B -m desktop.pyside6_shell_prototype --navigation-mode hover
```

## Evaluation Questions

- Does the product feel more companion-like?
- Does Home still feel calm and philosophy-first?
- Does Automation Environment remain clear and digestible?
- Does the navigation rail feel restrained rather than clever?
- Does the vertical format reduce dashboard/workspace energy?
- Does any content feel cramped enough to challenge the direction?

## Preserved Boundaries

R24 does not introduce:

- automation execution wiring
- runner calls
- real input behavior
- timing changes
- safety gate changes
- automation logic changes
- `main.py` changes
- final styling
- production visual design

## Current Status

The vertical companion layout is implemented as a reversible prototype path.

It should be evaluated by feel before further frontend commitment.
