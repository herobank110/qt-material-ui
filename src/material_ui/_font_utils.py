"""Utilities for internal default fonts."""

import httpx
from pathlib import Path
from tempfile import gettempdir
from hashlib import md5


async def download_font(
    client: httpx.AsyncClient, url: str, no_cache: bool = False
) -> Path | None:
    """Fetch a font from a URL and save to disk.

    Args:
        client: The HTTP client to use.
        url: The URL of the font to fetch.
        no_cache: If True, ignore the cached file.

    Returns:
        Path to the downloaded font file on disk, or None if it failed.
    """

    file_path = _get_cache_path_for_url(url)

    if no_cache or not file_path.exists():
        resp = await client.get(url)
        if resp.status_code != 200:
            return None
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(resp.content)

    return file_path


def _get_cache_path_for_url(url: str) -> Path:
    return _get_font_cache_dir() / md5(url.encode()).hexdigest()


def _get_font_cache_dir() -> Path:
    """Get the path to the font cache directory."""
    return Path(gettempdir()) / "qt-material-ui" / "font_cache"
