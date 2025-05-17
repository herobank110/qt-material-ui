"""Sample usage of Text Field components."""

from qtpy.QtCore import QMargins
from qtpy.QtWidgets import QApplication
from material_ui.text_fields import FilledTextField, OutlinedTextField
from material_ui import Component
from material_ui.tokens import md_sys_color
from material_ui.layout_basics import Row


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
        filled.value = "Value"
        filled.changed.connect(filled.value.set)
        row.add_widget(filled)

        outlined = OutlinedTextField()
        outlined.label = "Label"
        outlined.value = "Value"
        outlined.changed.connect(outlined.value.set)
        row.add_widget(outlined)

    def on_text_changed(self, text: str) -> None:
        print(f"Text changed: {text}")


def main():
    app = QApplication()
    window = SampleTextFields()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
