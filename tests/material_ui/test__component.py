import pytest
from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot

from material_ui._component import (
    Component,
    EffectDependencyError,
    Signal,
    effect,
    use_state,
)
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


def test_Component_state_kw_args_init_custom_state(qtbot: QtBot):
    class C(Component):
        a: str = use_state("")

    c1 = C(a="hi")
    assert c1.a == "hi"
    qtbot.add_widget(c1)


def test_Component_state_kw_args_init_parent(qtbot: QtBot):
    c1 = Component(a="hi")
    qtbot.add_widget(c1)
    c2 = Component(parent=c1)
    assert c2.parentWidget() is c1


def test_Component_state_kw_args_init_with_effect_dependency_custom_create(
    qtbot: QtBot,
    mocker: MockerFixture,
):
    stub = mocker.stub()

    class C(Component):
        a: str = use_state("")

        def _create(self) -> None:
            self.x = 1

        @effect(a)
        def a_effect(self) -> None:
            assert self.x == 1
            stub()

    c1 = C(a="hi")
    assert stub.called
    assert c1.a == "hi"
    qtbot.add_widget(c1)


def test_Component_state_kw_args_init_assign_to_signal_conversion(
    qtbot: QtBot,
    mocker: MockerFixture,
):
    stub = mocker.stub()

    class C(Component):
        a: Signal[int]

    c1 = C(a=stub)
    c1.a.emit(11)
    stub.assert_called_with(11)
    qtbot.add_widget(c1)


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


def test_Component_effect_children_dependency(qtbot: QtBot, mocker: MockerFixture):
    stub = mocker.stub()

    class TestComponent(Component):
        @effect(Component.children)
        def my_effect(self) -> None:
            stub()

    parent = TestComponent()
    child = Component()
    qtbot.add_widget(parent)
    qtbot.wait(1)  # Let the effect be called after constructor.
    assert stub.call_count == 1

    child.setParent(parent)

    assert stub.call_count == 2
