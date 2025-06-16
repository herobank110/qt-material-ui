import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from material_ui._component import Component, EffectDependencyError, effect, use_state
from material_ui.hook import Hook


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


def test_Component_effect_called_initially_and_on_change(
    qtbot: QtBot,
    mocker: MockerFixture,
):
    stub = mocker.stub()

    class C(Component):
        a = use_state("hello")

        @effect(a)
        def my_effect(self) -> None:
            stub(self.a)

    c = C()
    qtbot.add_widget(c)
    # Wait for the effect to be called after constructor.
    qtbot.wait_callback(timeout=0, raising=False).wait()

    # Check initial state call.
    stub.assert_called_once_with("hello")

    # New value assigned - effect should be called again.
    c.a = "hi"
    assert stub.call_count == 2
    stub.assert_called_with("hi")


def test_Component_effect_invalid_dependency_literal():
    with pytest.raises(EffectDependencyError):

        class C(Component):  # pyright: ignore[reportUnusedClass]
            @effect("hi")
            def my_effect(self) -> None:
                pass


def test_Component_effect_invalid_dependency_static():
    with pytest.raises(EffectDependencyError):

        class C(Component):  # pyright: ignore[reportUnusedClass]
            f = "hi"

            @effect(f)
            def my_effect(self) -> None:
                pass


def test_Component_effect_hook_dependency(qtbot: QtBot, mocker: MockerFixture):
    stub = mocker.stub()

    class MyHook(Hook):
        pass

    class MyComponent(Component):
        @effect(MyHook)
        def my_effect(self) -> None:
            stub()

    component = MyComponent()
    qtbot.add_widget(component)
    qtbot.wait(1)  # Let the effect be called after constructor.
    assert stub.call_count == 1

    MyHook.get().on_change.emit()
    assert stub.call_count == 2
