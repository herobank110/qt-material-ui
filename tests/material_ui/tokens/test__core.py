"""Tests for material_ui.tokens._core.py."""

from material_ui.tokens._core import resolve_token, to_python_name
from qtpy.QtGui import QColor


def test_resolve_token_direct_value() -> None:
    assert resolve_token("md.ref.palette.primary40") == QColor("#6750a4")


def test_resolve_token_indirection() -> None:
    assert resolve_token("md.sys.color.primary") == QColor("#6750a4")


def test_to_python_name() -> None:
    result = to_python_name("md.comp.elevated-button.container-color")
    assert result == "md_comp_elevated_button_container_color"
