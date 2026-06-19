"""Immutable license and entitlement data models."""

from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class LicensePayload:
    license_id: str
    product: str
    license_version: int
    discord_user_id: str
    edition: str
    features: frozenset[str]
    limits: Mapping[str, int | None]
    issued_at: datetime
    expires_at: datetime | None
    replaces_license_id: str | None = None
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "limits", MappingProxyType(dict(self.limits)))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


@dataclass(frozen=True)
class SignedLicense:
    payload: LicensePayload
    signature: bytes
    signing_key_id: str
    signed_payload: bytes
    serialized_json: str


@dataclass(frozen=True)
class EntitlementProfile:
    edition: str
    features: frozenset[str]
    limits: Mapping[str, int | None]
    license_id: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "limits", MappingProxyType(dict(self.limits)))

    def allows(self, feature: str) -> bool:
        return feature in self.features


@dataclass(frozen=True)
class LicenseState:
    status: str
    entitlements: EntitlementProfile
    message: str
    license: SignedLicense | None = None

    @property
    def is_licensed(self) -> bool:
        return self.status == "licensed" and self.license is not None


@dataclass(frozen=True)
class LicenseImportResult:
    accepted: bool
    state: LicenseState
    message: str


@dataclass(frozen=True)
class EntitlementDecision:
    allowed: bool
    message: str
    edition: str
    required_feature: str
    current_usage: int | None = None
    usage_limit: int | None = None
