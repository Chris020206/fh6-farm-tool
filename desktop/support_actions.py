"""Desktop actions for opening official product support."""

from collections.abc import Callable

from product.support import OFFICIAL_DISCORD_URL, OFFICIAL_YOUTUBE_URL


def open_official_discord(
    opener: Callable[[str], bool] | None = None,
) -> bool:
    """Open the official Discord invite, with injectable behavior for tests."""
    return _open_external_url(OFFICIAL_DISCORD_URL, opener)


def open_official_youtube(
    opener: Callable[[str], bool] | None = None,
) -> bool:
    """Open the official FAA YouTube channel."""
    return _open_external_url(OFFICIAL_YOUTUBE_URL, opener)


def _open_external_url(
    url: str,
    opener: Callable[[str], bool] | None,
) -> bool:
    if opener is not None:
        return bool(opener(url))

    from PySide6.QtCore import QUrl
    from PySide6.QtGui import QDesktopServices

    return bool(QDesktopServices.openUrl(QUrl(url)))
