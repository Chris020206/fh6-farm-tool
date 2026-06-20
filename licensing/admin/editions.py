"""Locked manually issuable FAA edition definitions."""

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from licensing.constants import (
    FEATURE_AUTO1_UNLIMITED,
    FEATURE_AUTO2_FULL,
    FEATURE_AUTO3_FULL,
    FEATURE_AUTO4_FULL,
    FEATURE_BATCH_LIMIT_EXTENDED,
    FEATURE_PROFILES_BASIC,
    FEATURE_PROFILES_PLUS,
)


@dataclass(frozen=True)
class IssuableEdition:
    edition: str
    features: tuple[str, ...]
    limits: Mapping[str, int | None] = field(default_factory=dict)
    metadata: Mapping[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "limits", MappingProxyType(dict(self.limits)))
        object.__setattr__(self, "metadata", MappingProxyType(dict(self.metadata)))


_CORE_FEATURES = (
    FEATURE_AUTO1_UNLIMITED,
    FEATURE_AUTO2_FULL,
    FEATURE_AUTO3_FULL,
)

ISSUABLE_EDITIONS = {
    "basic": IssuableEdition(
        edition="basic",
        features=(*_CORE_FEATURES, FEATURE_PROFILES_BASIC),
    ),
    "plus": IssuableEdition(
        edition="plus",
        features=(
            *_CORE_FEATURES,
            FEATURE_AUTO4_FULL,
            FEATURE_PROFILES_PLUS,
            FEATURE_BATCH_LIMIT_EXTENDED,
        ),
    ),
    "founding": IssuableEdition(
        edition="founding",
        features=(
            *_CORE_FEATURES,
            FEATURE_AUTO4_FULL,
            FEATURE_PROFILES_PLUS,
            FEATURE_BATCH_LIMIT_EXTENDED,
        ),
        metadata={"founding_supporter": True},
    ),
}


def get_issuable_edition(edition: str) -> IssuableEdition:
    try:
        return ISSUABLE_EDITIONS[edition]
    except KeyError as error:
        raise ValueError(
            "Edition must be one of: basic, plus, founding."
        ) from error
