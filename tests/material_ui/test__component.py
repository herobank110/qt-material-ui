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
    ],
)
def test__inject_state_primitive_types(default_value: Any, type_: type):
    state = State(default_value, "state", "")
    injected_value = _inject_state(default_value, state)
    assert isinstance(injected_value, type_)
    assert injected_value == default_value


def test__inject_state_float():
    value = 2.0
    state = State(value, "state", "")
    injected_value = _inject_state(value, state)
    assert isinstance(injected_value, float)
    assert injected_value == 2.0


# def test_hello(qtbot: QtBot):
#     component = Component()
#     component.focused
#     component.sx = {
#         "backgroundColor": "red",
#     }
