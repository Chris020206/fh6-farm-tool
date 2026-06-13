from product.readiness_model import AcknowledgementLevel, ReadinessModel


READINESS_MODELS: dict[str, ReadinessModel] = {
    "auto1": ReadinessModel(
        automation_id="auto1",
        expected_baseline=(
            "Expected FH6 baseline: post-race restart screen where pressing X restarts "
            "the event."
        ),
        manual_positioning_assumption=(
            "Assumed operator setup: FH6 is focused and positioned at the validated "
            "Auto1 restart baseline before execution starts."
        ),
        recommended_setup=(
            "Use the validated race setup and car assumptions from the Auto1 runbook.",
            "Keep FH6 focused before the startup delay finishes.",
            "Keep F8 ready for supervised stop control.",
        ),
        focus_requirement="FH6 should be the focused application before real input starts.",
        cursor_requirement=None,
        acknowledgement_level=AcknowledgementLevel.STANDARD,
        readiness_wording=(
            "Ready when the expected restart baseline is visible and the operator is "
            "prepared to supervise finite cycles."
        ),
        confidence_notes=(
            "Auto1 has a validated guarded/manual race restart flow.",
            "Readiness is based on operator positioning, not live FH6 state detection.",
        ),
        contextual_warnings=(
            "If a different menu is visible, stop before running Auto1.",
            "If focus changes during execution, use F8 and return to the baseline manually.",
        ),
        blocked_or_refused_conditions=(
            "Missing confirmation for guarded real-input execution.",
            "Invalid or non-positive cycle count.",
        ),
    ),
    "auto2": ReadinessModel(
        automation_id="auto2",
        expected_baseline=(
            "Expected FH6 baseline: Autoshow/menu state aligned with the official "
            "Auto2 navigation assumptions."
        ),
        manual_positioning_assumption=(
            "Assumed operator setup: FH6 is focused, Autoshow navigation starts from "
            "the documented baseline, and spending risk is understood before purchase testing."
        ),
        recommended_setup=(
            "Run test-mode navigation before any purchase validation when alignment is uncertain.",
            "Use the official profile unless a validated custom timing profile is intentionally selected.",
            "Confirm sufficient credits before the one-car purchase validation command.",
        ),
        focus_requirement="FH6 should remain focused for the full guarded real-input sequence.",
        cursor_requirement=(
            "Cursor should not interfere with menu navigation or FH6 focus during execution."
        ),
        acknowledgement_level=AcknowledgementLevel.DOUBLE_CONFIRMATION,
        readiness_wording=(
            "Ready only when the expected Autoshow baseline is prepared and the operator "
            "accepts the controlled spending risk."
        ),
        confidence_notes=(
            "Auto2 has validated test-mode navigation and one-car purchase validation.",
            "Readiness is assumption-based and does not inspect the active FH6 menu.",
        ),
        contextual_warnings=(
            "Purchase validation can spend credits.",
            "Unexpected manufacturer, car, or confirmation screens should be treated as misalignment.",
        ),
        blocked_or_refused_conditions=(
            "Missing real-input confirmation.",
            "Missing purchase confirmation for purchase validation.",
            "Cycle count other than one for the one-car purchase harness.",
        ),
    ),
    "auto3": ReadinessModel(
        automation_id="auto3",
        expected_baseline=(
            "Expected FH6 baseline: My Cars grid using the validated A-row start "
            "assumption and official Auto3 sorting setup."
        ),
        manual_positioning_assumption=(
            "Assumed operator setup: user starts from the documented garage baseline, "
            "with traversal limited to the current validated A1 to A2 path."
        ),
        recommended_setup=(
            "Use the start row A baseline.",
            "Keep car count at or below the guarded four-car validation boundary.",
            "Confirm skill point spending is acceptable before unlock testing.",
        ),
        focus_requirement="FH6 should remain focused during guarded real-input traversal and unlock.",
        cursor_requirement=None,
        acknowledgement_level=AcknowledgementLevel.DOUBLE_CONFIRMATION,
        readiness_wording=(
            "Ready when the validated My Cars baseline is prepared, start row A is used, "
            "and the operator accepts bounded skill point spending."
        ),
        confidence_notes=(
            "Auto3 traversal has been validated for A1 to B1 to C1 to A2 within guarded manual use.",
            "Readiness depends on operator baseline setup, not automatic game-state verification.",
        ),
        contextual_warnings=(
            "Auto3 real-input unlock commands can spend skill points.",
            "Starting from B or C rows is outside the current validated boundary.",
            "More than four cars is outside the current guarded validation limit.",
        ),
        blocked_or_refused_conditions=(
            "Missing real-input confirmation.",
            "Missing unlock confirmation for unlock testing.",
            "Car count above the guarded validation limit.",
        ),
    ),
}


def get_readiness_model(automation_id: str) -> ReadinessModel:
    return READINESS_MODELS[automation_id]


def get_all_readiness_models() -> list[ReadinessModel]:
    return list(READINESS_MODELS.values())
