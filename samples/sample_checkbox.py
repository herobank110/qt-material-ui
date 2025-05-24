"""Sample of using the checkbox."""

from material_ui._component import Component
from material_ui.checkbox import Checkbox
from material_ui.layout_basics import Row
from material_ui.tokens import md_sys_color
from qtpy.QtCore import QMargins
from qtpy.QtWidgets import QApplication


class SampleCheckbox(Component):
    def __init__(self) -> None:
        super().__init__()

        self.sx = {"background-color": md_sys_color.background}

        row = Row()
        row.gap = 30
        row.margins = QMargins(40, 30, 40, 30)

        checkbox1 = Checkbox()
        row.add_widget(checkbox1)

        checkbox2 = Checkbox()
        checkbox2.selected = True
        row.add_widget(checkbox2)

        checkbox3 = Checkbox()
        checkbox3.indeterminate = True
        row.add_widget(checkbox3)

        self.overlay_widget(row)


def main() -> None:
    app = QApplication()
    window = SampleCheckbox()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
