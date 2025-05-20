from pytestqt.qtbot import QtBot
from qtpy.QtCore import QEasingCurve
from qtpy.QtWidgets import QWidget

from material_ui._component import State, _TransitionConfig


def test_State_transition_applies_over_time(qtbot: QtBot):
    duration_ms = 50
    start_value = 10.0
    end_value = 20.0

    state = State(start_value, "")
    state.set_transition(_TransitionConfig(duration_ms, QEasingCurve.Type.Linear))
    state.set_value(end_value)

    periodically_inspected_values: list[float] = []
    for _ in range(duration_ms // 5 + 1):
        periodically_inspected_values.append(state.get_value())
        qtbot.wait(duration_ms // 5)

    assert state.get_value() == end_value
    assert periodically_inspected_values == sorted(periodically_inspected_values)
    assert min(periodically_inspected_values) >= start_value
    assert max(periodically_inspected_values) <= end_value


def test_State_transition_instant_changes_take_last_value(
    qtbot: QtBot,
):
    state = State(10.0, "")
    state.set_transition(_TransitionConfig(50, QEasingCurve.Type.Linear))
    state.set_value(20.0)
    state.set_value(10.0)
    qtbot.wait(60)
    assert state.get_value() == 10.0


def test_State_animate_to_instant_changes_take_last_value(
    qtbot: QtBot,
):
    state = State(10.0, "")
    state.animate_to(20.0, 50, QEasingCurve.Type.Linear)
    state.animate_to(10.0, 50, QEasingCurve.Type.Linear)
    qtbot.wait(60)
    assert state.get_value() == 10.0


def test_State___repr___current_value_and_parent_type(qtbot: QtBot):
    widget = QWidget()
    qtbot.add_widget(widget)
    state = State(1, "state")
    state.setParent(widget)
    assert repr(state) == "<State 'state' of component 'QWidget' (current value: 1)>"


def test_State___repr___null_parent():
    state = State(1, "state")
    assert repr(state) == "<State 'state' of component 'no-parent' (current value: 1)>"


def test_State_bound_cant_be_set():
    state1 = State(1, "")
    state2 = State(2, "")
    assert state2.get_value() == 2
    state2.bind(state1)
    assert state2.get_value() == 1
    state2.set_value(3)
    assert state2.get_value() == 1

    state1.set_value(4)
    assert state2.get_value() == 4
