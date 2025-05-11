"""Tests for material_ui.tokens._core.py."""

import pytest
from material_ui.tokens._core import DesignToken, resolve_token, to_python_name
from material_ui.tokens import md_ref_palette, md_sys_color, md_comp_switch
from qtpy.QtGui import QColor


def test_resolve_token_direct_value() -> None:
    assert resolve_token(md_ref_palette.primary40) == QColor("#6750a4")


def test_resolve_token_indirection_1_level() -> None:
    assert resolve_token(md_sys_color.primary) == QColor("#6750a4")


def test_resolve_token_indirection_2_levels() -> None:
    assert resolve_token(md_comp_switch.focus_indicator_thickness) == 3


def test_resolve_token_invalid_indirection() -> None:
    with pytest.raises(ValueError):
        resolve_token(DesignToken("aksdhalf  flkjah lkjashd a"))


def test_to_python_name() -> None:
    result = to_python_name("md.comp.elevated-button.container-color")
    assert result == "md_comp_elevated_button_container_color"
