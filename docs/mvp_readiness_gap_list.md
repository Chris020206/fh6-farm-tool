# MVP Readiness Gap List

This document lists remaining gaps before the FH6 Farm Tool should be treated
as a controlled MVP, a broader release, or post-MVP work.

## 1. Safety

Required before controlled MVP:

- Keep all real-input commands behind explicit confirmation flags.
- Keep `main.py` safe and free of automation startup behavior.
- Keep F8 stop available in guarded real-input commands.
- Keep refusal-path tests for dangerous commands passing.
- Confirm recovery instructions remain documented for real-input use.

Required before broader release:

- Add clearer user-facing pre-run checks for correct FH6 starting state.
- Add stronger guardrails around commands that can spend credits or skill
  points.
- Improve visibility of active command, selected profile, and stop behavior.

Postponed after MVP:

- Pause/resume.
- F7 start hotkey.
- Any unattended or background automation mode.

## 2. Reliability

Required before controlled MVP:

- Preserve current Auto1, Auto2, and Auto3 validation reports.
- Keep full test suite passing.
- Keep conservative timing values unless a profile-specific validation justifies
  changes.
- Document any new real-input findings before changing flow logic.

Required before broader release:

- Add more automated command refusal and profile-selection tests.
- Add repeatable smoke checks for in-memory CLI commands.
- Add clearer validation around optional real keyboard dependency behavior.

Postponed after MVP:

- Timing optimization.
- Adaptive timing.
- Hardware-specific timing presets.

## 3. Documentation

Required before controlled MVP:

- Keep command index current.
- Keep MVP scope lock current.
- Keep Auto1, Auto2, and Auto3 reliability reports aligned with current
  behavior.
- Keep Auto4 explicitly postponed.

Required before broader release:

- Add a concise user runbook for each real-input command.
- Add troubleshooting guidance for wrong FH6 baseline state.
- Add a clear glossary for official profiles, custom profiles, and dangerous
  commands.

Postponed after MVP:

- Full end-user manual.
- Visual setup guide.
- Release notes template.

## 4. CLI Usability

Required before controlled MVP:

- Keep command summaries and refusal messages consistent.
- Keep dangerous commands explicit about real input and resource spending.
- Keep command wrappers thin and free of automation logic.

Required before broader release:

- Replace module-path command usage with friendlier launcher scripts or packaged
  entry points.
- Improve help output with more complete examples.
- Consider a single command namespace for manual operations.

Postponed after MVP:

- UI/dashboard.
- Interactive command wizard.

## 5. Profile / Settings

Required before controlled MVP:

- Keep official profiles protected from editing.
- Keep custom profile timing edits validation-based.
- Keep backup/restore commands working before further tuning.
- Verify profile selection works for current Auto1, Auto2, and Auto3 manual
  commands.

Required before broader release:

- Harden profile selection lookup behavior for duplicate names or ambiguous
  identifiers.
- Add more tests for missing, wrong-type, and invalid custom profiles.
- Add clearer profile backup recommendations before editing.

Postponed after MVP:

- Profile key editing.
- Profile navigation-count editing.
- Profile import/export.
- Profile UI/editor.

## 6. Auto1

Required before controlled MVP:

- Preserve current guarded manual command behavior.
- Preserve F8 stop and held-key cleanup behavior.
- Keep official and custom profile execution paths working.

Required before broader release:

- Add more command-level smoke tests for profile selection and refusal paths.
- Add clearer FH6 starting-state checklist near the command index.

Postponed after MVP:

- Speed tuning beyond validated profile timing changes.
- UI control surface.

## 7. Auto2

Required before controlled MVP:

- Keep test-mode real-input validation available.
- Keep one-car purchase harness guarded by both confirmation flags.
- Keep full purchase flow and baseline reset documented.

Required before broader release:

- Decide whether and when to promote a production multi-cycle purchase command.
- Add stronger pre-run warnings for credit spending.
- Add more validation around estimated cost.

Postponed after MVP:

- Auto2 production multi-cycle purchase command.
- Purchase UI or confirmation modal.
- Advanced cost management.

## 8. Auto3

Required before controlled MVP:

- Keep Auto3 one-car and guarded 4-car unlock validation documented.
- Keep test modes no-unlock safe.
- Keep unlock harnesses guarded by `--confirm-real-input` and
  `--confirm-unlock`.
- Keep the guarded multi-car unlock hard max at 4 unless a later validation
  milestone explicitly changes it.
- Keep the start-row `A` assumption documented.

Required before broader release:

- Decide whether and when to promote an Auto3 production command.
- Add stronger pre-run checks for the required FH6 baseline and start row.
- Add more validation beyond the current `A1 -> B1 -> C1 -> A2` boundary before
  increasing the hard max above 4.
- Add clearer user-facing warnings for skill-point spending.

Postponed after MVP:

- Auto3 production command.
- Auto3 start-row flexibility.
- Auto3 counts greater than 4.
- Broader validation beyond the current start-row `A` path.
- Auto4 car removal.

## 9. Packaging / Release

Required before controlled MVP:

- No package is required for controlled MVP if commands remain developer/manual
  operated.
- Keep documented module commands accurate.

Required before broader release:

- Add packaging or installer strategy.
- Add dependency installation instructions.
- Add release checklist.
- Add versioned changelog.

Postponed after MVP:

- Signed installer.
- Auto-update.
- Non-technical dashboard-first release.

## Summary

Blocking gaps before controlled MVP are mostly safety/documentation hardening:
accurate docs, passing tests, guarded real-input commands, clear profile
behavior, and preserved startup safety.

Blocking gaps before broader release are larger: friendlier command entry
points, stronger user-facing safeguards, packaging, UI, and more automated
coverage.

Auto3 production operation, Auto3 start-row flexibility, Auto3 counts above 4,
Auto2 production multi-cycle purchase, timing optimization, UI, installer work,
and Auto4 remain outside the controlled MVP boundary.
