# R25 Overlay Hover Navigation Refinement

## Purpose

This checkpoint records the refinement from the R24 toggle-vs-hover comparison into a single hover-to-expand overlay navigation model.

This remains a prototype spike.

It is not final styling and not production UI.

## Decision

Use:

> hover-to-expand only

Reason:

Hover-to-expand feels more natural in the vertical companion layout, provided it does not disturb the main content.

The toggle comparison has been removed from the prototype.

## Interaction Model

Collapsed state:

```text
[ collapsed rail ][ stable main content ]
```

Hover state:

```text
[ expanded navigation overlay ]
[ over left part of stable main content ]
```

The collapsed rail remains spatially reserved on the left.

The expanded navigation floats over the left side of the main content.

Main content must not:

- resize
- compress
- reflow
- jump
- shift

## Animation

The overlay expansion uses a short controlled animation.

Current target:

- `200ms`

This is intended to feel:

- smooth
- calm
- lightweight
- intentional

It should not feel:

- flashy
- sluggish
- twitchy
- clever for its own sake

## Product Fit

This model supports the vertical companion hypothesis by keeping navigation available without making it feel like a dashboard sidebar.

The interaction should preserve:

- focus
- digestibility
- calmness
- subtle guidance
- premium companion identity

## Preserved Boundaries

R25 does not introduce:

- automation execution wiring
- runner calls
- real input behavior
- automation logic changes
- safety gate changes
- `main.py` changes
- final styling
- dashboard/admin behavior

## Current Status

The PySide6 prototype now uses hover-to-expand overlay navigation as the only navigation expansion behavior.

Further evaluation should focus on feel:

- Does it stay calm?
- Does it avoid flicker?
- Does the content remain stable?
- Does it reinforce companion identity?
