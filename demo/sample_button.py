"""Sample of using the buttons."""

from qtpy import QtCore, QtWidgets
from material_ui.button import ElevatedButton
from material_ui.layout_basics import Stack


def main() -> None:
    """Main function."""
    app = QtWidgets.QApplication()

    window = Stack()
    window.alignment = QtCore.Qt.AlignCenter
    window.gap = 30
    window.sx = {"background-color": "white"}
    window.resize(300, 300)

    for variant in [
        "elevated",
        # "filled",
        # "filled-tonal",
        # "outlined",
        # "text",
    ]:
        btn = ElevatedButton()
        btn.text.set(variant.title())
        btn.variant.set(variant)
        window.add_widget(btn)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()

