"""Sample usage of Text Field components."""

from material_ui import Component
from material_ui.layout_basics import Row
from material_ui.text_fields import FilledTextField, OutlinedTextField
from material_ui.tokens import md_sys_color
from qtpy.QtCore import QMargins
from qtpy.QtWidgets import QApplication


class SampleTextFields(Component):
    """Sample usage of Text Field components."""

    def __init__(self) -> None:
        super().__init__()

        self.sx = {"background-color": md_sys_color.surface}

        row = Row()
        row.gap = 30
        row.margins = QMargins(20, 20, 20, 20)
        self.overlay_widget(row)

        filled = FilledTextField()
        filled.label = "Label"
        # filled.value = "Value"
        row.add_widget(filled)

        outlined = OutlinedTextField()
        outlined.label = "Label"
        outlined.value = "Value"
        row.add_widget(outlined)

        # Take the initial focus away from the first text field.
        self.setFocus()
        # Steal focus when the empty area is clicked.
        def f():
            print("clicked window - clearing focus")
            self.setFocus()
        self.clicked.connect(f)

        from qtpy.QtCore import QTimer
        # QTimer.singleShot(100, lambda: filled.setFocus())
        # QTimer.singleShot(0, lambda: filled.setFocus())
        # filled.setFocus()


def main() -> None:
    app = QApplication()
    window = SampleTextFields()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
