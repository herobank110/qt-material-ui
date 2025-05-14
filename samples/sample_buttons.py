"""Sample of using the buttons."""

from qtpy import QtCore, QtWidgets
from material_ui.buttons import (
    ElevatedButton,
    FilledButton,
    FilledTonalButton,
    OutlinedButton,
    TextButton,
)
from material_ui.layout_basics import Row


def main() -> None:
    """Main function."""
    app = QtWidgets.QApplication()

    window = Row()
    window.alignment = QtCore.Qt.AlignCenter
    window.gap = 30
    window.sx = {"background-color": "white"}
    window.resize(700, 200)

    for variant, klass in {
        "Elevated": ElevatedButton,
        "Filled": FilledButton,
        "Tonal": FilledTonalButton,
        "Outlined": OutlinedButton,
        "Text": TextButton,
    }.items():
        button = klass()
        button.text = variant
        button.clicked.connect(lambda variant=variant: print(f"Clicked: {variant}"))
        window.add_widget(button)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
