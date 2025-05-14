"""Sample of using the buttons."""

from qtpy import QtCore, QtWidgets
from material_ui.buttons import ElevatedButton, FilledButton
from material_ui.layout_basics import Stack


def main() -> None:
    """Main function."""
    app = QtWidgets.QApplication()

    window = Stack()
    window.alignment = QtCore.Qt.AlignCenter
    window.gap = 30
    window.sx = {"background-color": "white"}
    window.resize(300, 300)

    for variant, klass in {
        "Elevated": ElevatedButton,
        "Filled": FilledButton,
        # "filled-tonal",
        # "outlined",
        # "text",
    }.items():
        button = klass()
        button.text = variant
        button.clicked.connect(lambda: print(f"Clicked: {variant}"))
        window.add_widget(button)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
