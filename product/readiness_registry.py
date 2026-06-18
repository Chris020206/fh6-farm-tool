from product.readiness_model import AcknowledgementLevel, ReadinessModel


READINESS_MODELS: dict[str, ReadinessModel] = {
    "auto1": ReadinessModel(
        automation_id="auto1",
        expected_baseline=(
            "Required Starting Position: post-race Restart screen. Complete one race "
            "first, then stay on the screen where pressing X restarts the event."
        ),
        manual_positioning_assumption=(
            "Assumed operator setup: Auto1 is used for repeated race automation from "
            "the validated restart screen."
        ),
        recommended_setup=(
            "Purpose: repeated race automation.",
            "Expected Result: repeated race restart and completion.",
            "Need help? See Help -> Auto1 Guide.",
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
            "Required Starting Position: Autoshow, at the validated buy-car menu "
            "baseline."
        ),
        manual_positioning_assumption=(
            "Target vehicle: Subaru Impreza 22B-STi Version (1998). Auto2 is "
            "designed around purchasing this specific validated wheelspin workflow vehicle."
        ),
        recommended_setup=(
            "Purpose: purchase the validated wheelspin vehicle.",
            "Expected Result: purchases the selected validated Subaru.",
            "Run test-mode navigation before any purchase validation when alignment is uncertain.",
            "Use the official profile unless a validated custom timing profile is intentionally selected.",
            "Need help? See Help -> Auto2 Guide.",
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
            "Auto2 has validated test-mode navigation and purchase-count execution.",
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
            "Required Starting Position: Garage -> Cars -> My Cars -> Recently Added."
        ),
        manual_positioning_assumption=(
            "Target vehicle assumption: Auto3 unlocks perks on the currently selected "
            "vehicle. It does not independently verify the car model."
        ),
        recommended_setup=(
            "Purpose: unlock the validated wheelspin perk path.",
            "The currently selected vehicle should be the first newly purchased Subaru Impreza 22B-STi Version (1998).",
            "Use start row A only.",
            "Expected Result: unlocks the validated perk path for the selected/newly purchased Subaru vehicles.",
            "Keep car count at or below the guarded four-car validation boundary.",
            "Need help? See Help -> Auto3 Guide.",
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
