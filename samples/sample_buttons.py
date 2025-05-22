"""Sample of using the buttons."""

from functools import partial

from material_ui._component import Component
from material_ui.buttons import (
    ElevatedButton,
    FilledButton,
    FilledTonalButton,
    OutlinedButton,
    TextButton,
)
from material_ui.layout_basics import Row
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication


class SampleButtons(Component):
    def __init__(self) -> None:
        super().__init__()
        self.resize(700, 200)

        row = Row()
        row.alignment = Qt.AlignmentFlag.AlignCenter
        row.gap = 30
        row.sx = {"background-color": "white"}
        self.overlay_widget(row)

        for variant, klass in {
            "Elevated": ElevatedButton,
            "Filled": FilledButton,
            "Tonal": FilledTonalButton,
            "Outlined": OutlinedButton,
            "Text": TextButton,
        }.items():
            button = klass()
            button.text = variant
            button.clicked.connect(partial(self._on_click_button, variant))
            row.add_widget(button)

    def _on_click_button(self, variant: str) -> None:
        print(f"Clicked: {variant}")


def main() -> None:
    app = QApplication()
    window = SampleButtons()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
