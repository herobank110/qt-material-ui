from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from material_ui._component import Component, effect, use_state


def test_Component_state_bind_on_assignment(qtbot: QtBot):
    class C(Component):
        a = use_state("")

    c1 = C()
    c1.a = "hello"
    qtbot.add_widget(c1)
    c2 = C()
    c2.a = "hey"
    qtbot.add_widget(c2)
    assert c1.a == "hello"
    assert c2.a == "hey"

    c2.a = c1.a
    assert c1.a == "hello"
    assert c2.a == "hello"

    c1.a = "hi"
    assert c1.a == "hi"
    assert c2.a == "hi"


def test_Component_effect_is_called_on_deps(qtbot: QtBot, mocker: MockerFixture):
    stub = mocker.stub()

    class C(Component):
        a = use_state("hello")

        @effect(a)
        def a_effect(self):
            stub(self.a)

    c = C()
    qtbot.add_widget(c)

    assert stub.call_count == 1
    assert stub.call_args == mocker.call("hello")

    c.a = "hi"
    assert stub.call_count == 2
    assert stub.call_args == mocker.call("hi")
