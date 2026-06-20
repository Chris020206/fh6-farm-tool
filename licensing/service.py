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
    LIMIT_AUTO1_MAX_LOOPS_PER_EXECUTION,
)
from licensing.entitlements import (
    LICENSED_AUTO1_MAX_LOOPS_PER_EXECUTION,
    community_entitlements,
    entitlements_from_license,
)
from licensing.models import (
    EntitlementDecision,
    LicenseImportResult,
    LicenseState,
    SignedLicense,
)
from licensing.parsing import LicenseParseError, parse_license_key, parse_signed_license_json
from licensing.storage import LicenseStorage, LicenseStorageError
from licensing.verification import LicenseVerificationError, LicenseVerifier


class LicenseService:
    def __init__(
        self,
        storage: LicenseStorage | None = None,
        verifier: LicenseVerifier | None = None,
    ) -> None:
        self.storage = storage or LicenseStorage()
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

    def evaluate_execution(
        self,
        automation_id: str,
        mode: str | None = None,
        requested_count: int | None = None,
    ) -> EntitlementDecision:
        """Evaluate an execution request without mutating local state."""
        state = self.current_state()
        entitlements = state.entitlements

        if automation_id == "auto1":
            if entitlements.allows(FEATURE_AUTO1_UNLIMITED):
                maximum = LICENSED_AUTO1_MAX_LOOPS_PER_EXECUTION
                required_feature = FEATURE_AUTO1_UNLIMITED
            else:
                if not entitlements.allows(FEATURE_AUTO1_FULL):
                    return self._denied(state, FEATURE_AUTO1_FULL)
                maximum = entitlements.limits.get(
                    LIMIT_AUTO1_MAX_LOOPS_PER_EXECUTION
                )
                required_feature = FEATURE_AUTO1_FULL

            if isinstance(maximum, bool) or not isinstance(maximum, int):
                return self._denied(
                    state,
                    LIMIT_AUTO1_MAX_LOOPS_PER_EXECUTION,
                    "Auto1 per-execution loop limit is unavailable.",
                )
            if maximum < 1:
                return self._denied(
                    state,
                    LIMIT_AUTO1_MAX_LOOPS_PER_EXECUTION,
                    "Auto1 per-execution loop limit is invalid.",
                )
            if requested_count is not None:
                if (
                    isinstance(requested_count, bool)
                    or not isinstance(requested_count, int)
                    or requested_count < 1
                ):
                    return self._denied(
                        state,
                        required_feature,
                        "Auto1 loop count must be a positive integer.",
                    )
                if requested_count > maximum:
                    return self._denied(
                        state,
                        required_feature,
                        (
                            f"{state.entitlements.edition.title()} Edition allows "
                            f"at most {maximum} Auto1 loops per execution."
                        ),
                    )
            return EntitlementDecision(
                allowed=True,
                message=(
                    f"Auto1 execution is available for up to {maximum} loop(s) "
                    "per execution."
                ),
                edition=state.entitlements.edition,
                required_feature=required_feature,
                max_loops_per_execution=maximum,
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
