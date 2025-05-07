"""Tests for material_ui.tokens._core.py."""

import pytest
from material_ui.tokens._core import resolve_token, to_python_name
from qtpy.QtGui import QColor


def test_resolve_token_direct_value() -> None:
    assert resolve_token("md.ref.palette.primary40") == QColor("#6750a4")


def test_resolve_token_indirection_1_level() -> None:
    assert resolve_token("md.sys.color.primary") == QColor("#6750a4")


def test_resolve_token_indirection_2_levels() -> None:
    assert resolve_token("md.comp.switch.focus-indicator.thickness") == 3


def test_resolve_token_invalid_token() -> None:
    with pytest.raises(ValueError):
        resolve_token("aksdhalf  flkjah lkjashd a")


def test_to_python_name() -> None:
    result = to_python_name("md.comp.elevated-button.container-color")
    assert result == "md_comp_elevated_button_container_color"
