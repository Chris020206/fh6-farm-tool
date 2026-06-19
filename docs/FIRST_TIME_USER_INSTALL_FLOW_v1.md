# Forza Automation Assist - First-Time User Install Flow v1

## Purpose

This document describes the expected experience of a first-time founding
tester.

It exists to:

- identify onboarding friction
- improve trust
- reduce support burden
- improve install success rates
- improve first-run success rates

This flow represents the intended founding tester experience during Phase 2 and
Phase 3.

---

## User Assumptions

Assume the user:

- has never spoken to the developer
- has never used Forza Automation Assist before
- has limited knowledge of the project
- may be cautious about downloading automation software
- may not understand the difference between automation and cheating
- may not understand FH6 baseline requirements

The flow should assume reasonable skepticism.

---

## Stage 0 - Discovery

Possible sources:

- Instagram
- YouTube
- Discord invite
- forum post
- friend recommendation

User question:

"What is this?"

Success criteria:

Within a short time the user understands:

- Forza Automation Assist
- supervised automation
- Forza Horizon 6 utility
- not a cheat
- not a mod
- not account sharing

Potential concerns:

- malware
- bans
- legitimacy
- trust

---

## Stage 1 - Discord Arrival

User joins Discord.

Expected channels:

- welcome
- software showcase
- how it works
- download and install
- FAQ

User goals:

- understand the product
- understand access requirements
- determine whether the project appears legitimate

Success criteria:

User understands:

- what the software does
- what it does not do
- how to get access
- where to ask questions

Potential friction:

- confusing explanations
- unclear terminology
- missing trust information

---

## Stage 2 - Download Decision

User reaches download information.

User evaluates:

- version
- requirements
- trustworthiness
- support availability

User question:

"Can I trust this?"

Trust assets should include:

- transparency messaging
- safety explanation
- support route
- known issues
- update information

Success criteria:

User understands the software before downloading.

---

## Stage 3 - Download

User downloads:

```text
Forza_Automation_Assist_v0.2.x-beta.zip
```

Success criteria:

User understands:

- this is a portable application
- no installer is required
- updates are manual
- the software is currently beta-stage

Potential friction:

- expectation of installer
- uncertainty about zip distribution

---

## Stage 4 - Safety Verification

Recommended flow:

1. Scan zip.
2. Extract zip.
3. Scan extracted folder.
4. Launch application.

User should understand:

- scanning is encouraged
- scanning is optional
- transparency is encouraged
- the software should not require blind trust

Success criteria:

User feels comfortable verifying the download before execution.

---

## Stage 5 - Extraction

User extracts package.

Expected package contents:

- `Forza Automation Assist.exe`
- `README_INSTALL.txt`
- `SAFETY_AND_TRANSPARENCY.txt`
- `VERSION.txt`
- `KNOWN_ISSUES.txt`

Success criteria:

Folder structure appears intentional and understandable.

Potential friction:

- missing documentation
- confusing file layout

---

## Stage 6 - First Launch

User launches:

```text
Forza Automation Assist.exe
```

User question:

"What do I do now?"

Goals:

- immediate clarity
- clear navigation
- obvious next action

Potential future onboarding opportunities:

- first-run guidance
- FH6 baseline reminders
- F8 explanation

---

## Stage 7 - Feature Understanding

User learns:

### Auto1

Purpose: race automation.

### Auto2

Purpose: buy-car automation.

### Auto3

Purpose: skill-tree automation.

Success criteria:

User understands:

- purpose
- required FH6 baseline
- expected result

This should not require deep documentation study.

---

## Stage 8 - First Execution

User prepares FH6.

User selects:

- Auto1
- Auto2
- Auto3

Critical understanding:

- required FH6 state
- F8 stop
- expected behavior
- expected completion

Success criteria:

User completes a successful first run.

Potential friction:

- wrong FH6 state
- misunderstanding baseline requirements
- misunderstanding expected results

---

## Stage 9 - Problem Occurs

Assumption: problems will occur.

User must know:

- where to get help
- how to report issues
- how to stop automation
- how to recover

Expected support route:

- Discord

Success criteria:

User feels supported rather than abandoned.

---

## Stage 10 - Update Flow

User learns a new version exists.

Process:

1. Download new zip.
2. Extract new version.
3. Replace or archive previous version.
4. Launch updated build.

Success criteria:

Updates remain simple and understandable.

No auto-updater is required.

---

## Primary Trust Risks

### Trust Risk 1 - Automation Legitimacy Concerns

Users may not understand the difference between supervised keyboard automation
and cheating. Explain what the tool does and does not do clearly.

### Trust Risk 2 - Windows Defender / SmartScreen Warnings

Early beta builds from a small developer may trigger unknown-publisher or
low-reputation warnings. Explain this calmly. Do not tell users to blindly
ignore warnings.

### Trust Risk 3 - Fear Of Bans Or Cheating Accusations

Users may worry that automation equals cheating. Address this through
transparent explanation, not pressure or vague reassurance.

### Trust Risk 4 - Small-Developer Trust Concerns

Users may hesitate because the project is small and early. Provide clear
versioning, known issues, support routes, and safety explanations.

---

## Primary Support Risks

### Support Risk 1 - Incorrect FH6 Baseline State

Users may start from the wrong FH6 screen. This should be solved with clear
baseline guidance before adding complexity.

### Support Risk 2 - User Misunderstanding Auto1, Auto2, Or Auto3

Users may not know what each automation is meant to do. Explanations should
focus on purpose, baseline, expected result, and stop behavior.

### Support Risk 3 - Installation Confusion

Users may expect an installer. The portable zip model must be explained simply.

### Support Risk 4 - Update Confusion

Users may not understand manual zip replacement. Keep update instructions short
and repeatable.

These risks should be solved through onboarding and documentation before adding
complexity.

---

## Success Definition

The first-time user flow is successful when a founding tester can:

- discover the project
- understand the project
- trust the project
- download the software
- verify the download if desired
- install/extract successfully
- launch successfully
- understand Auto1, Auto2, and Auto3
- complete a first run
- recover from common issues
- update successfully

without requiring constant direct founder assistance.

---

## Final Principle

The purpose of the first-time user experience is not to impress users.

The purpose is to make users feel:

- informed
- safe
- supported
- capable of succeeding

Trust should be earned through clarity and transparency, not assumed.
