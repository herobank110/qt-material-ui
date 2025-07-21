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

        row = Row(gap=30, margins=QMargins(40, 30, 40, 30))
        row.add_widget(Checkbox())
        row.add_widget(Checkbox(selected=True))
        row.add_widget(Checkbox(indeterminate=True))
        self.overlay_widget(row)


def main() -> None:
    app = QApplication()
    window = SampleCheckbox()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
