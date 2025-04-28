"""Quick overview of some of the available components."""

from qtpy import QtCore, QtWidgets
from material_ui.layout_basics import Stack
from material_ui.switch import Switch


def main() -> None:
    """Main function."""
    app = QtWidgets.QApplication()

    window = Stack()
    window.alignment.set(QtCore.Qt.AlignCenter)
    window.gap.set(30)
    window.sx.set({"background-color": "white"})
    window.resize(300, 200)

    switch = Switch()
    switch.selected.set(True)
    window.add_widget(switch)

    switch2 = Switch()
    switch2.selected.bind(switch.selected)
    # TODO: avoid 2 way binding, make array of switches!
    switch2.change_requested.connect(switch.selected.set)
    window.add_widget(switch2)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
