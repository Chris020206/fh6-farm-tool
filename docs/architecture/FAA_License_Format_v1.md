# FAA License Format v1

This document locks the byte-level format used by Milestone 1 license
verification. It is an interoperability contract, not a license issuance
workflow.

## Signed JSON File

A `.lic` file contains:

```json
{
  "payload": {},
  "signature": "STANDARD_BASE64_ED25519_SIGNATURE",
  "signing_key_id": "FAA_KEY_ID"
}
```

The Ed25519 signature covers only the canonical payload bytes described below.
The signing key ID selects a bundled public verification key.

## Canonical Payload Bytes

Before signing or verification, the payload object is serialized as:

- UTF-8
- JSON object keys sorted lexicographically at every object level
- no insignificant whitespace
- `,` between array/object entries
- `:` between object keys and values
- non-ASCII characters encoded directly as UTF-8, not `\u` escapes
- JSON `null`, `true`, and `false` in lowercase
- non-finite numbers (`NaN`, positive infinity, negative infinity) rejected
- no trailing newline

Equivalent Python reference operation:

```python
json.dumps(
    payload,
    allow_nan=False,
    ensure_ascii=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
```

The fixed conformance license is:

```text
tests/fixtures/licensing/valid_plus_license.lic
```

It must continue to verify against the bundled development Licensing Authority
public key. An accidental canonicalization change will invalidate this fixture.

## Pasteable Key

Current format:

```text
FAA-LIC-v1.<base64url(signing_key_id)>.<base64url(canonical_payload)>.<base64url(signature)>
```

Base64url segments omit `=` padding. The decoded signing key ID is UTF-8.

Legacy Milestone 1 three-segment keys remain accepted:

```text
FAA-LIC-v1.<base64url(canonical_payload)>.<base64url(signature)>
```

Legacy keys always select the default bundled key and therefore do not support
key rotation.

## Community Auto1 Limit

Community Edition may start Auto1 repeatedly. Each execution is limited to a
maximum of five consecutive race loops. No lifetime or local usage counter is
consumed. Licensed Basic, Plus, and Founding editions retain the validated
desktop maximum of 25 loops per execution.

The v1 claim identifier `FAA.Auto1.MaxRuns` is retained for signed-license
compatibility. Its enforced meaning is the Auto1 loop maximum for one
execution.
