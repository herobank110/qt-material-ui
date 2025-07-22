"""Sample of using the icons."""

from material_ui import Component
from material_ui._component import use_state
from material_ui.icon import Icon
from material_ui.layout_basics import Row, Stack
from material_ui.switch import Switch
from material_ui.tokens import md_sys_color
from material_ui.typography import Typography
from qtpy.QtCore import QMargins, Qt
from qtpy.QtWidgets import QApplication, QGridLayout

ICONS = ["star", "arrow_drop_down", "more_vert", "check", "close", "add"]


class IconsSample(Component):
    filled = use_state(False)
    icon_style = use_state("outlined")

    def _create(self) -> None:
        self.sx = {"background-color": md_sys_color.background}

        main_row = Row()

        # TODO: make a grid widget / flex box
        icon_grid = Component()
        icon_grid_layout = QGridLayout(icon_grid)
        self._icons: list[Icon] = []
        for i, icon_name in enumerate(ICONS):
            icon = Icon(icon_name=icon_name)
            icon.filled = self.filled  # bind
            icon_grid_layout.addWidget(icon, i // 3, i % 3)
            self._icons.append(icon)

        main_row.add_widget(icon_grid)

        filters_box = Stack(
            margins=QMargins(10, 10, 10, 10),
            sx={"background-color": md_sys_color.surface_container},
        )

        filled_row = Row(gap=5)
        filled_switch = Switch(on_change=self.set_state("filled"))
        filled_switch.selected = self.filled  # bind
        filled_row.add_widget(filled_switch)
        filled_row.add_widget(
            Typography(
                variant="body-large",
                alignment=Qt.AlignmentFlag.AlignVCenter,
                text="Filled",
            ),
        )
        filters_box.add_widget(filled_row)

        main_row.add_widget(filters_box)

        self.overlay_widget(main_row)


def main() -> None:
    """Main function."""
    app = QApplication()
    window = IconsSample()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
