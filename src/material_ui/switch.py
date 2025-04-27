from qtpy import QtWidgets
from material_ui._component import Component, Signal


class Switch(Component):
    """Switches toggle the selection of an item on or off."""

    change_requested: Signal[bool]
    """Signal emitted when the switch is toggled."""

    def __init__(self, *, defaultChecked: bool = False) -> None:
        super().__init__()
        # self.checked = defaultChecked

        self.setFixedSize(52, 32)

        self.setStyleSheet("background-color:red;border-radius:16px;")
