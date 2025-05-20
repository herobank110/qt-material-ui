"""Sample of fixed and indeterminate, circular and linear progress indicators."""

from material_ui._component import Component
from material_ui.layout_basics import Row
from material_ui.progress_indicators.circular_progress import CircularProgress
from material_ui.tokens import md_sys_color
from qtpy.QtCore import QMargins
from qtpy.QtWidgets import QApplication


class ProgressIndicatorsSample(Component):
    def __init__(self) -> None:
        super().__init__()

        self.sx = {"background-color": md_sys_color.surface}

        row = Row()

        circular = CircularProgress()
        circular.value = 0.75
        row.add_widget(circular)

        circular_indeterminate = CircularProgress()
        circular_indeterminate.indeterminate = True
        row.add_widget(circular_indeterminate)

        self.overlay_widget(row, margins=QMargins(20, 20, 20, 20))


def main() -> None:
    app = QApplication()
    window = ProgressIndicatorsSample()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
