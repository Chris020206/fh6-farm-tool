# FAA Manual License Administration v1

This document records the Milestone 2 local administration interface. The tool
is internal, CLI-first, and independent from the FAA desktop runtime.

## Entry Point

```powershell
python -B -m licensing.admin --help
```

## Local Defaults

```text
Database:
%USERPROFILE%\.faa-licensing\development\licensing.db

Private key:
%USERPROFILE%\.faa-licensing\development\FAA_KEY_DEV_2026_01_private.pem

Issued files:
%USERPROFILE%\.faa-licensing\development\issued\
```

Overrides:

- `--database` or `FAA_LICENSE_DB_PATH`
- `--private-key` or `FAA_LICENSE_PRIVATE_KEY_PATH`
- `--signing-key-id` or `FAA_LICENSE_SIGNING_KEY_ID`

The private key must remain outside the repository and desktop package. The
signer refuses a key that does not match the selected public key bundled with
the desktop verifier.

## Commands

Issue a first license:

```powershell
python -B -m licensing.admin issue --discord-id 123456789 --edition basic
python -B -m licensing.admin issue --discord-id 123456789 --edition plus
python -B -m licensing.admin issue --discord-id 123456789 --edition founding
```

Lookup current state and history:

```powershell
python -B -m licensing.admin lookup --discord-id 123456789
```

Export or resend the unchanged active license:

```powershell
python -B -m licensing.admin export --discord-id 123456789 --out C:\path\license.lic
```

Replace an active license with a higher edition:

```powershell
python -B -m licensing.admin replace --discord-id 123456789 --edition plus
```

Replacement creates and signs a new payload, marks the previous license
superseded, updates the customer's active license, and records both events.
The previous signed payload is never mutated.

## Boundaries

- Basic, Plus, and Founding are the only manually issuable editions.
- Founding licenses have `expires_at: null`.
- Developer/Admin is not exposed by this tool.
- No Discord, payment, role, online activation, or desktop dependency exists.
