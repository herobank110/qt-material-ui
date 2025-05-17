"""Sample of using the icons."""

from qtpy.QtWidgets import QApplication
from qtpy.QtCore import Qt
from material_ui.icon import Icon
from material_ui.layout_basics import Row


def main() -> None:
    """Main function."""
    app = QApplication()

    window = Row()
    window.alignment = Qt.AlignCenter
    window.gap = 30
    window.sx = {"background-color": "white"}
    window.resize(700, 200)

    for i, icon_name in enumerate(
        [
            "star",
            "arrow_drop_down",
            "more_vert",
            "check",
            "close",
            "add",
        ]
    ):
        icon = Icon()
        icon.icon_name = icon_name
        window.add_widget(icon)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
