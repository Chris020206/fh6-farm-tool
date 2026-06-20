# Repository Cleanup Backlog

This document records non-feature cleanup that should be handled deliberately.
Items listed here are not authorization to change validated automation,
licensing, packaging, timing, or desktop behavior.

## Maintainability

- Centralize Auto1 max loop constants.
- Avoid retrieving Auto1 entitlement state while rendering Auto2/Auto3.
- Use explicit edition/policy metadata instead of inferring Community versus
  licensed state from numeric limits.
- Keep legacy `FAA.Auto1.*` claim names until a future license-format version.
- Reduce `desktop/companion_shell.py` ownership breadth through behavior-neutral
  extraction after the beta baseline is locked.

## Review Needed

- Confirm whether the branding file ending in `2 - Copy.png` is obsolete
  source artwork before deleting it.
- Decide whether the duplicate logo in `assets/branding/` and
  `desktop/assets/` should be consolidated behind one packaged path.
- Review `core/state/`; it has no consumers outside its own package and no
  direct tests, but ownership should be confirmed before removal.
- Normalize `assets/Guides/` casing only with a packaged-path migration and
  Windows build verification.
- Decide whether historical R-series prototype documents should move into a
  clearly marked archive. Preserve their historical content if moved.
- Archive or explicitly supersede pre-desktop Auto2/Auto3 validation and design
  reports that still describe one-car-only, test-only, or not-yet-implemented
  behavior. Do not rewrite their original validation history in place.
- Retire `desktop/pyside6_shell_prototype.py` only after confirming no external
  developer workflow still uses the compatibility command.
- Add a dependency lock or constraints strategy before reproducible public
  release builds become a requirement.

## Intentionally Retained

- Internal repository/package identifiers containing `fh6_farm_tool`.
- Historical documents that use the former product name.
- Legacy licensing claim identifiers required by license format v1.
- Ignored local build, distribution, output, backup, and cache directories.
