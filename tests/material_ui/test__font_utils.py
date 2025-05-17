import pytest
import httpx
from pytest_mock import MockerFixture
from material_ui._font_utils import _get_cache_path_for_url, download_font

_URL = "https://example.com/font.ttf"


@pytest.mark.asyncio
async def test_download_font_valid_response(mocker: MockerFixture) -> None:
    async with httpx.AsyncClient() as client:
        mocker.patch.object(
            client,
            "get",
            return_value=mocker.Mock(status_code=200, content=b"font data"),
        )
        result = await download_font(client, _URL)
    assert result is not None


def test__get_cache_path_for_url_returns_valid_str() -> None:
    assert len(str(_get_cache_path_for_url(_URL))) > 10


def test__get_cache_path_for_url_returns_same_str() -> None:
    assert _get_cache_path_for_url(_URL) == _get_cache_path_for_url(_URL)
    assert _get_cache_path_for_url(_URL) != _get_cache_path_for_url(_URL + "2")
