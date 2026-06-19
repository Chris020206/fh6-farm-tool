# Forza Automation Assist - Beta Release Checklist v1

## Purpose

This checklist must be completed before any founding tester beta build is
distributed.

The purpose is to:

- reduce avoidable release mistakes
- improve release consistency
- improve trust
- improve support readiness
- verify packaging quality
- verify onboarding readiness

This checklist is a release gate.

A release is not considered ready until all required items are completed or
consciously waived.

---

## Section 1 - Release Identity

Verify:

- [ ] Version number assigned
- [ ] Version follows Packaging Strategy versioning scheme
- [ ] `VERSION.txt` updated
- [ ] Release date updated
- [ ] Changelog reviewed
- [ ] Build type identified correctly
- [ ] Known compatibility notes reviewed

Release candidate:

Version: __________

Build Type: __________

Date: __________

---

## Section 2 - Packaging Verification

Verify:

- [ ] Package created successfully
- [ ] Zip opens correctly
- [ ] Folder structure matches Packaging Strategy
- [ ] Executable present
- [ ] Required package files present
- [ ] Assets included correctly
- [ ] Branding assets included correctly
- [ ] No accidental developer files included

Examples of files that should not be included:

- source-control artifacts
- temporary files
- experimental exports
- unrelated working files

---

## Section 3 - Documentation Verification

Verify:

- [ ] `README_INSTALL.txt` reviewed
- [ ] `SAFETY_AND_TRANSPARENCY.txt` reviewed
- [ ] `VERSION.txt` reviewed
- [ ] `KNOWN_ISSUES.txt` reviewed
- [ ] Discord instructions remain accurate
- [ ] Support routes remain accurate
- [ ] Download instructions remain accurate

---

## Section 4 - Automation Validation

Verify:

### Auto1

- [ ] Launches correctly
- [ ] Expected behavior verified
- [ ] F8 stop verified
- [ ] Completion behavior verified

### Auto2

- [ ] Launches correctly
- [ ] Expected behavior verified
- [ ] Spending safeguards verified
- [ ] Completion behavior verified

### Auto3

- [ ] Launches correctly
- [ ] Validated traversal verified
- [ ] F8 stop verified
- [ ] Completion behavior verified

### General

- [ ] No known regression introduced
- [ ] Existing validated behavior preserved

---

## Section 5 - User Experience Verification

Verify:

- [ ] New user can understand installation process
- [ ] New user can locate support
- [ ] New user can understand Auto1
- [ ] New user can understand Auto2
- [ ] New user can understand Auto3
- [ ] New user can identify F8 stop behavior
- [ ] New user can identify known issues

Goal:

The user should not need direct founder assistance for basic operation.

---

## Section 6 - Trust Verification

Verify:

- [ ] Transparency information included
- [ ] Safety explanations remain accurate
- [ ] Defender guidance remains accurate
- [ ] No misleading claims present
- [ ] No absolute safety claims present
- [ ] No pressure-based trust language present

Principle:

Trust should be earned through clarity and transparency.

---

## Section 7 - Release Distribution Verification

Verify:

- [ ] Zip uploaded successfully
- [ ] Download link tested
- [ ] Discord announcement prepared
- [ ] Discord announcement reviewed
- [ ] Previous build archived
- [ ] Release notes prepared if applicable

---

## Section 8 - Final Release Gate

Before distribution, answer:

- [ ] Would I be comfortable giving this build to a complete stranger?
- [ ] Can a new user install this successfully?
- [ ] Can a new user understand what the software does?
- [ ] Can a new user understand how to stop automation?
- [ ] Can a new user recover from common problems?
- [ ] Does this build represent the project professionally?

If any answer is "No", the release should not be distributed until the issue
is understood and addressed.

---

## Waivers

If a checklist item is intentionally skipped:

Item:

---

Reason:

---

Approved By:

---

Date:

---

---

## Final Principle

The purpose of a beta release is not to ship quickly.

The purpose is to distribute a build that users can reasonably understand,
trust, install, operate, and receive support for.

Trust is easier to preserve than to rebuild.
