from typing import Any

import pytest
from pytestqt.qtbot import QtBot

from material_ui._component import Component, use_state

# @pytest.mark.parametrize(
#     ("default_value", "type_"),
#     [
#         (2, int),
#         (2.0, float),
#         ("hello", str),
#         (True, bool),
#         (None, type(None)),
#     ],
# )
# def test__inject_state_primitive_types(default_value: Any, type_: type):
#     state = State(default_value, "", "")
#     injected_value = _inject_state(default_value, state)
#     assert isinstance(injected_value, type_)
#     assert injected_value == default_value


class MyComponent(Component):
    a = use_state(0)


def test_Component_state_bind_on_assignment(qtbot: QtBot):
    component1 = MyComponent()
    qtbot.add_widget(component1)
    component2 = MyComponent()
    qtbot.add_widget(component2)
    component2.a = component1.a
    assert component1.a == 0
    assert component2.a == 0
    component1.a = 1
    assert component1.a == 1
    assert component2.a == 1
