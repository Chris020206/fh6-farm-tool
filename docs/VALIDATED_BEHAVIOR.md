# FH6 Farm Tool - Validated Behavior

## Purpose

This document records manually validated behavior for FH6 Farm Tool. It acts as
an anti-regression boundary for future code, documentation, UI, refactor, and
AI-assisted changes.

Validated behavior must be treated as current source-of-truth behavior unless
explicit approval changes it.

## Scope

This baseline applies to controlled/manual developer use only.

It does not mean public launch readiness, unattended automation readiness, or
broad customer release readiness.

## Auto1 - Validated Baseline

- desktop UI execution validated
- focus handoff success
- focus handoff fail-closed behavior
- F8 stop
- loop count handling
- runtime race duration adjustment
- completion-state behavior
- guarded/manual CLI path still exists

## Auto2 - Validated Baseline

- desktop UI execution validated
- test mode
- purchase mode
- purchase count greater than 1
- F8 stop
- spending-risk protection
- completion-state behavior
- guarded/manual CLI paths still exist

## Auto3 - Validated Baseline

- desktop UI execution validated
- first-car exception
- safety reset navigation
- Recently Added re-sort
- Get In path
- Upgrades & Tuning navigation
- Car Mastery navigation
- locked perk unlock path
- multiple-car traversal
- A1 -> B1 -> C1 -> A2
- row 3 / column 1 -> row 1 / column 2 uses Right -> Up -> Up
- corrected timing model
- completion-state behavior
- max validated cars = 4
- row A start only
- guarded/manual CLI paths still exist

## Anti-Regression Rule

Validated behavior must not be changed, removed, renamed, bypassed, or weakened
without explicit approval.

Any change affecting Auto1, Auto2, or Auto3 execution must preserve the
validated baseline unless the change is explicitly approved and revalidated.

## Boundaries

- no Auto4
- no unattended automation
- no startup automation
- no expansion beyond the validated Auto3 boundary
- no broad public launch readiness claim
