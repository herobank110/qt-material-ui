from pytestqt.qtbot import QtBot
from qtpy.QtCore import QEasingCurve

from material_ui._component import State, _TransitionConfig


def test_State_transition_applies_over_time(qtbot: QtBot):
    my_state = State(10.0, "my_state")
    my_state.set_transition(_TransitionConfig(50, QEasingCurve.Type.Linear))
    my_state.set_value(20.0)

    periodically_inspected_values: list[float] = []
    for _ in range(50 // 10 + 2):
        periodically_inspected_values.append(my_state.get_value())
        qtbot.wait(10)

    assert my_state.get_value() == 20.0
    assert periodically_inspected_values == sorted(periodically_inspected_values)
    assert min(periodically_inspected_values) >= 10.0
    assert max(periodically_inspected_values) <= 20.0
