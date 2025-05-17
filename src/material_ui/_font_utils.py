"""Utilities for internal default fonts."""

from functools import cache
import httpx
from pathlib import Path
from tempfile import gettempdir
from hashlib import md5


@cache
async def download_font(client: httpx.AsyncClient, url: str) -> Path:
    """Fetch a font from a URL and save to disk.

    If the font is already cached from a previous program run, it will be reused.

    Args:
        client: The HTTP client to use.
        url: The URL of the font to fetch.

    Returns:
        Path to the downloaded font file on disk.
    """

    file_path = _get_cache_path_for_url(url)

    if not file_path.exists():
        resp = await client.get(url)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(resp.content)

    return file_path


def _get_cache_path_for_url(url: str) -> Path:
    return _get_font_cache_dir() / md5(url.encode()).hexdigest()


def _get_font_cache_dir() -> Path:
    """Get the path to the font cache directory."""
    return Path(gettempdir()) / "qt-material-ui" / "font_cache"
