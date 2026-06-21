"""Shared product support references and user-facing licensing guidance."""

OFFICIAL_DISCORD_URL = "https://discord.gg/SgARD8YenU"


def license_activation_failure_message() -> str:
    return (
        "License could not be activated.\n\n"
        "The selected license file was invalid or could not be verified.\n\n"
        "Your current edition has not been changed.\n\n"
        "For documentation, edition information, and support, visit the official "
        "FAA Discord."
    )


def community_feature_unavailable_message() -> str:
    return (
        "This feature requires a different FAA edition.\n\n"
        "Your current edition:\n"
        "Community Edition\n\n"
        "Included features:\n"
        "• Auto1 Community\n"
        "• Auto2 Navigation Test\n"
        "• Auto3 Navigation Test\n\n"
        "For documentation, edition information and support,\n"
        "visit the official FAA Discord."
    )
