"""Sample of using the elevation."""

from qtpy import QtCore, QtWidgets
from material_ui.elevation import Elevation
from material_ui.layout_basics import Stack
from material_ui.tokens import md_sys_elevation


def main() -> None:
    """Main function."""
    app = QtWidgets.QApplication()

    window = Stack()
    window.alignment.set(QtCore.Qt.AlignCenter)
    window.gap.set(20)
    window.sx.set({"background-color": "white"})
    window.resize(300, 300)

    levels = [
        md_sys_elevation.level0,
        md_sys_elevation.level1,
        md_sys_elevation.level2,
        md_sys_elevation.level3,
        md_sys_elevation.level4,
    ]
    for level in levels:
        comp = Elevation()
        comp.setFixedSize(50, 50)
        comp.elevation.set(level)
        window.add_widget(comp)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
