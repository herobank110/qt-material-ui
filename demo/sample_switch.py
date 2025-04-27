"""Quick overview of some of the available components."""

from qtpy import QtWidgets
from material_ui.layout_basics import Stack
from material_ui.switch import Switch


def main() -> None:
    """Main function."""
    app = QtWidgets.QApplication()

    window = Stack()
    window.resize(300, 200)

    switch = Switch(defaultChecked=True)
    window.add_widget(switch)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
