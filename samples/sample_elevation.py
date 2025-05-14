"""Sample of using the elevation."""

from qtpy import QtCore, QtWidgets
from material_ui.elevation import Elevation
from material_ui.layout_basics import Row
from material_ui.tokens import md_sys_elevation
from material_ui.typography import Typography


def main() -> None:
    """Main function."""
    app = QtWidgets.QApplication()

    window = Row()
    window.alignment.set(QtCore.Qt.AlignCenter)
    window.gap.set(20)
    window.sx.set({"background-color": "white"})
    window.resize(400, 200)

    levels = [
        md_sys_elevation.level0,
        md_sys_elevation.level1,
        md_sys_elevation.level2,
        md_sys_elevation.level3,
        md_sys_elevation.level4,
    ]
    for i, level in enumerate(levels):
        comp = Elevation()
        comp.setFixedSize(50, 50)
        comp.elevation.set(level)

        label = Typography()
        label.text.set(str(i))
        label.setParent(comp)
        label.move(5, 5)

        window.add_widget(comp)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
