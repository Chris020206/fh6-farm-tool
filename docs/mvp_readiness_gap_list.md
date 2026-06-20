# MVP Readiness Gap List

This document lists remaining gaps after the Controlled MVP baseline. The
current project is ready for supervised developer/manual use, not public launch
or unattended automation.

## 1. Safety

Current baseline:

- Auto1, Auto2, and Auto3 real-input execution remains guarded/manual.
- F8 stop is available in guarded real-input paths.
- Refusal-path tests exist for dangerous/manual paths.
- `main.py` remains safe and does not run automation.
- Operator supervision is required.

Remaining gaps:

- Keep pre-run baseline requirements clear in the desktop UI and runbooks.
- Keep spending-risk warnings clear for Auto2 and Auto3.
- Preserve fail-closed behavior when focus handoff, readiness, or execution
  setup fails.
- Continue hardening desktop UI safety language before public launch.

Postponed:

- Unattended automation.
- F7 start hotkey.
- Pause/resume.
- Auto4/remove-car behavior.

## 2. Reliability

Current baseline:

- Auto1 desktop execution is validated.
- Auto2 desktop execution is validated.
- Auto3 desktop execution is validated within the 4-car row-A boundary.
- Conservative timing remains the default reliability strategy.
- The test suite is expected to remain passing.
- `docs/VALIDATED_BEHAVIOR.md` defines the anti-regression baseline.

Remaining gaps:

- Preserve validated behavior during refactors and UI changes.
- Add tests where new desktop state or refusal behavior is introduced.
- Treat timing changes as validation work, not casual cleanup.
- Keep validation reports and runbooks aligned with runtime behavior.

Postponed:

- Major timing optimization.
- Adaptive timing.
- Hardware-specific timing presets.
- Auto3 expansion beyond the validated boundary.

## 3. Documentation

Current baseline:

- `docs/VALIDATED_BEHAVIOR.md` is the anti-regression source of truth.
- Operator runbooks exist for Auto1, Auto2, and Auto3.
- `docs/PROJECT_STATE.md` reflects the current controlled MVP state.
- `docs/engineering_standards.md` reflects current desktop execution
  boundaries.

Remaining gaps:

- Continue realigning older docs with the validated desktop execution surface.
- Keep command index, runbooks, and validation reports synchronized.
- Remove stale wording when implementation reality changes.
- Keep public-launch language separate from controlled/manual MVP language.

Postponed:

- Full end-user manual.
- Visual setup guide.
- Release notes template.

## 4. CLI Usability

Current baseline:

- CLI/manual guarded runners remain valid operator paths.
- Desktop UI is now a validated controlled/manual operator surface.
- CLI is no longer the only operator surface.

Remaining gaps:

- Keep CLI help/refusal messages clear and consistent.
- Keep module-path commands documented for developer/manual use.
- Avoid letting CLI paths bypass desktop or safety boundaries.

Postponed:

- Friendly packaged launcher commands.
- Interactive command wizard.
- Single consolidated command namespace.

## 5. Profile / Settings

Current baseline:

- Official profiles remain protected.
- Custom timing edits remain guarded by profile tooling.
- Runtime UI adjustments are narrow and automation-specific.
- Profile-driven behavior remains the execution model.

Remaining gaps:

- Harden profile lookup behavior for duplicate or ambiguous identifiers.
- Add tests for missing, wrong-type, and invalid custom profiles where gaps
  remain.
- Keep user-facing profile language separate from raw timing internals.

Postponed:

- Profile key editing.
- Profile navigation-count editing.
- Broad profile import/export.

## 6. Auto1

Current baseline:

- Desktop UI execution validated.
- Focus handoff validated.
- Fail-closed behavior validated.
- F8 stop available.
- Runtime race duration adjustment exists.
- Loop count handling exists.
- Completion behavior validated.
- Guarded/manual CLI path still exists.

Remaining gaps:

- Harden public-facing UI wording and baseline guidance.
- Preserve Auto1 validated behavior during desktop refactors.
- Keep runtime adjustment narrow and Auto1-specific.

Postponed:

- Speed tuning beyond validated timing/profile changes.
- Unattended Auto1 operation.

## 7. Auto2

Current baseline:

- Desktop UI execution validated.
- Test mode validated.
- Purchase mode validated.
- Purchase count greater than 1 validated.
- Spending-risk protections remain required.
- Completion behavior validated.
- Guarded/manual CLI paths still exist.

Remaining gaps:

- Harden public-facing purchase warnings and confirmation language.
- Keep requested purchase count visible and understandable before execution.
- Preserve spending-risk protections during UI and execution refactors.

Postponed:

- Unattended purchasing.
- Advanced cost management.
- Broad public launch exposure without stronger safeguards.

## 8. Auto3

Current baseline:

- Desktop UI execution validated.
- First-car exception validated.
- Safety reset logic validated.
- Recently Added re-sort validated.
- Get In path, Upgrades & Tuning navigation, Car Mastery navigation, and locked
  perk path validated.
- Traversal model validated through `A1 -> B1 -> C1 -> A2`.
- Row 3 / column 1 -> row 1 / column 2 uses Right -> Up -> Up.
- Corrected timing model validated.
- Max validated cars = 4.
- Row A start only.
- Completion behavior validated.
- Guarded/manual CLI paths still exist.

Remaining gaps:

- Do not expand beyond 4 cars without explicit approval and validation.
- Do not support row B/C starts without explicit design and validation.
- Keep skill-point risk visible before execution.
- Preserve reset/re-sort and timing behavior during refactors.

Postponed:

- Auto3 counts greater than 4.
- Start-row flexibility.
- Broader traversal validation beyond current row-A boundary.
- Unattended Auto3 operation.

## 9. Packaging / Release

Current baseline:

- A repeatable PyInstaller onedir and ZIP assembly workflow exists.
- The generated portable beta artifact has passed clean-folder validation.
- Desktop UI exists and is validated for controlled/manual use.
- The UI is not public launch-ready.

Remaining gaps:

- Repeatable release-build ownership and release recordkeeping.
- Founding-tester distribution and support validation.
- Versioned release notes and artifact checksum publication.
- Public-launch UX hardening.

Postponed:

- Signed installer.
- Auto-update.
- Public/customer launch packaging.

## Summary

The remaining gaps are now mostly UX hardening, desktop polish,
maintainability, packaging, launch safeguards, and anti-regression discipline.

Auto1, Auto2, and Auto3 automation capability is validated within the current
controlled/manual boundaries. Future work should preserve that baseline rather
than reinterpret it.
