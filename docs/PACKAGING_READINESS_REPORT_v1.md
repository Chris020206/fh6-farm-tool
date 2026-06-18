# FH6 Farm Tool - Packaging Readiness Report v1

## Summary Verdict

FH6 Farm Tool appears ready for a first portable Windows packaging prototype,
but not for public release packaging.

Recommended path:

- use PyInstaller for the first Phase 2 packaging prototype
- build a portable folder first, then zip it
- package the desktop entry point only
- explicitly bundle assets, profiles, config, and required package text files
- validate launch, UI rendering, assets, profiles, and no automation-on-startup
  before any founding tester distribution

Main blockers discovered:

- PyInstaller is not installed in the current environment.
- No dependency file exists yet in the repo root.
- Package text files such as `README_INSTALL.txt`, `SAFETY_AND_TRANSPARENCY.txt`,
  `VERSION.txt`, and `KNOWN_ISSUES.txt` do not exist yet as package-ready files.

No automation behavior needs to change for the first packaging prototype.

---

## Recommended Packaging Tool

Recommendation: PyInstaller.

PyInstaller is appropriate for the current PySide6 desktop app because:

- the project is Python-first
- the desktop app already launches through a Python module
- PyInstaller supports Windows GUI executables
- PyInstaller has established PySide6 hook support
- a folder-based build maps well to the portable zip strategy

Better alternatives for this phase:

- Nuitka may produce stronger compiled output, but it adds complexity too early.
- Briefcase is better suited to app-style distribution workflows, not the
  current portable zip milestone.
- cx_Freeze is viable, but PyInstaller is the simpler first prototype choice.

Phase 2 recommendation:

Use PyInstaller in `--onedir` mode first. Do not start with `--onefile`.

Reason:

`--onedir` is easier to inspect, easier to debug, easier to support, and better
aligned with the current portable beta package structure.

---

## Recommended Entry Point

Current developer launch command:

```powershell
python -B -m desktop.app
```

This is the correct conceptual entry point.

Recommended packaged executable entry point:

```text
desktop/app.py
```

Packaged executable name:

```text
FH6 Farm Tool.exe
```

Import/package path assessment:

- `desktop.app` imports the production-facing desktop shell facade.
- PySide6 imports are mostly lazy inside the desktop launch path.
- Desktop execution adapters import dangerous/manual automation runners lazily
  only during guarded execution paths.
- The package should be built from the repository root so imports resolve as
  package-style imports.

Likely issue:

Several paths are based on `Path(__file__)` or repository-relative directory
structure. A PyInstaller `--onedir` build should work if data folders are copied
beside the packaged executable in a compatible structure. `--onefile` is more
likely to expose path-resolution issues.

---

## Dependency Review

Observed in the current environment:

- PySide6 is installed.
- `keyboard` is installed.
- PyInstaller is not installed.

Likely packaging dependencies:

- PySide6
- keyboard
- standard-library Windows APIs through `ctypes`
- project source packages under `app`, `app_logging`, `automation`, `core`,
  `desktop`, `frontend`, `integrations`, `product`, `profiles`, `sessions`,
  `settings`, and `ui`

PySide6 special requirements:

- Qt platform plugins must be included.
- Image format support should be included for PNG/SVG assets.
- PyInstaller usually handles these through PySide6 hooks, but the prototype
  must verify launch on a clean extracted folder.

Real keyboard backend handling:

- Real keyboard support depends on the optional `keyboard` package.
- Desktop execution paths import real-input dependencies lazily through guarded
  execution adapters and dangerous/manual runner paths.
- Packaging must include `keyboard` if founding tester builds are expected to
  run real Auto1/Auto2/Auto3 execution.
- Real input must not initialize during ordinary app launch.

---

## Required Bundled Files

Required application data:

- `desktop/assets/fh6_farm_tool_logo.png`
- `desktop/assets/chevron_down.svg`
- `assets/branding/` if present
- `profiles/official/`
- `profiles/custom/`
- `config/default_settings.json`

Recommended package documentation files:

- `README_INSTALL.txt`
- `SAFETY_AND_TRANSPARENCY.txt`
- `VERSION.txt`
- `KNOWN_ISSUES.txt`

Current status:

- Desktop assets exist under `desktop/assets/`.
- Branding assets exist under `assets/branding/`.
- Official and custom profiles exist under `profiles/`.
- Config exists under `config/default_settings.json`.
- Package-ready text files still need to be generated or copied from approved
  docs before creating a beta candidate.

---

## Portable Package Structure

Recommended first prototype output:

```text
FH6 Farm Tool v0.2.0-beta/
|-- FH6 Farm Tool.exe
|-- README_INSTALL.txt
|-- SAFETY_AND_TRANSPARENCY.txt
|-- VERSION.txt
|-- KNOWN_ISSUES.txt
|-- assets/
|-- profiles/
|-- config/
|-- logs/
`-- _internal/
```

Notes:

- `_internal/` is expected for a PyInstaller `--onedir` build.
- The exact PyInstaller support-folder name can vary by configuration.
- `logs/` should be present as an empty writable folder if file logging is added
  later; current logging writes to stderr.
- The zip candidate should be named:

```text
FH6_Farm_Tool_v0.2.0-beta.zip
```

---

## Expected Packaging Risks

Likely risks:

- PySide6 platform plugins missing from the packaged output.
- PNG/SVG assets not found because current desktop paths use
  `Path(__file__).with_name("assets")`.
- `profiles/` missing or placed where `ProfileManager` cannot find it.
- `config/default_settings.json` missing or placed where `settings.config_loader`
  cannot find it.
- Hidden imports for dangerous/manual execution modules not detected because
  they are imported lazily inside worker functions.
- `keyboard` package missing from the packaged environment.
- Windows focus handoff behavior needs validation from packaged execution.
- Real keyboard backend must remain lazy and must not initialize on app launch.
- One-file packaging may break file-path assumptions more easily than one-dir.
- Package may include unintended developer files if copied manually.

Current lower risks:

- Logging currently writes to stderr, so no immediate file-log write-path issue
  was found.
- `main.py` startup is separate and remains safe.

---

## First Build Command Recommendation

Install PyInstaller in the packaging environment first.

Initial prototype command direction:

```powershell
python -B -m PyInstaller --noconfirm --clean --windowed --onedir --name "FH6 Farm Tool" `
  --icon "assets/branding/app_icon.ico" `
  --add-data "desktop/assets;desktop/assets" `
  --add-data "assets;assets" `
  --add-data "profiles;profiles" `
  --add-data "config;config" `
  --hidden-import automation.auto1_race.run_auto1 `
  --hidden-import automation.auto2_buy_car.dangerous_auto2_test_mode_real_input_test `
  --hidden-import automation.auto2_buy_car.dangerous_auto2_one_car_purchase_test `
  --hidden-import automation.auto3_skill_tree.dangerous_auto3_multi_car_test_mode_real_input_test `
  --hidden-import automation.auto3_skill_tree.dangerous_auto3_multi_car_unlock_test `
  desktop/app.py
```

Do not overengineer the first build.

Recommended next step after the first successful command:

- convert the working command into a checked-in `.spec` file only after the
  first prototype proves the needed data files and hidden imports.

---

## Validation Checklist

Before calling the packaging prototype successful:

- [ ] Build completes without fatal PyInstaller errors.
- [ ] Packaged `FH6 Farm Tool.exe` launches.
- [ ] Packaged executable uses `assets/branding/app_icon.ico`.
- [ ] Desktop UI opens to the expected Home screen.
- [ ] Window and taskbar icon appear where supported by Windows.
- [ ] Top branding logo is visible.
- [ ] Dropdown arrow asset is visible.
- [ ] Navigation works at a basic smoke-test level.
- [ ] Profiles screen can read official profiles.
- [ ] Settings/config startup path works.
- [ ] App closes cleanly.
- [ ] No automation starts on launch.
- [ ] No real keyboard backend initializes on launch.
- [ ] `main.py` still starts safely from source.
- [ ] Packaged folder can be zipped.
- [ ] Zip can be extracted to a fresh folder and launched.
- [ ] Required package text files are present.
- [ ] Package size is recorded.

Do not run real-input automation as part of this packaging investigation.

---

## Output Expectations

Likely PyInstaller output folder:

```text
dist/FH6 Farm Tool/
```

Expected beta candidate folder:

```text
FH6 Farm Tool v0.2.0-beta/
```

Expected zip candidate name:

```text
FH6_Farm_Tool_v0.2.0-beta.zip
```

Estimated output size:

Unknown until first build. PySide6 folder-based packages are commonly large,
often hundreds of MB. The first prototype should record actual size rather than
optimize early.

---

## Recommended Next Action

Next action:

Create the first PyInstaller `--onedir` packaging prototype in a controlled
local packaging pass.

Before building:

- install PyInstaller in the packaging environment
- generate package-ready text files
- confirm package asset paths
- keep build output out of source control

After building:

- launch the packaged executable
- verify assets, profiles, and config
- record package size
- document packaging issues
- only then decide whether a `.spec` file should be committed

Do not create an installer, updater, tray behavior, public release build, or
new automation capability during this step.
