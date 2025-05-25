"""Utilities for internal default fonts."""

import asyncio
from functools import cache, partial
from hashlib import md5
from pathlib import Path
from tempfile import gettempdir

import httpx
from qtpy.QtGui import QFontDatabase

_FONT_URLS = [
    "https://raw.githubusercontent.com/google/material-design-icons/refs/heads/master/variablefont/MaterialSymbolsOutlined[FILL,GRAD,opsz,wght].ttf",
    "https://raw.githubusercontent.com/google/material-design-icons/refs/heads/master/variablefont/MaterialSymbolsRounded[FILL,GRAD,opsz,wght].ttf",
    "https://raw.githubusercontent.com/google/material-design-icons/refs/heads/master/variablefont/MaterialSymbolsSharp[FILL,GRAD,opsz,wght].ttf",
    # Regular
    "https://fonts.gstatic.com/s/roboto/v47/KFOmCnqEu92Fr1Me5WZLCzYlKw.ttf",
    # Italic
    # https://fonts.gstatic.com/s/roboto/v47/KFOkCnqEu92Fr1Mu52xPKTM1K9nz.ttf
]


@cache
def install_default_fonts() -> bool:
    """Apply the material fonts to the QFontDatabase.

    Returns:
        Whether all fonts were successfully installed.
    """
    file_paths = asyncio.run(_download_all_fonts())
    font_ids = [
        QFontDatabase.addApplicationFont(str(font_path))
        for font_path in filter(None, file_paths)
    ]
    return all(file_paths) and all(font_id != -1 for font_id in font_ids)


async def _download_all_fonts() -> list[Path | None]:
    async with httpx.AsyncClient() as client:
        return await asyncio.gather(*map(partial(_download_font, client), _FONT_URLS))


async def _download_font(
    client: httpx.AsyncClient,
    url: str,
    *,
    no_cache: bool = False,
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
        if resp.status_code != httpx.codes.OK:
            return None
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("wb") as f:
            f.write(resp.content)

    return file_path


def _get_cache_path_for_url(url: str) -> Path:
    return _get_font_cache_dir() / md5(url.encode(), usedforsecurity=False).hexdigest()


def _get_font_cache_dir() -> Path:
    """Get the path to the font cache directory."""
    return Path(gettempdir()) / "qt-material-ui" / "font_cache"
