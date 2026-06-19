# Forza Automation Assist — Licensing System Architecture
## Final Locked Architecture + Implementation Roadmap

## Purpose

This document defines the licensing system architecture for Forza Automation Assist (FAA).

The system is designed to support a commercial launch while preserving the product philosophy:

- Trust-first
- Simple
- Offline-first
- Reliable
- Explainable
- Professional
- Easy for honest customers
- Not designed to defeat determined reverse engineers

The goal is not to stop all piracy.

The goal is to create a clean, professional, sustainable commercial workflow.

---

# Part 1 — Licensing Goals & Non-Goals

## Goals

FAA licensing exists to:

1. Enable commercial distribution.
2. Keep the download publicly available through Nexus Mods.
3. Require users to obtain a license through Discord.
4. Unlock paid functionality.
5. Keep licensing simple for customers and the developer.
6. Allow FAA to remain offline after installation.
7. Support automatic license delivery through Discord.
8. Allow manual admin license issuance.
9. Support upgrades, replacements, and support workflows.

## Non-Goals

The licensing system is not intended to:

- Fully stop piracy.
- Defeat reverse engineers.
- Require always-online validation.
- Depend on Discord at runtime.
- Depend on Nexus Mods at runtime.
- Lock users out because Discord, PayBot, Stripe, or APIs are temporarily unavailable.
- Add complex account management before the product needs it.

## Locked Architecture Direction

FAA uses:

**Offline signed licenses + Discord-based issuance + manual admin issuance + local feature gating.**

---

# Part 2 — Threat Model

## Assets to Protect

The licensing system protects:

- Paid FAA features.
- License authenticity.
- Customer experience.
- Developer time and support workload.

## Threats We Care About

The system should protect against:

- Users editing licenses.
- Users inventing fake keys.
- Casual license sharing.
- Confusing activation flows.
- Payment/Discord bot outages disrupting new issuance.
- Public redistribution of the installer.

## Threats We Explicitly Ignore

The system does not try to defeat:

- Professional reverse engineering.
- Binary patching.
- Memory patching.
- Debugger bypasses.
- Kernel-level attacks.
- Determined piracy groups.

## Security Philosophy

The licensing system exists to:

- Make honest purchasing easy.
- Make casual piracy inconvenient.
- Ensure only FAA can issue valid licenses.
- Keep FAA usable offline.
- Avoid punishing legitimate customers.
- Stay understandable and maintainable.

---

# Part 3 — User Experience & Licensing Journey

## Discovery

FAA is discovered and downloaded publicly through Nexus Mods.

The download is not hidden behind payment.

## First Launch

FAA opens normally without login or internet requirement.

Unlicensed users enter:

**FAA Community Edition**

Community Edition should feel intentional, not broken.

## Community Edition

Community Edition allows:

- Auto1.Full with a maximum of 5 executions.
- Auto2.NavigationTest.
- Auto3.NavigationTest.
- Preview of locked paid features.

Locked features should be explained clearly and professionally.

## Upgrade Flow

The app directs users to Discord for purchase.

User journey:

```text
Nexus Mods download
↓
Install FAA
↓
Use Community Edition
↓
Join Discord
↓
Purchase membership
↓
Receive license by DM
↓
Import/paste license into FAA
↓
FAA verifies offline
↓
Paid features unlock
```

## Activation

FAA should support:

- Pasteable license key.
- License file import.

After activation, FAA displays:

- Current edition.
- License status.
- License ID.
- Enabled features.

No restart should be required.

## Everyday Use

After activation, licensing should disappear into the background.

FAA starts, verifies the local license offline, and unlocks features.

---

# Part 4 — License Data Model

## Principle

A license should describe permissions, not implementation details.

A license should answer:

**What is this customer allowed to do?**

## Required License Fields

A license should contain:

- License ID.
- Product.
- License format version.
- Discord user ID.
- Edition.
- Feature claims.
- Limits.
- Issued timestamp.
- Expiration field.
- Optional replacement reference.
- Optional metadata.
- Digital signature.

## Owner Identity

The license should store:

**Discord User ID**

not Discord username.

Usernames can change. Discord user IDs are stable.

## Feature Claims

Feature permissions should be explicit.

Example:

```text
FAA.Auto1.Full
FAA.Auto1.Unlimited
FAA.Auto2.NavigationTest
FAA.Auto2.Full
FAA.Auto3.NavigationTest
FAA.Auto3.Full
FAA.Auto4.Full
FAA.Profiles.Basic
FAA.Profiles.Plus
```

FAA should ask:

**Does this license contain this feature claim?**

not:

**Is this user Plus?**

## What Should Not Be in the License

Avoid storing:

- Discord role names.
- Payment information.
- API tokens.
- Secrets.
- Hardware fingerprints.
- Implementation-specific internals.

## License Design Principle

Licenses are declarative, not procedural.

They declare facts:

- This license belongs to this product.
- This license belongs to this Discord user ID.
- This license grants these feature claims.
- This license was signed by FAA.

---

# Part 5 — Signing & Verification Architecture

## Root of Trust

There is one root of trust:

**Licensing Authority**

Not Discord.  
Not PayBot.  
Not Nexus Mods.  
Not the desktop app.

## Private Key Rule

The private signing key must never be included in:

- FAA desktop app.
- GitHub repository.
- Nexus Mods upload.
- Installer.
- Public configuration files.
- User-facing tools.

Only the Licensing Authority can sign valid licenses.

## Public Verification Key

FAA ships with the public verification key.

The public key can verify licenses but cannot create them.

## Issuance Flow

```text
Customer qualifies
↓
License payload is built
↓
Payload is signed
↓
Signed license is stored
↓
Signed license is delivered to customer
```

## Verification Flow

```text
FAA reads license
↓
FAA extracts payload and signature
↓
FAA verifies signature using public key
↓
If valid, FAA unlocks permitted features
↓
If invalid, FAA remains in Community Edition
```

## Fail-Closed Behavior

If anything fails, FAA should remain in Community Edition.

Examples:

- Corrupt license.
- Missing signature.
- Invalid signature.
- Unsupported version.
- Expired license.
- Malformed file.

FAA should not crash or accuse the user.

## Offline Runtime

Once installed, FAA must not require:

- Discord.
- PayBot.
- Stripe.
- Nexus Mods.
- Licensing server.
- Online validation.

for normal operation.

## Key Rotation

Future-ready key rotation should be supported through signing key/version metadata.

---

# Part 6 — Discord Integration & Licensing Workflow

## Responsibility Split

### PayBot

PayBot handles:

- Payment checkout.
- Stripe/payment logic.
- Discord paid role assignment.
- Role removal if subscriptions or access expiry require it.

PayBot does not handle:

- FAA license generation.
- FAA license signing.
- FAA license storage.
- FAA feature permissions.
- FAA app unlocking.

### Discord License Service

The Discord License Service handles:

- Watching FAA paid roles.
- Detecting role changes.
- Mapping roles to internal FAA editions.
- Checking license records.
- Requesting license creation.
- DMing licenses.
- Resending licenses.
- Admin commands.
- Support fallback.

### Licensing Authority

The Licensing Authority handles:

- License ID generation.
- License payload creation.
- Edition-to-feature mapping.
- Digital signing.
- License record storage.
- Manual admin issuance.
- Private signing key protection.

### FAA Desktop App

FAA handles:

- Importing license.
- Verifying signature offline.
- Storing current local license.
- Unlocking features.
- Replacing local license when a valid upgrade is imported.
- Falling back to Community Edition when invalid.

## Two-Bot Discord Architecture

Correct Discord architecture:

```text
PayBot
↓
Discord paid role
↓
Discord License Service
↓
Licensing Authority
↓
Signed license
↓
Customer DM
↓
FAA offline verification
```

## Key Rule

PayBot is not part of the license trust model.

PayBot only creates the condition:

**This user has a paid Discord role.**

The Discord License Service and Licensing Authority decide:

**Issue signed FAA license.**

## Membership Tier Upgrades & License Replacement

Each Discord user should have:

**one current active FAA license**

not one active license per tier.

Upgrade flow:

```text
User upgrades membership tier
↓
PayBot updates Discord role
↓
Discord License Service detects upgraded role
↓
Bot compares current active license
↓
Licensing Authority issues replacement license
↓
Old license is marked superseded
↓
New license is DM'd to user
↓
User imports new license into FAA
↓
FAA unlocks upgraded features
```

## Replacement, Not Mutation

Old licenses should not be edited because signed content cannot be changed without invalidating the signature.

Instead:

- New license is issued.
- Old license is marked superseded.
- New license references old license if useful.

## FAA Desktop License Replacement

FAA must support local license replacement.

When importing a new license, FAA checks:

- Valid signature.
- Same product.
- Same owner Discord user ID, when applicable.
- Newer issued timestamp.
- Valid edition/feature claims.
- Not expired.
- Replacement metadata, if present.

FAA stores one current local license.

## License Lifecycle

A license is not just a key.

It is a managed customer state.

License states:

- No License.
- Issued.
- Activated.
- Replaced.
- Reissued.
- Superseded.
- Revoked, future/offline-limited.

Replacement vs reissue:

Replacement:

- New license.
- New ID.
- New signature.
- New permissions.

Reissue:

- Same license.
- Same ID.
- Same signature.
- Same permissions.
- Only delivered again.

---

# Part 7 — Feature Gating & Edition Logic

## Core Principle

FAA never asks:

**Is this user paid?**

FAA asks:

**Does the current verified license allow this feature?**

Feature claims, not payment status, control execution.

## Edition vs Feature Claims

Two separate concepts exist:

- Edition = customer-facing commercial package.
- Feature Claims = permissions enforced by FAA.

The UI displays the edition.

FAA internally enforces feature claims.

## Editions

The locked edition structure is:

- Community.
- Basic.
- Plus.
- Founding Edition.
- Developer/Admin.

## Community Edition

Community Edition is the intentional default experience.

It is not a trial.

Allowed:

- Auto1.Full, maximum 5 executions.
- Auto2.NavigationTest.
- Auto3.NavigationTest.

Locked:

- Unlimited Auto1.
- Auto2.Full.
- Auto3.Full.
- Auto4.Full.
- Premium profiles.
- Advanced convenience features.

Purpose:

- Build trust.
- Demonstrate FAA.
- Verify compatibility.
- Allow users to experience the product before purchasing.

## Basic Edition

Basic represents the complete core product.

Purpose:

**Everything required to successfully use FAA.**

Typical features:

- Auto1.Unlimited.
- Auto2.Full.
- Auto3.Full.
- Basic Profiles.
- Standard limits.

## Plus Edition

Plus is designed for power users.

Plus should improve workflow rather than compensate for missing functionality.

Examples:

- Auto4.Full.
- Higher batch limits.
- Faster Auto2 implementation.
- Advanced profiles.
- Convenience features.
- Reduced friction.

The philosophy is:

**Sell convenience, not artificial restrictions.**

## Founding Edition

Founding Edition replaces the previous Lifetime concept.

Purpose:

Recognize the earliest supporters who helped shape FAA during its launch.

Characteristics:

- Everything included in Plus.
- Permanent ownership.
- Exclusive Discord recognition.
- Priority beta access, optional.
- Early supporter status.

Founding Edition is only available during the initial launch period and is never sold again.

## Developer/Admin Edition

Internal only.

Contains:

- All features.
- Testing tools.
- Debug functionality.
- Internal diagnostics.

Never sold publicly.

## Feature Gates

FAA should gate individual capabilities.

Examples:

- FAA.Auto1.Full.
- FAA.Auto1.Unlimited.
- FAA.Auto2.NavigationTest.
- FAA.Auto2.Full.
- FAA.Auto3.NavigationTest.
- FAA.Auto3.Full.
- FAA.Auto4.Full.
- FAA.Profiles.Basic.
- FAA.Profiles.Plus.
- FAA.BatchLimit.Standard.
- FAA.BatchLimit.Extended.

Avoid using a single generic PaidUser flag.

## UI Behaviour

Locked features remain visible.

Example:

```text
Auto3 Full Execution
Locked — Available in Basic / Plus
```

FAA should educate users rather than hide functionality.

## Execution Boundary

Permission checks occur when execution begins.

Flow:

```text
Run requested
↓
Verify feature claim
↓
Allowed: continue
↓
Denied: show upgrade guidance
```

UI visibility must never be the only protection.

## Fail-Closed

If license verification fails:

FAA returns to Community Edition.

The application continues functioning safely.

## Upgrade Behaviour

When a replacement license is imported:

- Signature verified.
- Old license replaced.
- Feature permissions recalculated.
- No restart required.

## Locked Feature Messaging

Tone should always remain professional.

Example:

```text
This feature is available in FAA Plus.

Current edition: FAA Basic.

Upgrade through the FAA Discord.
```

Never use hostile wording.

## Locked Feature Gate Decision

FAA decisions are based only on:

- Verified local license.
- Explicit feature claims.

Never on:

- Discord roles.
- Payment status.
- Usernames.
- Online connectivity.

## Edition Philosophy

Each edition answers:

**Who is this edition for?**

Community:
People discovering FAA.

Basic:
People who simply want FAA to solve their problem.

Plus:
Power users who value efficiency and convenience.

Founding Edition:
The first supporters who helped establish FAA.

Developer/Admin:
Internal development and testing only.

## Locked Principle

FAA editions define customer experiences, not pricing ladders.

---

# Part 8 — Technical Implementation Architecture

This is the last architectural section.

The goal is to convert the licensing design into concrete build decisions.

## Recommended Technical Shape

FAA should use:

```text
Signed JSON license
+
local license storage
+
offline public-key verification
```

Not binary.  
Not encrypted.  
Not online activation.

## License Storage Location

On Windows, store the active imported license here:

```text
%APPDATA%\ForzaAutomationAssist\license.lic
```

Example:

```text
C:\Users\<User>\AppData\Roaming\ForzaAutomationAssist\license.lic
```

FAA should allow importing from anywhere, but once imported, it copies the validated license into this location.

## License Format

Use a signed JSON object.

Physical file:

```text
license.lic
```

Example:

```json
{
  "payload": {
    "license_id": "FAA-2026-000001",
    "product": "forza_automation_assist",
    "license_version": 1,
    "discord_user_id": "123456789012345678",
    "edition": "plus",
    "features": [
      "FAA.Auto1.Unlimited",
      "FAA.Auto2.Full",
      "FAA.Auto3.Full",
      "FAA.Profiles.Plus"
    ],
    "limits": {
      "FAA.Auto1.MaxRuns": null,
      "FAA.Auto2.MaxBatch": 50,
      "FAA.Auto3.MaxBatch": 50
    },
    "issued_at": "2026-06-19T18:00:00Z",
    "expires_at": null,
    "replaces_license_id": null
  },
  "signature": "BASE64_SIGNATURE",
  "signing_key_id": "FAA_KEY_2026_01"
}
```

Important:

- The payload is readable.
- The signature protects it from editing.
- The file contains no secrets.

## License Key Format

For Discord DM delivery, the same license can be encoded as a pasteable key.

Example:

```text
FAA-LIC-v1.<base64url(payload)>.<base64url(signature)>
```

FAA should support both:

- Import license file.
- Paste license key.

Internally both decode into the same license object.

## Signing Algorithm

Use:

```text
Ed25519
```

Preferred Python library:

```text
cryptography
```

## Signing Key Handling

Private signing key location:

```text
Never inside FAA desktop app.
```

For launch, the private key can live only on the developer/admin machine, protected outside the repo.

Example local path:

```text
C:\Secure\FAA_Licensing\private_key.pem
```

Public key location:

```text
FAA desktop source code or bundled config
```

Rules:

- never commit private key.
- never package private key.
- back up private key securely.
- keep at least one offline backup.

## License Verification in FAA

FAA startup flow:

```text
Start FAA
↓
Look for local license.lic
↓
If missing → Community Edition
↓
If found → parse license
↓
Verify signature
↓
Check product
↓
Check version
↓
Check expiration
↓
Load feature claims and limits
↓
Set current edition
```

If any step fails:

```text
Community Edition
```

## Community Edition Limits

Community Edition should be represented internally like a license profile, even though no license exists.

```json
{
  "edition": "community",
  "features": [
    "FAA.Auto1.Full",
    "FAA.Auto2.NavigationTest",
    "FAA.Auto3.NavigationTest"
  ],
  "limits": {
    "FAA.Auto1.MaxRuns": 5
  }
}
```

Everything asks:

```text
Does current entitlement allow this?
```

## Execution Boundary Check

Before any automation runs, FAA checks entitlement.

Example:

```text
User starts Auto1
↓
Check FAA.Auto1.Full
↓
Check FAA.Auto1.MaxRuns
↓
Allowed or denied
```

For Auto2:

```text
User starts Auto2 purchase execution
↓
Check FAA.Auto2.Full
↓
Allowed or upgrade message
```

For Auto3:

```text
User starts Auto3 unlock execution
↓
Check FAA.Auto3.Full
↓
Allowed or upgrade message
```

This must happen at execution time, not only in the UI.

## License Replacement

When importing a new license:

```text
Parse
↓
Verify signature
↓
Check product
↓
Compare with current license
↓
If valid upgrade/replacement → store new license.lic
↓
Recalculate entitlements
↓
Update UI immediately
```

Do not mutate old licenses.

Replace local stored license with the new valid license.

## License Administration Console

For launch, the admin console can be simple and CLI-first.

It needs:

- Create license.
- Lookup customer.
- Resend license.
- Replace license.
- View license history.

Example:

```text
license-admin issue --discord-id 123456789 --edition plus
license-admin lookup --discord-id 123456789
license-admin resend --discord-id 123456789
license-admin replace --discord-id 123456789 --edition founding
```

A GUI can come later.

Do not build a full admin dashboard before launch.

## License Records Storage

For launch, use SQLite.

Example:

```text
licensing.db
```

Minimum tables:

```text
customers
licenses
license_events
```

Minimum fields:

```text
customers:
- discord_user_id
- first_seen_at
- current_license_id

licenses:
- license_id
- discord_user_id
- edition
- payload_json
- signature
- status
- issued_at
- replaces_license_id

license_events:
- event_id
- license_id
- discord_user_id
- event_type
- timestamp
- notes
```

SQLite is enough.

No server database needed for launch.

## Discord License Service

The Discord bot should do only this:

```text
Observe role changes
↓
Map role to edition
↓
Check SQLite license records
↓
Issue/resend/replace license
↓
DM user
↓
Log event
```

It should not:

- handle payments.
- know Stripe.
- verify app licenses.
- contain UI logic.
- contain the private key directly if avoidable.

For launch, bot and admin console can call the same local license service module.

## PayBot Integration

PayBot integration point:

```text
Discord paid role
```

Not Stripe API.  
Not payment webhook.  
Not PayBot database.

The Discord License Service only cares:

```text
Does this member have a paid FAA role?
```

Role mapping example:

```text
FAA Basic Role → basic
FAA Plus Role → plus
FAA Founding Role → founding
```

## Failure Handling

No license:
Community Edition.

Invalid license:
Community Edition plus helpful message.

Expired license:
Community Edition plus clear explanation.

Import valid upgrade:
Replace current license.

DM failed:
License still stored; admin/support can resend.

Bot offline during payment:
On restart, bot scans members with FAA roles and issues missing licenses.

Database unavailable:
Bot stops issuing licenses. FAA desktop remains unaffected.

## What We Should Not Build for Launch

Do not build:

- online activation server.
- hardware binding.
- web dashboard.
- complex account system.
- automatic revocation enforcement.
- multi-product platform abstraction.
- enterprise licensing.
- anti-tamper DRM.
- cloud database.

## Locked Technical Direction

For FAA launch:

```text
Signed JSON license
Ed25519 signature
cryptography library
local license.lic in AppData
SQLite license records
CLI-first admin console
Discord bot watches paid roles
PayBot handles payment and role assignment
FAA verifies offline
```

---

# Part 9 — Implementation Roadmap

This is the execution plan.

After this, architecture stops and implementation begins.

## Milestone 1 — Desktop License Foundation

Goal:

FAA can understand licenses locally.

Build:

- License data model.
- Signed JSON parsing.
- Ed25519 signature verification.
- Public key bundled with FAA.
- Community Edition entitlement profile.
- 5-run Auto1 Community limit.
- Local license storage in AppData.
- Import license file.
- Paste license key.
- Feature gate checks at execution boundary.

Done when:

```text
FAA starts without a license → Community Edition
FAA imports valid license → paid features unlock
FAA imports invalid license → Community Edition
Auto1 Community limit blocks after 5 runs
Auto2/Auto3 full execution require license claims
```

## Milestone 2 — Manual License Issuance

Goal:

Admin can issue licenses without Discord automation.

Build:

- CLI admin tool.
- Private key loading outside repo.
- License signing.
- SQLite database.
- Customer records.
- License records.
- License event logs.
- Manual issue command.
- Manual lookup command.
- Manual resend/export command.
- Manual replace/upgrade command.

Done when:

```text
Admin can create Basic license
Admin can create Plus license
Admin can create Founding license
Admin can replace Basic → Plus
Admin can resend existing license
FAA accepts licenses created by admin tool
```

## Milestone 3 — Discord License Service

Goal:

Discord roles automatically create and deliver licenses.

Build:

- Bot reads configured paid roles.
- Role → edition mapping.
- Detect member role update.
- Check if customer already has active license.
- Issue new license if none exists.
- Replace license if tier upgraded.
- Resend existing license if already active.
- DM license key/file.
- Log DM success/failure.
- Startup scan for members with paid roles.

Done when:

```text
User receives Basic role → Basic license DM
User upgrades Basic → Plus → replacement Plus license DM
User already has license → bot resends instead of duplicating
Bot restart → missing licenses are issued
DM failure → license remains stored for manual resend
```

## Milestone 4 — PayBot Integration

Goal:

PayBot becomes the payment trigger.

Build/configure:

- PayBot checkout.
- Discord paid roles.
- Basic role.
- Plus role.
- Founding role.
- Role mapping in Discord License Service.
- End-to-end test payment flow.

Done when:

```text
User pays through PayBot
PayBot assigns Discord role
Discord License Service detects role
License is generated
License is DM'd
User imports license into FAA
Correct features unlock offline
```

## Milestone 5 — Polish, Testing, Beta

Goal:

Make the system launch-safe.

Build/test:

- Friendly activation UI messages.
- Invalid license handling.
- Expired license handling.
- Replacement license handling.
- Community limit UX.
- License support runbook.
- Admin backup procedure.
- Private key backup procedure.
- Beta tester issuance workflow.
- Founding Edition workflow.
- End-to-end test checklist.

Done when:

```text
A new user can download FAA from Nexus
Join Discord
Pay through PayBot
Receive license automatically
Import license
Use paid features offline
And support can recover/resend licenses manually
```

## Final Locked Execution Order

```text
1. Desktop License Foundation
2. Manual License Issuance
3. Discord License Service
4. PayBot Integration
5. Polish, Testing, Beta
```

Do not start with PayBot.  
Do not start with Discord automation.  
Do not start with a GUI admin dashboard.

Start with the desktop license foundation because FAA itself must understand licensing first.

---

# Final Build Rule

From this point forward:

- Stop expanding architecture.
- Stop renaming internal concepts unless implementation requires it.
- Stop planning hypothetical future products.
- Start building according to the milestone order.

Any architecture change must be justified by an implementation problem, not theoretical improvement.
