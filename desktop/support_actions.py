"""Desktop actions for opening official product support."""

from collections.abc import Callable

from product.support import OFFICIAL_DISCORD_URL


def open_official_discord(
    opener: Callable[[str], bool] | None = None,
) -> bool:
    """Open the official Discord invite, with injectable behavior for tests."""
    if opener is not None:
        return bool(opener(OFFICIAL_DISCORD_URL))

    from PySide6.QtCore import QUrl
    from PySide6.QtGui import QDesktopServices

    return bool(QDesktopServices.openUrl(QUrl(OFFICIAL_DISCORD_URL)))
