# R26 Vertical Companion Foundation Review

## Purpose

This checkpoint records the outcome of the R24–R25 vertical companion experiments.

Goal:

> Determine whether the vertical companion direction feels more aligned with FH6 Farm Tool’s philosophy than the earlier horizontal utility direction.

This milestone is intentionally evaluative.

No automation execution, runner calls, real input behavior, automation logic, safety gates, or main.py behavior were changed.

---

## High-Level Verdict

Current status:

> Vertical companion layout is now the leading product direction.

Not fully locked.

But strongly favored.

Reason:

The prototype increasingly feels:

> more like FH6 Farm Tool.

rather than:

> a generic desktop application.

This is considered a meaningful product identity discovery.

---

## Major Findings

### 1. Vertical Layout Feels More Purpose-Built

Observed feeling:

> focused premium companion

rather than:

> software workspace.

The vertical format appears to improve:

- focus
- digestibility
- calmness
- subtle guidance
- uniqueness
- intentionality

It also reduces the feeling of:

- dashboard energy
- workspace sprawl
- unnecessary horizontal expansion

This aligns strongly with the product philosophy.

---

### 2. Navigation Should Feel Occasional, Not Persistent

Earlier assumption:

> Persistent sidebar creates stability.

Updated understanding:

> Stability can exist without persistent navigation when navigation is intentional and occasional.

The miniature navigation rail appears philosophically stronger in the vertical format.

Reason:

Navigation switching is not expected to be constant.

Users primarily:

```text
Home
↓
Automation Environment
↓
Profiles
↓
Back to Home
```

Navigation exists to support operation.

Not dominate it.

---

### 3. Hover Overlay Navigation Is Stronger Than Toggle

Earlier experiment:

- Toggle-to-expand
- Hover-to-expand

Observed result:

> Hover-to-expand feels better.

Updated direction:

> Hover-only navigation.

Reason:

Hover expansion feels:

- calmer
- lighter
- more refined
- more premium
- less operationally heavy

provided:

> main content remains stable.

Toggle mode is no longer the leading direction.

---

### 4. Stable Main Content Is Important

A critical refinement insight emerged.

Incorrect direction:

> sidebar expansion compresses or reflows content.

Why this felt wrong:

- instability
- visual jumpiness
- unnecessary complexity
- weaker refinement feeling

Correct direction:

```text
[ reserved rail ][ stable main content ]
```

On hover:

```text
[ expanded overlay navigation ]
[ over left side of stable content ]
```

Main content remains:

> spatially stable.

This is now considered an important design rule.

---

### 5. Motion Quality Matters

Hover expansion quality significantly influences perceived refinement.

Poor behavior:

- flicker
- twitchiness
- instant jump
- sluggish expansion

Current direction:

> fast but controlled motion.

Current prototype:

> ~200ms expansion/collapse.

Observed interpretation:

This contributes positively to:

- refinement
- premium feeling
- trust
- calmness

Motion is not decorative.

It communicates product quality.

---

## Important Clarification

“Floating navigation” does NOT mean:

> collapsed rail overlays content.

Correct interpretation:

The collapsed rail keeps its own reserved space.

Only the expanded navigation overlays content.

This distinction matters for maintaining:

> compositional stability.

---

## Remaining Reality Check

The prototype still requires:

> visual refinement.

Observed sentiment:

> Foundationally speaking this feels peak.

But:

> visually it still needs refinement.

This is considered a good sign.

Reason:

Architecture problems are harder than visual refinement.

The product now appears to have:

> a strong behavioral foundation.

---

## Carry-Forward Design Rules

Preserve:

1. Vertical companion direction.
2. Hover-only navigation.
3. Miniature navigation rail.
4. Stable main content.
5. Overlay expansion.
6. Calm premium motion.
7. Non-dashboard Home philosophy.
8. Companion identity over workspace identity.
9. Focus-first information density.
10. Space must justify itself.

---

## Recommended Next Phase

Shift emphasis from:

> architecture

Toward:

> compositional refinement.

Candidate milestones:

- R27 — Navigation Rail Visual Refinement
- R28 — Vertical Spacing & Visual Rhythm
- R29 — Typography Hierarchy
- R30 — Home Screen Composition Refinement
- R31 — Automation Environment Vertical Readability

Current recommendation:

> Continue with R27.

Vertical companion direction should be treated as:

> the leading candidate unless future testing strongly disproves it.