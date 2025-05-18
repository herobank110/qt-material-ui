from qtpy.QtGui import QColor
import pytest
from material_ui._utils import _stringify_sx_value


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (QColor(255, 0, 0, 255), "rgba(255,0,0,255)"),
        (QColor("#dad666"), "rgba(218,214,102,255)"),
        (QColor.fromRgbF(0.5, 0.5, 0.25, 0.72), "rgba(128,128,64,184)"),
    ],
)
def test_stringify_sx_value_qcolor(value: QColor, expected: str) -> None:
    assert _stringify_sx_value(value) == expected


def test_stringify_sx_value_string() -> None:
    assert _stringify_sx_value("30px") == "30px"
    assert _stringify_sx_value("1px solid red") == "1px solid red"
