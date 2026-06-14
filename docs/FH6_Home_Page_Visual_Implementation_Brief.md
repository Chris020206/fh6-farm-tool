# FH6 Farm Tool — Home Page Visual Implementation Brief

## Purpose

This artifact instructs a lead frontend developer to implement the current **FH6 Farm Tool Home page visual direction** as closely as possible to the latest approved vertical mockup.

The goal is not to invent a new product direction.

The goal is to translate the mockup into a disciplined frontend implementation that preserves the repo's established UI architecture:

- trust-first
- calm operational launch surface
- vertical companion layout
- no dashboard behavior
- no execution wiring changes
- no automation logic changes
- no new product features

---

## 1. Target Experience

The Home page must feel like:

> a calm operational launch surface.

It must not feel like:

- a dashboard
- a control panel
- a settings page
- a statistics screen
- a loud gamer interface
- generic macro software

The user should open the software and immediately feel:

> I understand where I am.  
> This feels controlled.  
> I know what to do next.

The Home page should communicate:

```text
Identity
↓
Orientation
↓
Recommended next action
↓
Context
↓
Quiet reassurance
```

This psychological order matters more than visual decoration.

---

## 2. Implementation Baseline

Use the existing PySide6 prototype as the implementation base.

Current repo-prototype constants to preserve unless intentionally changed:

```python
window_width = 640
window_height = 768
is_fixed_size = True

top_bar.height = 42

navigation_rail.collapsed_width = 64
navigation_rail.expanded_width = 184
navigation_rail.expansion_trigger = "hover"
navigation_rail.animation_duration_ms = 200
navigation_rail.item_height = 34
navigation_rail.item_spacing = 8

vertical_rhythm.content_margin = 18
vertical_rhythm.header_spacing = 8
vertical_rhythm.section_spacing = 14
vertical_rhythm.group_spacing = 10
vertical_rhythm.group_inner_margin = 10
vertical_rhythm.important_element_spacing = 16
```

Important:

The visual mockup is aspirational, but the implementation should remain anchored to the actual fixed vertical companion shell unless a later milestone explicitly changes dimensions.

---

## 3. Global Visual Identity

### Visual DNA

```text
Identity: Technical Companion
Mood: Calm, premium, focused, intentional, confident
Base: dark graphite / light black
Secondary: restrained light greys
Accent: confident pink
Shape: soft rounded
Depth: soft layered depth
Borders: subtle precision borders
Glass/blur: none
Texture: none
```

### Must Avoid

```text
No gamer RGB
No dashboard clutter
No glassmorphism
No carbon fiber
No fake luxury
No heavy gradients everywhere
No oversized statistics
No loud execution language
No "START NOW" aggression
```

---

## 4. Color System

Use semantic tokens. Do not hardcode one-off colors throughout the UI.

### Core Tokens

```text
color.surface.root        = #0F1115
color.surface.base        = #17191E
color.surface.rail        = #111318
color.surface.topbar      = #101217
color.surface.card        = #1E2128
color.surface.cardRaised  = #262B35
color.surface.cardSoft    = #20242C
color.surface.recessed    = #191C22

color.border.subtle       = #353A46
color.border.strong       = #444B59
color.border.active       = #F21A87

color.text.primary        = #E7E9EE
color.text.secondary      = #B1B8C4
color.text.muted          = #7C8593
color.text.faint          = #5F6673

color.accent.primary      = #F21A87
color.accent.hover        = #FF4FA5
color.accent.pressed      = #C8146D
color.accent.softTint     = rgba(242, 26, 135, 0.12)
color.accent.mediumTint   = rgba(242, 26, 135, 0.20)
```

### Accent Rule

Pink is a **precision signal**, not decoration.

Use pink for:

- active nav item
- selected state
- primary CTA
- focus ring
- key status dot
- important icon strokes
- one hero accent treatment

Do not use pink for:

- large full backgrounds
- every border
- all icons at once
- decorative noise
- uncontrolled glow

Pink should occupy roughly **5–10% of the visible UI**.

---

## 5. Shell Layout

### Overall Structure

```text
┌──────────────────────────────┐
│ Top Product Bar              │ 42px
├──────┬───────────────────────┤
│ Rail │ Home Content          │
│ 64px │ fixed vertical canvas │
└──────┴───────────────────────┘
```

### Window

```text
Width: 640px
Height: 768px
Fixed size: yes
Scrolling: no
```

The product should feel like a **vertical companion utility**, not a wide desktop dashboard.

---

## 6. Top Product Bar

### Purpose

Anchor product identity.

It should subtly say:

> you are inside FH6 Farm Tool.

### Visual Requirements

```text
Height: 42px
Background: color.surface.topbar
Bottom border: color.border.subtle
Horizontal padding: 16px
```

### Content

Left side:

```text
FH6  Farm Tool
```

Recommended treatment:

- `FH6` in accent pink
- `Farm Tool` in primary text
- compact spacing
- no giant logo
- no hero treatment

Right side:

- optional native window controls only
- optional tiny status later
- keep quiet

### Avoid

- large hero banner
- corporate ribbon
- gamer HUD
- complex status widgets

---

## 7. Navigation Rail

### Purpose

Intentional navigation, not exploration.

Collapsed state:

```text
Width: 64px
Low noise
Icon-only
Active item visible
```

Expanded hover state:

```text
Width: 184px
Hover overlay
Does not resize main content
Animation: 200ms
```

### Behavior

Required:

```text
Collapsed rail reserves 64px.
Expanded navigation overlays main content.
Main content must not reflow, resize, compress, or shift.
```

### Visual Requirements

Collapsed rail:

```text
Background: color.surface.rail
Right border: color.border.subtle
Content padding: 8px horizontal, 12px vertical
Item height: 34px
Item spacing: 8px
```

Active nav item:

```text
Soft rounded selection
Accent pink icon/text
Subtle pink left indicator or tinted background
No loud glow
```

Footer closure:

```text
Controlled MVP
Manual operation ready
```

This is structural closure, not dashboard information.

---

## 8. Home Content Layout

### Top-Level Order

The Home content must follow this order:

```text
Screen title
Opening statement
Hero surface
Recommended next step card
Review / plan card
Recent context + quiet status row
Footer metadata
```

### Main Content Padding

Use repo rhythm:

```text
Content margin: 18px
Header spacing: 8px
Section spacing: 14px
Important spacing: 16px
Group spacing: 10px
```

### Header

Text:

```text
Home
Overview and next steps for your farming operations.
```

Style:

```text
Title: 20px, 650 weight, primary text
Subtitle: 12–13px, secondary text
```

Do not make Home title dramatic.

---

## 9. Hero Surface

### Purpose

Psychological anchoring.

The hero says:

> Here is the state of the system.

It should be operational, not motivational.

### Text

Preferred:

```text
Ready when baseline conditions are clear.
Controlled preparation before supervised operation.
System ready
```

Alternative shorter implementation if space is tight:

```text
Ready when the baseline is clear.
Quiet confidence before operational commitment.
System ready
```

### Layout

Hero card should appear immediately below header.

Recommended:

```text
Width: full content width
Height: approximately 132–150px
Radius: 18–20px
Border: color.border.subtle
Background: layered dark surface
```

Composition:

```text
Left: large check/status icon
Center: heading + support text + status pill
Right: restrained pink radial/arc accent, very subtle
```

### Visual Treatment

Use:

```text
Dark card base
Subtle inner contrast
Pink accent only on status icon / right-side accent
No heavy glow
No animated particles
No texture
```

The hero is important, but it must not overpower the primary action below.

---

## 10. Primary Action Zone

### Purpose

Remove ambiguity.

The user should immediately know what to do next.

### Card 1 — Recommended Next Step

Text:

```text
RECOMMENDED NEXT STEP
Prepare a supervised run
Review baseline, requirements and environment before starting.
Button: Prepare a Run
```

Visual treatment:

```text
Most important action card
Accent border or accent top/left treatment
Soft raised card
Pink CTA button
```

Important:

This card should be more visually dominant than the Review / Plan card.

Recommended hierarchy:

```text
Recommended card: 60% perceived importance
Review card: 40% perceived importance
```

In the vertical companion layout, this can be achieved by stacking cards vertically and making the recommended card use accent border + stronger CTA.

### Card 2 — Review & Plan

Text:

```text
REVIEW & PLAN
Review profile and readiness
Check profile, readiness, warnings and commitment before proceeding.
Button: Open Review
```

Visual treatment:

```text
Same family as primary card
Lower contrast than recommended card
No pink border unless hovered/focused
Button should be secondary/outline
```

---

## 11. Secondary Context Zone

### Purpose

Reassurance without clutter.

This is not logs, analytics, or statistics.

### Layout

Two small cards in one row if space allows:

```text
Recent Context | Quiet Status
```

If implementation constraints require stacking, keep both low emphasis.

### Recent Context Card

Text:

```text
RECENT CONTEXT
Last prepared:
Auto1 / supervised baseline
```

Visual treatment:

```text
Small
Muted
No action button
Optional quiet document/history icon
```

### Quiet Status Card

Text:

```text
QUIET STATUS
Controlled MVP
Manual operation ready
```

Visual treatment:

```text
Lowest emphasis
Almost footer-like
Very subtle pink check icon allowed
```

Psychological purpose:

> subconscious reassurance.

If this card attracts too much attention, it is too loud.

---

## 12. Footer Metadata

At the bottom of the Home content, include low-emphasis metadata:

```text
• FH6 Farm Tool • v0.1.0 • Local Mode
```

Style:

```text
10–11px
Muted text
Accent dot optional
Border-top optional
```

This should feel quiet, not like a status dashboard.

---

## 13. Typography

Use Segoe UI unless the frontend strategy changes.

Current repo hierarchy:

```text
Screen title:        20px
Opening statement:  13px
Section title:       13px
Summary:             12px
Detail:              11px
Navigation:          12px
Footer:              10px
```

Recommended visual adjustment for the polished mockup:

```text
Home title:             22–24px only if vertical fit remains clean
Hero heading:           18–20px
Primary card heading:   17–19px
Card eyebrow label:     10–11px, uppercase, letter-spaced
Body text:              12–13px
Footer/status:          10–11px
```

Principle:

> Scan first, detail second.

Avoid:

- huge dramatic headings
- equal-weight text everywhere
- fake luxury typography
- dense paragraphs

---

## 14. Shape / Radius System

Use soft rounded shapes.

```text
App window:      18–22px if custom-frameless window is used
Hero card:       18–20px
Primary cards:   18–20px
Small cards:     14–16px
Buttons:         12–14px
Pills/chips:     10–12px
Nav items:       12–14px
```

Avoid:

- sharp admin UI
- over-rounded bubbly UI
- inconsistent radius values

---

## 15. Depth / Borders

### Depth

Use soft depth only.

```text
Main canvas: mostly flat
Cards: subtle lift
Primary CTA: slightly stronger presence
```

No heavy drop shadows.

### Borders

Use subtle visible borders.

```text
Standard card border: color.border.subtle
Active/primary border: color.accent.primary
Secondary border: lower contrast
```

Active states should rely more on:

```text
pink accent + subtle tint
```

than on heavy shadow.

---

## 16. Icons

Use line icons only.

Style:

```text
Stroke: 1.75–2px
Rounded line caps
No filled gaming icons
No emoji-style icons
No complex illustration
```

Icon meanings:

```text
Home: house
Recommended: flag
Review: clipboard
Recent: clock/document
Status: shield/check
Settings: gear
Help: question mark
History: simple chart/log icon
```

Accent rules:

```text
Only active icon or key action icon should be pink.
Inactive icons should be muted grey.
```

---

## 17. Interaction States

### Buttons

Primary button:

```text
Background: color.accent.primary
Hover: color.accent.hover
Pressed: color.accent.pressed
Text: near-white or very dark only if contrast is verified
Radius: 12–14px
```

Secondary button:

```text
Transparent or dark surface
Border: color.border.strong
Text: color.text.primary
Hover: slight surface lift or border brightening
```

### Cards

Hover behavior should be subtle.

Allowed:

```text
border slight brightening
very slight surface lift
```

Not allowed:

```text
large movement
large glow
color flashing
```

### Navigation

Collapsed rail hover expands overlay in 200ms.

Overlay must not shift main content.

---

## 18. Copy Rules

The UI must sound calm and operational.

Use:

```text
Prepare
Review
Baseline
Readiness
Supervised
Controlled
Manual operation ready
```

Avoid:

```text
Start now
Launch
Boost
Farm hard
Hack
Exploit
Maximize
Dominate
Insane
```

Primary CTA should remain:

```text
Prepare a Run
```

Not:

```text
Start Automation
```

This is critical because the Home page represents preparation, not direct execution.

---

## 19. Non-Goals

Do not add:

- automation execution wiring
- runner calls
- real keyboard input changes
- timing changes
- safety gate changes
- new automation features
- profile editing
- licensing
- payment/paywall logic
- dashboard analytics
- scrollable Home page
- wide desktop dashboard layout

This artifact is visual/frontend guidance only.

---

## 20. Acceptance Criteria

A lead frontend implementation is acceptable when:

1. The app opens as a fixed vertical companion shell around `640 × 768`.
2. The top product bar anchors identity quietly.
3. The rail is 64px collapsed and expands to 184px on hover.
4. The rail expansion overlays content without reflow.
5. Home is fully understandable in roughly 3 seconds.
6. Home does not require scrolling.
7. The hero surface feels calm, operational, and trust-building.
8. The recommended next step is visually dominant.
9. The review/planning pathway is visible but secondary.
10. Recent context and quiet status are low-emphasis reassurance.
11. Pink `#F21A87` is used as a restrained signature accent.
12. The interface does not look like a dashboard, gamer app, or generic macro tool.
13. No automation behavior is changed.
14. All styling is tokenized or centralized, not scattered as one-off values.
15. The implementation still respects existing product-facing screen structures.

---

## 21. Developer Note

The current prototype already contains many structural values and product-facing concepts.

The task is not to redesign the architecture.

The task is to upgrade the Home surface to match the approved visual direction:

> dark graphite vertical companion  
> restrained grey hierarchy  
> confident pink accent  
> soft rounded cards  
> clean, no texture  
> calm operational launch surface

Implement visually, but protect the system philosophy.
