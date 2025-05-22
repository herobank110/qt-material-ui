"""Sample of fixed and indeterminate, circular and linear progress indicators."""

from material_ui._component import Component
from material_ui.layout_basics import Row, Stack
from material_ui.progress_indicators.circular_progress import CircularProgress
from material_ui.progress_indicators.linear_progress import LinearProgress
from material_ui.tokens import md_sys_color
from qtpy.QtCore import QMargins
from qtpy.QtWidgets import QApplication


class ProgressIndicatorsSample(Component):
    def __init__(self) -> None:
        super().__init__()

        self.sx = {"background-color": md_sys_color.background}

        row = Row()
        row.gap = 20

        circular = CircularProgress()
        circular.value = 0.75
        row.add_widget(circular)

        circular_indeterminate = CircularProgress()
        circular_indeterminate.indeterminate = True
        row.add_widget(circular_indeterminate)

        stack = Stack()
        stack.setFixedWidth(100)

        linear = LinearProgress()
        linear.value = 0.75
        stack.add_widget(linear)

        linear_indeterminate = LinearProgress()
        linear_indeterminate.indeterminate = True
        stack.add_widget(linear_indeterminate)

        row.add_widget(stack)

        self.overlay_widget(row, margins=QMargins(40, 30, 40, 30))


def main() -> None:
    app = QApplication()
    window = ProgressIndicatorsSample()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
