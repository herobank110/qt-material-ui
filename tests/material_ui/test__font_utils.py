import pytest
import httpx
from pytest_mock import MockerFixture
from material_ui._font_utils import _get_cache_path_for_url, _download_font

_URL = "https://example.com/font.ttf"
_VALID_RESPONSE = httpx.Response(status_code=200, content=b"data")
_INVALID_RESPONSE = httpx.Response(status_code=500)


@pytest.fixture(autouse=True, scope="function")
def clear_cached_font() -> None:
    """Delete the cached font file before each test."""
    _get_cache_path_for_url(_URL).unlink(missing_ok=True)


@pytest.fixture
def client() -> httpx.AsyncClient:
    """Fixture to create a HTTP client for testing."""
    return httpx.AsyncClient()


@pytest.mark.asyncio
async def test__download_font_valid_response(
    mocker: MockerFixture, client: httpx.AsyncClient
) -> None:
    mocker.patch.object(client, "get", return_value=_VALID_RESPONSE)
    result = await _download_font(client, _URL)
    assert result is not None


@pytest.mark.asyncio
async def test__download_font_invalid_response(
    mocker: MockerFixture, client: httpx.AsyncClient
) -> None:
    mocker.patch.object(client, "get", return_value=_INVALID_RESPONSE)
    result = await _download_font(client, _URL)
    assert result is None


@pytest.mark.asyncio
async def test__download_font_no_refetch_if_cached(
    mocker: MockerFixture, client: httpx.AsyncClient
) -> None:
    mock_get = mocker.patch.object(client, "get", return_value=_VALID_RESPONSE)

    result1 = await _download_font(client, _URL)
    assert result1 is not None
    assert mock_get.call_count == 1

    # Already fetched, don't refetch
    result2 = await _download_font(client, _URL)
    assert result1 == result2
    assert mock_get.call_count == 1

    # With nocache, it should refetch
    result3 = await _download_font(client, _URL, no_cache=True)
    assert result1 == result3
    assert mock_get.call_count == 2


def test__get_cache_path_for_url_returns_valid_str() -> None:
    assert len(str(_get_cache_path_for_url(_URL))) > 10


def test__get_cache_path_for_url_returns_same_str() -> None:
    assert _get_cache_path_for_url(_URL) == _get_cache_path_for_url(_URL)
    assert _get_cache_path_for_url(_URL) != _get_cache_path_for_url(_URL + "2")
