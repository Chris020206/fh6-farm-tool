# Licensing System Architecture — Forza Automation Assist
## Locked Core Architecture: Parts 1–6

## Product Philosophy

The FAA licensing system is designed to be:

- Trust-first
- Simple
- Offline-first
- Reliable
- Explainable
- Professional
- Easy for honest customers
- Not designed to defeat nation-state attackers or determined reverse engineers

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
9. Support future upgrades, replacements, and support workflows.

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

Community Edition may allow:

- Auto1
- Auto2 navigation test
- Auto3 navigation test
- Preview of locked paid features

Locked features should be explained clearly and professionally.

## Upgrade Flow

The app directs users to Discord for purchase.

The user journey is:

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

- Pasteable license key
- License file import

After activation, FAA displays:

- Current edition
- License status
- License ID
- Enabled features

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

- License ID
- Product
- License format version
- Discord user ID
- Edition
- Feature claims
- Issued timestamp
- Expiration field
- Optional replacement reference
- Optional metadata
- Digital signature

## Owner Identity

The license should store:

**Discord User ID**

not Discord username.

Usernames can change.  
Discord user IDs are stable.

## Feature Claims

Feature permissions should be explicit.

Example:

```text
Auto1
Auto2.NavigationTest
Auto2.Full
Auto3.NavigationTest
Auto3.Full
Auto4.Full
Profiles.Basic
Profiles.Plus
```

FAA should ask:

**Does this license contain this feature claim?**

not:

**Is this user Plus?**

## What Should Not Be in the License

Avoid storing:

- Discord role names
- Payment information
- API tokens
- Secrets
- Hardware fingerprints
- Implementation-specific internals

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

**FAA Licensing Authority**

Not Discord.  
Not PayBot.  
Not Nexus Mods.  
Not the desktop app.

## Private Key Rule

The private signing key must never be included in:

- FAA desktop app
- GitHub repository
- Nexus Mods upload
- Installer
- Public configuration files
- User-facing tools

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

- Corrupt license
- Missing signature
- Invalid signature
- Unsupported version
- Expired license
- Malformed file

FAA should not crash or accuse the user.

## Offline Runtime

Once installed, FAA must not require:

- Discord
- PayBot
- Stripe
- Nexus Mods
- Licensing server
- Online validation

for normal operation.

## Key Rotation

Future-ready key rotation should be supported through signing key/version metadata.

---

# Part 6 — Discord Integration & Licensing Authority Workflow

## Responsibility Split

### PayBot

PayBot handles:

- Payment checkout
- Stripe/payment logic
- Discord paid role assignment
- Role removal if subscriptions or access expiry require it

PayBot does not handle:

- FAA license generation
- FAA license signing
- FAA license storage
- FAA feature permissions
- FAA app unlocking

### FAA License Bot

The FAA License Bot handles:

- Watching FAA paid roles
- Detecting role changes
- Mapping roles to internal FAA editions
- Checking license records
- Requesting license creation
- DMing licenses
- Resending licenses
- Admin commands
- Support fallback

### FAA Licensing Authority

The Licensing Authority handles:

- License ID generation
- License payload creation
- Edition-to-feature mapping
- Digital signing
- License record storage
- Manual admin issuance
- Private signing key protection

### FAA Desktop App

FAA handles:

- Importing license
- Verifying signature offline
- Storing current local license
- Unlocking features
- Replacing local license when a valid upgrade is imported
- Falling back to Community Edition when invalid

---

# Part 6.11 — Two-Bot Discord Architecture

The correct Discord architecture is:

```text
PayBot
↓
Discord paid role
↓
FAA License Bot
↓
FAA Licensing Authority
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

FAA License Bot and Licensing Authority decide:

**Issue signed FAA license.**

---

# Part 6.12 — Membership Tier Upgrades & License Replacement

## Correct Rule

Each Discord user should have:

**one current active FAA license**

not one active license per tier.

## Upgrade Flow

```text
User upgrades membership tier
↓
PayBot updates Discord role
↓
FAA License Bot detects upgraded role
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

Example:

```text
Old:
FAA-2026-000042
Edition: Basic
Status: Superseded
Replaced By: FAA-2026-000089

New:
FAA-2026-000089
Edition: Plus
Status: Active
Replaces: FAA-2026-000042
```

---

# Part 6.13 — FAA Desktop License Replacement

FAA must support local license replacement.

When importing a new license, FAA checks:

- Valid signature
- Same product
- Same owner Discord user ID, when applicable
- Newer issued timestamp
- Valid edition/feature claims
- Not expired
- Replacement metadata, if present

## Allowed Replacement Direction

Expected upgrades:

```text
Community → Basic
Basic → Plus
Plus → Lifetime
Beta → Plus/Lifetime
```

Suspicious downgrades:

```text
Plus → Basic
Lifetime → Plus
```

should either be rejected or require confirmation.

## Desktop Rule

FAA stores one current local license.

```text
Import new license
↓
Verify signature
↓
Compare against current license
↓
Replace local license if valid upgrade/replacement
↓
Unlock updated features immediately
```

---

# Part 6.14 — License Lifecycle Architecture

A license is not just a key.

It is a managed customer state.

## License States

### No License

FAA runs as Community Edition.

### Issued

The Licensing Authority created and signed the license.

The user may not have imported it yet.

### Activated

The user imported the license into FAA.

FAA verified it and unlocked features.

### Replaced

A new upgraded license replaced the old one.

### Reissued

The same license is resent to the user.

This is not a new license.

### Superseded

A historical license that was replaced by a newer license.

### Revoked

Future state. Useful for admin records, but limited in offline enforcement.

## Replacement vs Reissue

### Replacement

New license.  
New ID.  
New signature.  
New permissions.

### Reissue

Same license.  
Same ID.  
Same signature.  
Same permissions.  
Only delivered again.

---

# Locked Foundation

Parts 1–6 are locked as the FAA Licensing Core Architecture.

The foundation is:

```text
Public Nexus download
↓
FAA Community Edition
↓
Discord purchase through PayBot
↓
Paid Discord role
↓
FAA License Bot detects role
↓
FAA Licensing Authority signs license
↓
License sent by DM
↓
FAA verifies offline
↓
Features unlock locally
```

This foundation is now stable enough to build edition logic, feature gating, pricing, trials, and implementation plans on top of it.
