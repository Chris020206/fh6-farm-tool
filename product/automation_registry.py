from product.automation_definition import AutomationDefinition
from product.risk_levels import RiskLevel


AUTOMATION_DEFINITIONS: dict[str, AutomationDefinition] = {
    "auto1": AutomationDefinition(
        automation_id="auto1",
        display_name="Auto1 — Race Automation",
        short_purpose="Repeat race farming through a validated restart flow.",
        long_purpose=(
            "Auto1 helps repeat a validated race flow using controlled restart "
            "behavior and guarded execution assumptions."
        ),
        risk_level=RiskLevel.LOW,
        validated_scope="Validated restart-screen race automation flow.",
        expected_baseline="FH6 positioned at validated restart screen.",
        available_profiles=["auto1_race_default"],
        supported_modes=["standard"],
        contextual_warnings=[
            "Requires validated FH6 starting position."
        ],
        suggested_next_step="Review recent run in Operational History.",
    ),
    "auto2": AutomationDefinition(
        automation_id="auto2",
        display_name="Auto2 — Buy Car Automation",
        short_purpose="Purchase vehicles using a validated Autoshow traversal path.",
        long_purpose=(
            "Auto2 follows a controlled Autoshow traversal process with "
            "explicit safety boundaries around purchase execution."
        ),
        risk_level=RiskLevel.CONTROLLED,
        validated_scope="Validated Autoshow purchase traversal.",
        expected_baseline="FH6 positioned at Autoshow with expected cursor placement.",
        available_profiles=["auto2_buy_car_default"],
        supported_modes=["single_purchase", "repeat_purchase"],
        contextual_warnings=[
            "Manufacturer ordering assumptions may change in FH6 updates."
        ],
        suggested_next_step="Auto3 may follow depending on vehicle goals.",
    ),
    "auto3": AutomationDefinition(
        automation_id="auto3",
        display_name="Auto3 — Skill Tree Automation",
        short_purpose="Unlock validated skill-tree paths with controlled traversal.",
        long_purpose=(
            "Auto3 executes validated skill-tree traversal with bounded "
            "navigation and protected unlock assumptions."
        ),
        risk_level=RiskLevel.CONTROLLED,
        validated_scope="Validated multi-step skill-tree traversal.",
        expected_baseline="FH6 positioned on expected seated vehicle baseline.",
        available_profiles=["auto3_skill_tree_default"],
        supported_modes=["test", "unlock"],
        contextual_warnings=[
            "Requires validated garage and vehicle positioning assumptions."
        ],
        suggested_next_step="Review completion details in Operational History.",
    ),
    "auto4": AutomationDefinition(
        automation_id="auto4",
        display_name="Auto4 — Remove Car Automation",
        short_purpose="Future controlled removal automation.",
        long_purpose=(
            "Auto4 is reserved for a future validated vehicle removal flow "
            "once safety boundaries are finalized."
        ),
        risk_level=RiskLevel.HIGH,
        validated_scope="Not yet active.",
        expected_baseline="Unavailable.",
        package_tier="plus",
        maturity_status="future",
        is_active=False,
    ),
}


def get_automation_definition(automation_id: str) -> AutomationDefinition:
    return AUTOMATION_DEFINITIONS[automation_id]



def get_all_automation_definitions() -> list[AutomationDefinition]:
    return list(AUTOMATION_DEFINITIONS.values())



def get_active_automation_definitions() -> list[AutomationDefinition]:
    return [
        definition
        for definition in AUTOMATION_DEFINITIONS.values()
        if definition.is_active
    ]
