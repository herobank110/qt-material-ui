"""Sample of using the ComboBox."""

from material_ui._component import Component
from material_ui.combobox import ComboBox
from material_ui.tokens import md_sys_color
from qtpy.QtCore import QMargins
from qtpy.QtWidgets import QApplication


class SampleComboBox(Component):
    def __init__(self) -> None:
        super().__init__()
        self.sx = {"background-color": md_sys_color.background}

        cb = ComboBox()
        cb.items = ["Option 1", "Option 2", "Option 3"]
        cb.label = "Label"

        self.overlay_widget(cb, QMargins(40, 40, 40, 40))


def main() -> None:
    app = QApplication([])
    window = SampleComboBox()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
