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
        # self.resize(700, 400)

        # TODO: should it be md_sys_color.background?
        self.sx = {"background-color": md_sys_color.surface}

        main_row = Row()
        main_row.gap = 20

        filters_box = Stack()
        filters_box.sx = {"background-color": md_sys_color.surface_container}
        filters_box.alignment = Qt.AlignTop

        filled_row = Row()
        filled_row.gap = 5
        filled_row.alignment = Qt.AlignCenter
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
            icon_grid_layout.addWidget(icon, i // 3, i % 3)
            self._icons.append(icon)
        main_row.add_widget(icon_grid)

        self.overlay_widget(main_row, QMargins(10, 10, 10, 10))

    @effect(filled)
    def _apply_filled(self) -> None:
        for icon in self._icons:
            icon.icon_style = "outlined" if self.filled.get() else "rounded"


def main() -> None:
    """Main function."""
    app = QApplication()

    # window = Stack()
    # window.alignment = Qt.AlignCenter
    # window.gap = 30
    # window.sx = {"background-color": md_sys_color.surface}
    # window.resize(700, 200)

    # for icon_style in ["outlined", "rounded", "sharp"]:
    #     row = Row()
    #     row.gap = 20
    #     window.add_widget(row)
    #     for icon_name in ICONS:
    #         icon = Icon()
    #         icon.icon_name = icon_name
    #         icon.icon_style = icon_style
    #         row.add_widget(icon)

    window = IconsSample()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
