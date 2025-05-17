from typing import Any
import pytest
import httpx
from pytest_mock import MockerFixture
from material_ui._font_utils import _get_cache_path_for_url, download_font

_URL = "https://example.com/font.ttf"
"""Sample URL for font download tests."""


_VALID_RESPONSE = httpx.Response(status_code=200, content=b"data")
_INVALID_RESPONSE = httpx.Response(status_code=500)


@pytest.fixture(autouse=True, scope="function")
def clear_cached_font() -> None:
    """Delete the cached font file before each test.

    Ideally it should mock the file writing, but they are only small
    files.
    """
    _get_cache_path_for_url(_URL).unlink(missing_ok=True)


@pytest.fixture
def client() -> httpx.AsyncClient:
    """Fixture to create an HTTP client for testing."""
    return httpx.AsyncClient()


@pytest.mark.asyncio
async def test_download_font_valid_response(
    mocker: MockerFixture, client: httpx.AsyncClient
) -> None:
    mocker.patch.object(client, "get", return_value=_VALID_RESPONSE)
    result = await download_font(client, _URL)
    assert result is not None


@pytest.mark.asyncio
async def test_download_font_invalid_response(
    mocker: MockerFixture, client: httpx.AsyncClient
) -> None:
    mocker.patch.object(client, "get", return_value=_INVALID_RESPONSE)
    result = await download_font(client, _URL)
    assert result is None


@pytest.mark.asyncio
async def test_download_font_no_refetch_if_cached(
    mocker: MockerFixture, client: httpx.AsyncClient
) -> None:
    mock_get = mocker.patch.object(client, "get", return_value=_VALID_RESPONSE)

    result1 = await download_font(client, _URL)
    assert result1 is not None
    assert mock_get.call_count == 1

    result2 = await download_font(client, _URL)
    assert result1 == result2
    assert mock_get.call_count == 1


def test__get_cache_path_for_url_returns_valid_str() -> None:
    assert len(str(_get_cache_path_for_url(_URL))) > 10


def test__get_cache_path_for_url_returns_same_str() -> None:
    assert _get_cache_path_for_url(_URL) == _get_cache_path_for_url(_URL)
    assert _get_cache_path_for_url(_URL) != _get_cache_path_for_url(_URL + "2")
