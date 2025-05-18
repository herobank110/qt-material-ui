from pytestqt.qtbot import QtBot

from material_ui._component import Component, use_state


class MyComponent(Component):
    a = use_state("")


def test_Component_state_bind_on_assignment(qtbot: QtBot):
    component1 = MyComponent()
    component1.a = "hello"
    qtbot.add_widget(component1)
    component2 = MyComponent()
    component2.a = "hey"
    qtbot.add_widget(component2)
    assert component1.a == "hello"
    assert component2.a == "hey"

    component2.a = component1.a
    assert component1.a == "hello"
    assert component2.a == "hello"

    component1.a = "hi"
    assert component1.a == "hi"
    assert component2.a == "hi"
