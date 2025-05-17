"""Sample of using the icons."""

from qtpy.QtWidgets import QApplication, QGridLayout
from qtpy.QtCore import Qt, QMargins
from material_ui._component import effect, use_state
from material_ui.icon import Icon
from material_ui.layout_basics import Stack, Row
from material_ui.switch import Switch
from material_ui.tokens import md_sys_color
from material_ui import Component
from material_ui.typography import Typography

ICONS = ["star", "arrow_drop_down", "more_vert", "check", "close", "add"]


class IconsSample(Component):
    filled = use_state(False)
    icon_style = use_state("outlined")

    def __init__(self):
        super().__init__()

        # TODO: should it be md_sys_color.background?
        self.sx = {"background-color": md_sys_color.surface}

        main_row = Row()
        main_row.gap = 20

        filters_box = Stack()
        filters_box.margins = QMargins(10, 10, 10, 10)
        filters_box.sx = {"background-color": md_sys_color.surface_container}
        filters_box.alignment = Qt.AlignTop | Qt.AlignRight

        filled_row = Row()
        filled_row.gap = 5
        filled_row.alignment = Qt.AlignRight
        filled_label = Typography()
        filled_label.alignment = Qt.AlignCenter
        filled_label.text = "Filled"
        filled_row.add_widget(filled_label)
        filled_switch = Switch()
        filled_switch.selected.bind(self.filled)
        filled_switch.change_requested.connect(self.filled.set)
        filled_row.add_widget(filled_switch)
        filters_box.add_widget(filled_row)

        main_row.add_widget(filters_box)

        # TODO: make a grid widget / flex box
        icon_grid = Component()
        icon_grid_layout = QGridLayout(icon_grid)
        self._icons: list[Icon] = []
        for i, icon_name in enumerate(ICONS):
            icon = Icon()
            icon.icon_name = icon_name
            icon.filled.bind(self.filled)
            icon_grid_layout.addWidget(icon, i // 3, i % 3)
            self._icons.append(icon)
        main_row.add_widget(icon_grid)

        self.overlay_widget(main_row, QMargins(10, 10, 10, 10))


def main() -> None:
    """Main function."""
    app = QApplication()
    window = IconsSample()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
