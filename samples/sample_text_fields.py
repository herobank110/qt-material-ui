"""Sample usage of Text Field components."""

from qtpy.QtCore import QMargins
from qtpy.QtWidgets import QApplication
from material_ui.text_fields._base_text_field import BaseTextField
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

        text_field = BaseTextField()
        text_field.label = "Label"
        text_field.value = "Value"
        # internally controlled value
        text_field.changed.connect(text_field.value.set)
        row.add_widget(text_field)

    def on_text_changed(self, text: str) -> None:
        print(f"Text changed: {text}")


def main():
    app = QApplication()
    window = SampleTextFields()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
