from pytestqt.qtbot import QtBot
from qtpy.QtCore import QEasingCurve

from material_ui._component import State, _TransitionConfig


def test_State_transition_applies_over_time(qtbot: QtBot):
    duration_ms = 50
    start_value = 10.0
    end_value = 20.0

    state = State(start_value, "state")
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
