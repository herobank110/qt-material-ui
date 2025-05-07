"""Tests for material_ui.tokens._core.py."""

from material_ui.tokens._core import resolve_token
from qtpy.QtGui import QColor


def test_resolve_token_indirection() -> None:
    assert resolve_token("md.sys.color.primary") == QColor("#6200ee")
