"""Offline license loading, import, replacement, and entitlement decisions."""

from pathlib import Path

from licensing.constants import (
    EDITION_RANKS,
    FEATURE_AUTO1_FULL,
    FEATURE_AUTO1_UNLIMITED,
    FEATURE_AUTO2_FULL,
    FEATURE_AUTO2_NAVIGATION_TEST,
    FEATURE_AUTO3_FULL,
    FEATURE_AUTO3_NAVIGATION_TEST,
    LIMIT_AUTO1_MAX_RUNS,
)
from licensing.entitlements import community_entitlements, entitlements_from_license
from licensing.models import (
    EntitlementDecision,
    LicenseImportResult,
    LicenseState,
    SignedLicense,
)
from licensing.parsing import LicenseParseError, parse_license_key, parse_signed_license_json
from licensing.storage import CommunityUsageStore, LicenseStorage, LicenseStorageError
from licensing.verification import LicenseVerificationError, LicenseVerifier


class LicenseService:
    def __init__(
        self,
        storage: LicenseStorage | None = None,
        usage_store: CommunityUsageStore | None = None,
        verifier: LicenseVerifier | None = None,
    ) -> None:
        self.storage = storage or LicenseStorage()
        self.usage_store = usage_store or CommunityUsageStore(self.storage.directory)
        self.verifier = verifier or LicenseVerifier()

    def current_state(self) -> LicenseState:
        try:
            stored_text = self.storage.read()
        except LicenseStorageError as error:
            return self._community_state("invalid", str(error))
        if stored_text is None:
            return self._community_state(
                "community",
                "No local license is installed. Community Edition is active.",
            )
        try:
            signed_license = parse_signed_license_json(stored_text)
            self.verifier.verify(signed_license)
        except (LicenseParseError, LicenseVerificationError) as error:
            return self._community_state("invalid", str(error))
        return LicenseState(
            status="licensed",
            entitlements=entitlements_from_license(signed_license),
            message=f"{signed_license.payload.edition.title()} Edition license is active.",
            license=signed_license,
        )

    def import_file(self, source_path: str | Path) -> LicenseImportResult:
        try:
            raw_text = Path(source_path).read_text(encoding="utf-8")
        except OSError as error:
            return self._rejected_import("Selected license file could not be read.")
        return self.import_json(raw_text)

    def import_json(self, raw_text: str) -> LicenseImportResult:
        try:
            candidate = parse_signed_license_json(raw_text)
        except LicenseParseError as error:
            return self._rejected_import(str(error))
        return self._import_verified_candidate(candidate)

    def import_key(self, raw_key: str) -> LicenseImportResult:
        try:
            candidate = parse_license_key(raw_key)
        except LicenseParseError as error:
            return self._rejected_import(str(error))
        return self._import_verified_candidate(candidate)

    def remove_license(self) -> LicenseImportResult:
        current = self.current_state()
        try:
            removed = self.storage.remove()
        except LicenseStorageError as error:
            return LicenseImportResult(False, current, str(error))
        if not removed:
            return LicenseImportResult(False, current, "No local license is installed.")
        state = self._community_state(
            "community",
            "Local license removed. Community Edition is active.",
        )
        return LicenseImportResult(True, state, "License removed successfully.")

    def evaluate_execution(
        self,
        automation_id: str,
        mode: str | None = None,
    ) -> EntitlementDecision:
        """Evaluate an execution request without mutating usage state."""
        state = self.current_state()
        entitlements = state.entitlements

        if automation_id == "auto1":
            if entitlements.allows(FEATURE_AUTO1_UNLIMITED):
                return self._allowed(state, FEATURE_AUTO1_UNLIMITED)
            if not entitlements.allows(FEATURE_AUTO1_FULL):
                return self._denied(state, FEATURE_AUTO1_FULL)
            maximum = entitlements.limits.get(LIMIT_AUTO1_MAX_RUNS)
            if not isinstance(maximum, int):
                return self._denied(
                    state,
                    LIMIT_AUTO1_MAX_RUNS,
                    "Auto1 execution limit is unavailable.",
                )
            try:
                usage = self.usage_store.execution_count()
            except LicenseStorageError as error:
                return self._denied(state, LIMIT_AUTO1_MAX_RUNS, str(error))
            if usage >= maximum:
                return EntitlementDecision(
                    allowed=False,
                    message=(
                        f"Community Edition Auto1 limit reached ({usage}/{maximum}). "
                        "Import a license to continue with unlimited Auto1 execution."
                    ),
                    edition=state.entitlements.edition,
                    required_feature=FEATURE_AUTO1_UNLIMITED,
                    current_usage=usage,
                    usage_limit=maximum,
                )
            return EntitlementDecision(
                allowed=True,
                message=f"Auto1 execution is available ({usage}/{maximum} Community runs used).",
                edition=state.entitlements.edition,
                required_feature=FEATURE_AUTO1_FULL,
                current_usage=usage,
                usage_limit=maximum,
            )

        if automation_id == "auto2":
            if mode not in {"test", "purchase"}:
                return self._unknown_mode_decision(state, "Auto2", mode)
            required = (
                FEATURE_AUTO2_FULL
                if mode == "purchase"
                else FEATURE_AUTO2_NAVIGATION_TEST
            )
            if entitlements.allows(FEATURE_AUTO2_FULL) or entitlements.allows(required):
                return self._allowed(state, required)
            return self._denied(state, required)

        if automation_id == "auto3":
            if mode not in {"test", "unlock"}:
                return self._unknown_mode_decision(state, "Auto3", mode)
            required = (
                FEATURE_AUTO3_FULL
                if mode == "unlock"
                else FEATURE_AUTO3_NAVIGATION_TEST
            )
            if entitlements.allows(FEATURE_AUTO3_FULL) or entitlements.allows(required):
                return self._allowed(state, required)
            return self._denied(state, required)

        return self._denied(
            state,
            f"FAA.{automation_id}.Full",
            "This automation is not available through the current entitlement boundary.",
        )

    def consume_auto1_execution(self) -> EntitlementDecision:
        """Atomically consume one Community run immediately before Auto1 starts."""
        state = self.current_state()
        entitlements = state.entitlements
        if entitlements.allows(FEATURE_AUTO1_UNLIMITED):
            return self._allowed(state, FEATURE_AUTO1_UNLIMITED)
        if not entitlements.allows(FEATURE_AUTO1_FULL):
            return self._denied(state, FEATURE_AUTO1_FULL)

        maximum = entitlements.limits.get(LIMIT_AUTO1_MAX_RUNS)
        if not isinstance(maximum, int):
            return self._denied(
                state,
                LIMIT_AUTO1_MAX_RUNS,
                "Auto1 execution limit is unavailable.",
            )
        try:
            allowed, usage = self.usage_store.consume_auto1_execution(maximum)
        except LicenseStorageError as error:
            return self._denied(state, LIMIT_AUTO1_MAX_RUNS, str(error))
        if not allowed:
            return EntitlementDecision(
                allowed=False,
                message=(
                    f"Community Edition Auto1 limit reached ({usage}/{maximum}). "
                    "Import a license to continue with unlimited Auto1 execution."
                ),
                edition=entitlements.edition,
                required_feature=FEATURE_AUTO1_UNLIMITED,
                current_usage=usage,
                usage_limit=maximum,
            )
        return EntitlementDecision(
            allowed=True,
            message=f"Auto1 execution started ({usage}/{maximum} Community runs used).",
            edition=entitlements.edition,
            required_feature=FEATURE_AUTO1_FULL,
            current_usage=usage,
            usage_limit=maximum,
        )

    def _import_verified_candidate(self, candidate: SignedLicense) -> LicenseImportResult:
        try:
            self.verifier.verify(candidate)
        except LicenseVerificationError as error:
            return self._rejected_import(str(error))

        current = self.current_state()
        if current.is_licensed:
            replacement_error = _replacement_error(current.license, candidate)
            if replacement_error is not None:
                return LicenseImportResult(False, current, replacement_error)

        try:
            self.storage.write(candidate.serialized_json)
        except LicenseStorageError as error:
            return LicenseImportResult(False, current, str(error))

        new_state = LicenseState(
            status="licensed",
            entitlements=entitlements_from_license(candidate),
            message=f"{candidate.payload.edition.title()} Edition license is active.",
            license=candidate,
        )
        return LicenseImportResult(True, new_state, "License imported successfully.")

    def _rejected_import(self, message: str) -> LicenseImportResult:
        return LicenseImportResult(False, self.current_state(), message)

    @staticmethod
    def _community_state(status: str, message: str) -> LicenseState:
        return LicenseState(status, community_entitlements(), message)

    @staticmethod
    def _allowed(state: LicenseState, feature: str) -> EntitlementDecision:
        return EntitlementDecision(
            True,
            "Execution is allowed by the current entitlement.",
            state.entitlements.edition,
            feature,
        )

    @staticmethod
    def _denied(
        state: LicenseState,
        feature: str,
        message: str | None = None,
    ) -> EntitlementDecision:
        return EntitlementDecision(
            False,
            message or (
                f"{feature} is not available in {state.entitlements.edition.title()} Edition. "
                "Import a license with this feature to continue."
            ),
            state.entitlements.edition,
            feature,
        )

    @staticmethod
    def _unknown_mode_decision(
        state: LicenseState,
        automation_name: str,
        mode: str | None,
    ) -> EntitlementDecision:
        display_mode = "missing" if mode is None else repr(mode)
        return EntitlementDecision(
            False,
            f"{automation_name} execution mode {display_mode} is not supported.",
            state.entitlements.edition,
            f"FAA.{automation_name}.KnownMode",
        )


def _replacement_error(
    current: SignedLicense | None,
    candidate: SignedLicense,
) -> str | None:
    if current is None:
        return None
    old = current.payload
    new = candidate.payload
    if old.license_id == new.license_id:
        if current.signature == candidate.signature:
            return None
        return "A different license with the current license ID cannot replace it."
    if old.discord_user_id != new.discord_user_id:
        return "Replacement license owner does not match the installed license."
    if new.issued_at <= old.issued_at:
        return "Replacement license must be newer than the installed license."
    if EDITION_RANKS[new.edition] < EDITION_RANKS[old.edition]:
        return "License downgrade was refused."
    if new.replaces_license_id is not None and new.replaces_license_id != old.license_id:
        return "Replacement reference does not match the installed license."
    return None
