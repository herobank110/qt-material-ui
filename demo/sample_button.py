"""Sample of using the buttons."""

from qtpy import QtCore, QtWidgets
from material_ui.button import ElevatedButton
from material_ui.layout_basics import Stack


def main() -> None:
    """Main function."""
    app = QtWidgets.QApplication()

    window = Stack()
    window.alignment.set(QtCore.Qt.AlignCenter)
    window.gap.set(30)
    window.sx.set({"background-color": "white"})
    window.resize(300, 300)

    for variant in [
        "elevated",
        # "filled",
        # "filled-tonal",
        # "outlined",
        # "text",
    ]:
        btn = ElevatedButton()
        btn.text.set("Click me")
        btn.variant.set(variant)
        window.add_widget(btn)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()

