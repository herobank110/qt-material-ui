from material_ui._font_utils import _get_cache_path_for_url

_URL = "https://example.com/font.ttf"


# def test_download_font_basic(monkeypatch: MonkeyPath):
#     assert len(str(_get_cache_path_for_url(url))) > 10


def test__get_cache_path_for_url_returns_valid_str():
    assert len(str(_get_cache_path_for_url(_URL))) > 10


def test__get_cache_path_for_url_returns_same_str():
    assert _get_cache_path_for_url(_URL) == _get_cache_path_for_url(_URL)
    assert _get_cache_path_for_url(_URL) != _get_cache_path_for_url(_URL + "2")
