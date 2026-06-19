# FAA Licensing Architecture --- Part 7

## Feature Gating & Edition Logic (Locked)

# 7.1 Core Principle

FAA never asks:

> Is this user paid?

FAA asks:

> Does the current verified license allow this feature?

Feature claims---not payment status---control execution.

------------------------------------------------------------------------

# 7.2 Edition vs Feature Claims

Two separate concepts exist:

-   **Edition** = customer-facing commercial package.
-   **Feature Claims** = permissions enforced by FAA.

The UI displays the edition.

FAA internally enforces feature claims.

------------------------------------------------------------------------

# 7.3 Editions

The locked edition structure is:

-   Community
-   Basic
-   Plus
-   Founding Edition
-   Developer/Admin

------------------------------------------------------------------------

# 7.4 Community Edition

Community Edition is the intentional default experience.

It is **not** a trial.

Allowed:

-   Auto1.Full (maximum 5 executions)
-   Auto2.NavigationTest
-   Auto3.NavigationTest

Locked:

-   Unlimited Auto1
-   Auto2.Full
-   Auto3.Full
-   Auto4.Full
-   Premium profiles
-   Advanced convenience features

Purpose:

-   Build trust
-   Demonstrate FAA
-   Verify compatibility
-   Allow users to experience the product before purchasing

------------------------------------------------------------------------

# 7.5 Basic Edition

Basic represents the complete core product.

Purpose:

-   Everything required to successfully use FAA.

Typical features:

-   Auto1.Full
-   Auto2.Full
-   Auto3.Full
-   Basic Profiles
-   Standard limits

------------------------------------------------------------------------

# 7.6 Plus Edition

Plus is designed for power users.

Plus should improve workflow rather than compensate for missing
functionality.

Examples:

-   Auto4.Full
-   Higher batch limits
-   Faster Auto2 implementation
-   Advanced profiles
-   Convenience features
-   Reduced friction

The philosophy is:

Sell convenience, not artificial restrictions.

------------------------------------------------------------------------

# 7.7 Founding Edition

Founding Edition replaces the previous Lifetime concept.

Purpose:

Recognize the earliest supporters who helped shape FAA during its
launch.

Characteristics:

-   Everything included in Plus
-   Permanent ownership
-   Exclusive Discord recognition
-   Priority beta access (optional)
-   Early supporter status

Founding Edition is only available during the initial launch period and
is never sold again.

------------------------------------------------------------------------

# 7.8 Developer/Admin Edition

Internal only.

Contains:

-   All features
-   Testing tools
-   Debug functionality
-   Internal diagnostics

Never sold publicly.

------------------------------------------------------------------------

# 7.9 Feature Gates

FAA should gate individual capabilities.

Examples:

-   Auto2.NavigationTest
-   Auto2.Full
-   Auto3.NavigationTest
-   Auto3.Full
-   Auto4.Full
-   Profiles.Basic
-   Profiles.Plus
-   BatchLimit.Standard
-   BatchLimit.Extended

Avoid using a single generic "PaidUser" flag.

------------------------------------------------------------------------

# 7.10 UI Behaviour

Locked features remain visible.

Example:

Auto3 Full Execution (Locked --- Available in Basic / Plus)

FAA should educate users rather than hide functionality.

------------------------------------------------------------------------

# 7.11 Execution Boundary

Permission checks occur when execution begins.

Flow:

Run requested → Verify feature claim → Allowed: continue → Denied: show
upgrade guidance

UI visibility must never be the only protection.

------------------------------------------------------------------------

# 7.12 Fail-Closed

If license verification fails:

FAA returns to Community Edition.

The application continues functioning safely.

------------------------------------------------------------------------

# 7.13 Upgrade Behaviour

When a replacement license is imported:

-   Signature verified
-   Old license replaced
-   Feature permissions recalculated
-   No restart required

------------------------------------------------------------------------

# 7.14 Locked Feature Messaging

Tone should always remain professional.

Example:

"This feature is available in FAA Plus.

Current edition: FAA Basic.

Upgrade through the FAA Discord."

Never use hostile wording.

------------------------------------------------------------------------

# 7.15 Locked Feature Gate Decision

FAA decisions are based only on:

-   Verified local license
-   Explicit feature claims

Never on:

-   Discord roles
-   Payment status
-   Usernames
-   Online connectivity

------------------------------------------------------------------------

# 7.16 Edition Philosophy

Each edition answers:

"Who is this edition for?"

## Community

People discovering FAA.

## Basic

People who simply want FAA to solve their problem.

## Plus

Power users who value efficiency and convenience.

## Founding Edition

The first supporters who helped establish FAA.

## Developer/Admin

Internal development and testing only.

------------------------------------------------------------------------

# Locked Principle

FAA editions define customer experiences---not pricing ladders.

Parts 1--7 now establish the complete external licensing and edition
architecture.
