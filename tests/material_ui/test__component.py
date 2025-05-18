from typing import Any

import pytest
from pytestqt.qtbot import QtBot

from material_ui._component import Component, State, _inject_state


@pytest.mark.parametrize(
    ("default_value", "type_"),
    [
        (2, int),
        (2.0, float),
        ("hello", str),
        (True, bool),
        (None, type(None)),
    ],
)
def test__inject_state_primitive_types(default_value: Any, type_: type):
    state = State(default_value, "", "")
    injected_value = _inject_state(default_value, state)
    assert isinstance(injected_value, type_)
    assert injected_value == default_value


# def test_hello(qtbot: QtBot):
#     component = Component()
#     component.focused
#     component.sx = {
#         "backgroundColor": "red",
#     }
