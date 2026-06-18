# FH6 Farm Tool - Packaging Strategy v1

## Purpose

This document defines how beta builds are packaged, versioned, distributed,
updated, and explained to users during Phase 2 - Beta Readiness.

It exists to:

- reduce install friction
- increase trust
- prevent packaging scope creep
- keep beta distribution simple
- avoid premature installer/update complexity

This strategy applies to the founding tester beta, not public launch.

---

## Packaging Decision

Decision: use a portable `.zip` package for the founding tester beta.

Explicitly rejected for now:

- full installer
- auto-updater
- Microsoft Store distribution
- Python/terminal setup for users

Reason:

Portable zip packaging is simpler, easier to inspect, easier to replace, easier
to support, and better suited to a small high-touch beta.

This decision can be revisited after the founding tester beta stabilizes.

---

## Portable App Philosophy

The beta package should behave like a portable Windows app.

User flow:

1. Download zip.
2. Scan zip if desired.
3. Extract folder.
4. Scan extracted folder if desired.
5. Run `FH6 Farm Tool.exe`.

The package should require:

- no registry dependency
- no Windows service
- no background install
- no startup automation
- no account login
- no required installer

---

## Versioning Strategy

Use simple pre-1.0 versioning.

Recommended scheme:

- `v0.1.x` - controlled MVP/internal validation
- `v0.2.x-beta` - founding tester beta
- `v0.3.x-beta` - paid beta
- `v1.0.0` - future public launch candidate

Build naming:

```text
FH6_Farm_Tool_v0.2.0-beta.zip
```

Executable name:

```text
FH6 Farm Tool.exe
```

Each package should include `VERSION.txt`.

`VERSION.txt` should include:

- version number
- release date
- build type
- short changelog
- known compatibility notes if needed

---

## Update Strategy

Decision: use manual zip replacement during the founding tester beta.

Process:

1. New zip is posted in Discord.
2. Announcement is posted with version and changes.
3. User closes the app.
4. User extracts the new version.
5. User replaces the old folder or keeps the old folder as backup.
6. User launches the new exe.

No auto-updater during Phase 2.

Reason:

Auto-updaters increase complexity, trust risk, and failure modes too early.

An installer/update system may be reconsidered after paid beta or before public
launch.

---

## Recommended Package Structure

Target zip structure:

```text
FH6 Farm Tool v0.2.0-beta/
|-- FH6 Farm Tool.exe
|-- README_INSTALL.txt
|-- SAFETY_AND_TRANSPARENCY.txt
|-- VERSION.txt
|-- KNOWN_ISSUES.txt
|-- profiles/
|-- assets/
`-- logs/
```

Exact packaging output may evolve, but every beta build should include clear
install, safety, version, and known-issues information.

---

## Required Package Files

### README_INSTALL.txt

Purpose: simple user install/run guide.

Must include:

- extract zip
- optionally scan zip/folder
- run exe
- required FH6 baseline setup
- F8 stop reminder
- support route through Discord

### SAFETY_AND_TRANSPARENCY.txt

Purpose: plain explanation of what the tool does and does not do.

The tool does:

- send keyboard input
- automate validated FH6 flows
- require user supervision
- provide F8 emergency stop

The tool does not:

- modify FH6 files
- inject into the game
- edit memory
- bypass anti-cheat
- access user accounts
- collect passwords
- require login credentials
- run automation on startup

### VERSION.txt

Purpose: make build identity obvious.

Must include:

- version
- build type
- date
- short changelog
- important notes

### KNOWN_ISSUES.txt

Purpose: reduce support confusion and build trust.

Must include:

- known current limitations
- expected beta issues
- what users should report
- Discord support route

---

## Windows Defender / Antivirus Guidance

Users should be encouraged to scan the downloaded zip and extracted folder with
Windows Security or their preferred antivirus before running the app.

Recommended user flow:

1. Right-click zip.
2. Scan with Windows Security.
3. Extract.
4. Right-click extracted folder.
5. Scan again.
6. Run exe.

A scan reduces risk but does not prove absolute safety.

Because the app is an early beta from a small developer and is not code-signed
yet, Windows SmartScreen or Defender may warn about an unknown publisher or low
reputation.

Do not tell users to blindly ignore warnings.

Do not claim that warnings are impossible.

Do not make absolute safety claims.

Tone should be calm, transparent, and non-defensive.

---

## Trust And Transparency Approach

Principle: trust is part of the product.

The packaging must support the trust model.

Include:

- transparent safety explanation
- recommended antivirus scan
- no hidden install behavior
- no background services
- no startup automation
- no credential collection
- clear known issues
- clear versioning
- Discord support visibility

The product should never ask users to "just trust us."

It should explain clearly what the software does, what it does not do, and how
users can take reasonable precautions.

---

## Tray Scope

Minimal tray support is allowed during Phase 2 as a lightweight legitimacy and
desktop-native polish feature.

Allowed tray scope:

- show/open app
- hide/show app
- exit app
- optional simple ready status

Not allowed in Phase 2:

- start automation from tray
- hidden automation
- background execution
- notification system
- startup-with-Windows
- complex tray state
- update checking

Purpose:

The tray exists to make the app feel like a real desktop utility, not to add
automation capability.

---

## Branding Assets

Branding assets should live under:

```text
assets/branding/
```

Recommended assets:

- app_icon.ico
- app icon
- tray icon
- light logo
- dark logo
- transparent logo

Branding should support:

- executable icon
- tray icon
- Discord visuals
- future installer/website use

Do not allow branding work to delay beta readiness.

---

## Future Installer / Auto-Updater

Installer and updater are explicitly postponed.

They may be reconsidered after:

- founding tester beta stabilizes
- support burden is understood
- paid beta begins or public launch preparation starts

Future possibilities:

- installer
- signed executable
- auto-update system
- website download portal

None are Phase 2 requirements.

---

## Scope Freeze

During Phase 2, packaging work must not expand into:

- auto-updater
- installer polish
- complex launchers
- account/login system
- licensing system
- telemetry
- background services
- website work

If it does not help a founding tester download, trust, launch, or use the app
safely, postpone it.

---

## Exit Condition

Packaging strategy is successful when a founding tester can:

- download the zip
- understand what it is
- scan it if desired
- extract it
- launch the app
- know where to get support
- know how to stop automation
- understand the software is controlled/manual and beta-stage
