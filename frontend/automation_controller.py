from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from product.automation_definition import AutomationDefinition
from product.automation_registry import AUTOMATION_DEFINITIONS
from product.profile_metadata import ProfileMetadata
from product.profile_metadata_registry import PROFILE_METADATA
from product.readiness_model import ReadinessModel
from product.readiness_registry import READINESS_MODELS
from sessions.run_session import RunSession
from sessions.session_status import SessionStatus


class RefusalReason(str, Enum):
    UNKNOWN_AUTOMATION = "unknown_automation"
    INACTIVE_AUTOMATION = "inactive_automation"
    UNKNOWN_PROFILE = "unknown_profile"
    PROFILE_MISMATCH = "profile_mismatch"
    INVALID_REQUESTED_COUNT = "invalid_requested_count"
    MISSING_READINESS_MODEL = "missing_readiness_model"


@dataclass(frozen=True)
class AutomationRunRequest:
    automation_id: str
    profile_id: str
    requested_count: int
    mode: str | None = None
    acknowledgement_ids: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class AutomationRunPlan:
    request: AutomationRunRequest
    accepted: bool
    automation_definition: AutomationDefinition | None = None
    profile_metadata: ProfileMetadata | None = None
    readiness_model: ReadinessModel | None = None
    session_preview: RunSession | None = None
    refusal_reason: RefusalReason | None = None
    refusal_message: str | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)


class FrontendAutomationController:
    def __init__(
        self,
        session_id_provider: Callable[[], str] | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._session_id_provider = session_id_provider or self._default_session_id
        self._clock = clock or self._default_clock

    def prepare_run_plan(
        self,
        request: AutomationRunRequest,
    ) -> AutomationRunPlan:
        if request.requested_count <= 0:
            return self._refuse(
                request=request,
                reason=RefusalReason.INVALID_REQUESTED_COUNT,
                message="Run was not prepared because the requested count must be greater than zero.",
            )

        automation_definition = AUTOMATION_DEFINITIONS.get(request.automation_id)
        if automation_definition is None:
            return self._refuse(
                request=request,
                reason=RefusalReason.UNKNOWN_AUTOMATION,
                message="Run was not prepared because the automation is not known.",
            )

        if not automation_definition.is_active:
            return self._refuse(
                request=request,
                reason=RefusalReason.INACTIVE_AUTOMATION,
                message="Run was not prepared because this automation is not active.",
                automation_definition=automation_definition,
            )

        profile_metadata = PROFILE_METADATA.get(request.profile_id)
        if profile_metadata is None:
            return self._refuse(
                request=request,
                reason=RefusalReason.UNKNOWN_PROFILE,
                message="Run was not prepared because the selected profile is not known.",
                automation_definition=automation_definition,
            )

        if request.profile_id not in automation_definition.available_profiles:
            return self._refuse(
                request=request,
                reason=RefusalReason.PROFILE_MISMATCH,
                message="Run was not prepared because the selected profile does not belong to this automation.",
                automation_definition=automation_definition,
                profile_metadata=profile_metadata,
            )

        readiness_model = READINESS_MODELS.get(request.automation_id)
        if readiness_model is None:
            return self._refuse(
                request=request,
                reason=RefusalReason.MISSING_READINESS_MODEL,
                message="Run was not prepared because readiness guidance is not available.",
                automation_definition=automation_definition,
                profile_metadata=profile_metadata,
            )

        session_preview = self._build_session_preview(
            request=request,
            status=SessionStatus.PREPARED,
            warnings=readiness_model.contextual_warnings,
            summary=(
                f"{automation_definition.display_name} is prepared for "
                f"{request.requested_count} requested run(s)."
            ),
            suggested_next_step="Review readiness assumptions before starting execution.",
        )

        return AutomationRunPlan(
            request=request,
            accepted=True,
            automation_definition=automation_definition,
            profile_metadata=profile_metadata,
            readiness_model=readiness_model,
            session_preview=session_preview,
            warnings=readiness_model.contextual_warnings,
        )

    def _refuse(
        self,
        request: AutomationRunRequest,
        reason: RefusalReason,
        message: str,
        automation_definition: AutomationDefinition | None = None,
        profile_metadata: ProfileMetadata | None = None,
    ) -> AutomationRunPlan:
        session_preview = self._build_session_preview(
            request=request,
            status=SessionStatus.REFUSED,
            warnings=(),
            summary=message,
            suggested_next_step="Review the request and try again when the safety boundary is satisfied.",
        )

        return AutomationRunPlan(
            request=request,
            accepted=False,
            automation_definition=automation_definition,
            profile_metadata=profile_metadata,
            session_preview=session_preview,
            refusal_reason=reason,
            refusal_message=message,
        )

    def _build_session_preview(
        self,
        request: AutomationRunRequest,
        status: SessionStatus,
        warnings: tuple[str, ...],
        summary: str,
        suggested_next_step: str,
    ) -> RunSession:
        return RunSession(
            session_id=self._session_id_provider(),
            automation_id=request.automation_id,
            profile_id=request.profile_id,
            requested_count=request.requested_count,
            completed_count=0,
            status=status,
            started_at=self._clock(),
            warnings_encountered=warnings,
            user_facing_summary=summary,
            suggested_next_step=suggested_next_step,
        )

    def _default_session_id(self) -> str:
        return f"preview-{uuid4()}"

    def _default_clock(self) -> datetime:
        return datetime.now(timezone.utc)
