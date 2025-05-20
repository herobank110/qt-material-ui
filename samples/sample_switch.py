"""Sample of using the switch."""

from material_ui._component import Component, use_state
from material_ui.layout_basics import Stack
from material_ui.switch import Switch
from qtpy import QtWidgets
from qtpy.QtCore import Qt


class SampleSwitch(Component):
    """Window with two switches with linked state."""

    selected = use_state(False)

    def __init__(self) -> None:
        super().__init__()
        self.resize(300, 200)

        stack = Stack()
        stack.alignment = Qt.AlignmentFlag.AlignCenter
        stack.gap = 30
        stack.sx = {"background-color": "white"}
        self.overlay_widget(stack)

        switch = Switch()
        switch.selected = self.selected
        switch.on_change.connect(lambda value: setattr(self, "selected", value))
        stack.add_widget(switch)

        # This switch can't be toggled - value is controlled the other one.
        switch2 = Switch()
        switch2.selected = self.selected
        stack.add_widget(switch2)


def main() -> None:
    """Main function."""
    app = QtWidgets.QApplication()
    window = SampleSwitch()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
