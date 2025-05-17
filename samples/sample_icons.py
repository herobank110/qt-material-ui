"""Sample of using the icons."""

from qtpy.QtWidgets import QApplication
from qtpy.QtCore import Qt
from material_ui.icon import Icon
from material_ui.layout_basics import Stack, Row
from material_ui.tokens import md_sys_color


def main() -> None:
    """Main function."""
    app = QApplication()

    window = Stack()
    window.alignment = Qt.AlignCenter
    window.gap = 30
    window.sx = {"background-color": md_sys_color.surface}
    window.resize(700, 200)

    icons = ["star", "arrow_drop_down", "more_vert", "check", "close", "add"]

    for icon_style in ["outlined", "rounded", "sharp"]:
        row = Row()
        row.gap = 20
        window.add_widget(row)
        for icon_name in icons:
            icon = Icon()
            icon.icon_name = icon_name
            icon.icon_style = icon_style
            row.add_widget(icon)

    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
