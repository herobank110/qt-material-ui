"""Sample of the dynamic color palette system."""

from dataclasses import dataclass, replace

from material_ui._component import Component, Signal, effect, use_state
from material_ui.layout_basics import Row, Stack
from material_ui.shape import Shape
from material_ui.switch import Switch
from material_ui.text_fields.filled_text_field import FilledTextField
from material_ui.theming.dynamic_color import apply_dynamic_color_scheme
from material_ui.tokens import md_sys_color
from material_ui.typography import Typography
from materialyoucolor.hct import Hct
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
from qtpy.QtCore import QMargins, Qt
from qtpy.QtWidgets import QApplication, QGridLayout


class ColorGrid(Component):
    def __init__(self) -> None:
        super().__init__()

        self.sx = {"background-color": md_sys_color.background}

        grid = QGridLayout()
        grid.setContentsMargins(QMargins(40, 40, 40, 40))
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        grid.setSpacing(0)

        # TODO: cleanup repetitive quick code

        primary_cell = Shape()
        primary_cell.setFixedSize(180, 100)
        primary_cell.color = md_sys_color.primary
        primary_label = Typography()
        primary_label.variant = "label-large"
        primary_label.color = md_sys_color.on_primary
        primary_label.text = "Primary"
        primary_label.setParent(primary_cell)
        primary_label.move(10, 10)
        grid.addWidget(primary_cell, 0, 0)

        on_primary_cell = Shape()
        on_primary_cell.setFixedSize(180, 50)
        on_primary_cell.color = md_sys_color.on_primary
        on_primary_label = Typography()
        on_primary_label.variant = "label-large"
        on_primary_label.color = md_sys_color.primary
        on_primary_label.text = "On Primary"
        on_primary_label.setParent(on_primary_cell)
        on_primary_label.move(10, 10)
        grid.addWidget(on_primary_cell, 1, 0)

        secondary_cell = Shape()
        secondary_cell.setFixedSize(180, 100)
        secondary_cell.color = md_sys_color.secondary
        secondary_label = Typography()
        secondary_label.variant = "label-large"
        secondary_label.color = md_sys_color.on_secondary
        secondary_label.text = "Secondary"
        secondary_label.setParent(secondary_cell)
        secondary_label.move(10, 10)
        grid.addWidget(secondary_cell, 0, 1)

        on_secondary_cell = Shape()
        on_secondary_cell.setFixedSize(180, 50)
        on_secondary_cell.color = md_sys_color.on_secondary
        on_secondary_label = Typography()
        on_secondary_label.variant = "label-large"
        on_secondary_label.color = md_sys_color.secondary
        on_secondary_label.text = "On Secondary"
        on_secondary_label.setParent(on_secondary_cell)
        on_secondary_label.move(10, 10)
        grid.addWidget(on_secondary_cell, 1, 1)

        tertiary_cell = Shape()
        tertiary_cell.setFixedSize(180, 100)
        tertiary_cell.color = md_sys_color.tertiary
        tertiary_label = Typography()
        tertiary_label.variant = "label-large"
        tertiary_label.color = md_sys_color.on_tertiary
        tertiary_label.text = "Tertiary"
        tertiary_label.setParent(tertiary_cell)
        tertiary_label.move(10, 10)
        grid.addWidget(tertiary_cell, 0, 2)

        on_tertiary_cell = Shape()
        on_tertiary_cell.setFixedSize(180, 50)
        on_tertiary_cell.color = md_sys_color.on_tertiary
        on_tertiary_label = Typography()
        on_tertiary_label.variant = "label-large"
        on_tertiary_label.color = md_sys_color.tertiary
        on_tertiary_label.text = "On Tertiary"
        on_tertiary_label.setParent(on_tertiary_cell)
        on_tertiary_label.move(10, 10)
        grid.addWidget(on_tertiary_cell, 1, 2)

        primary_container_cell = Shape()
        primary_container_cell.setFixedSize(180, 100)
        primary_container_cell.color = md_sys_color.primary_container
        primary_container_label = Typography()
        primary_container_label.variant = "label-large"
        primary_container_label.color = md_sys_color.on_primary_container
        primary_container_label.text = "Primary Container"
        primary_container_label.setParent(primary_container_cell)
        primary_container_label.move(10, 10)
        grid.addWidget(primary_container_cell, 2, 0)

        on_primary_container_cell = Shape()
        on_primary_container_cell.setFixedSize(180, 50)
        on_primary_container_cell.color = md_sys_color.on_primary_container
        on_primary_container_label = Typography()
        on_primary_container_label.variant = "label-large"
        on_primary_container_label.color = md_sys_color.primary_container
        on_primary_container_label.text = "On Primary Container"
        on_primary_container_label.setParent(on_primary_container_cell)
        on_primary_container_label.move(10, 10)
        grid.addWidget(on_primary_container_cell, 3, 0)

        secondary_container_cell = Shape()
        secondary_container_cell.setFixedSize(180, 100)
        secondary_container_cell.color = md_sys_color.secondary_container
        secondary_container_label = Typography()
        secondary_container_label.variant = "label-large"
        secondary_container_label.color = md_sys_color.on_secondary_container
        secondary_container_label.text = "Secondary Container"
        secondary_container_label.setParent(secondary_container_cell)
        secondary_container_label.move(10, 10)
        grid.addWidget(secondary_container_cell, 2, 1)

        on_secondary_container_cell = Shape()
        on_secondary_container_cell.setFixedSize(180, 50)
        on_secondary_container_cell.color = md_sys_color.on_secondary_container
        on_secondary_container_label = Typography()
        on_secondary_container_label.variant = "label-large"
        on_secondary_container_label.color = md_sys_color.secondary_container
        on_secondary_container_label.text = "On Secondary Container"
        on_secondary_container_label.setParent(on_secondary_container_cell)
        on_secondary_container_label.move(10, 10)
        grid.addWidget(on_secondary_container_cell, 3, 1)

        tertiary_container_cell = Shape()
        tertiary_container_cell.setFixedSize(180, 100)
        tertiary_container_cell.color = md_sys_color.tertiary_container
        tertiary_container_label = Typography()
        tertiary_container_label.variant = "label-large"
        tertiary_container_label.color = md_sys_color.on_tertiary_container
        tertiary_container_label.text = "Tertiary Container"
        tertiary_container_label.setParent(tertiary_container_cell)
        tertiary_container_label.move(10, 10)
        grid.addWidget(tertiary_container_cell, 2, 2)

        on_tertiary_container_cell = Shape()
        on_tertiary_container_cell.setFixedSize(180, 50)
        on_tertiary_container_cell.color = md_sys_color.on_tertiary_container
        on_tertiary_container_label = Typography()
        on_tertiary_container_label.variant = "label-large"
        on_tertiary_container_label.color = md_sys_color.tertiary_container
        on_tertiary_container_label.text = "On Tertiary Container"
        on_tertiary_container_label.setParent(on_tertiary_container_cell)
        on_tertiary_container_label.move(10, 10)
        grid.addWidget(on_tertiary_container_cell, 3, 2)

        self.setLayout(grid)


@dataclass
class Settings:
    color_hex: str = "#4181EE"
    is_dark: bool = False


class SettingsSideBar(Component):
    settings = use_state(Settings())
    on_change_settings: Signal[Settings]

    def __init__(self) -> None:
        super().__init__()

        self.sx = {"background-color": md_sys_color.surface}

        stack = Stack()
        stack.alignment = Qt.AlignmentFlag.AlignTop
        stack.gap = 15
        stack.margins = QMargins(20, 20, 20, 20)

        title = Typography()
        title.variant = "headline-medium"
        title.text = "Color Palette"
        title.color = md_sys_color.on_surface
        stack.add_widget(title)

        self._color_hex_textfield = FilledTextField()
        self._color_hex_textfield.label = "Color (Hex)"
        self._color_hex_textfield.on_change.connect(self._on_change_color_hex)
        stack.add_widget(self._color_hex_textfield)

        dark_mode_row = Row()
        dark_mode_row.gap = 5
        dark_mode_label = Typography()
        dark_mode_label.variant = "body-large"
        dark_mode_label.text = "Dark Mode"
        dark_mode_label.color = md_sys_color.on_surface
        dark_mode_label.alignment = Qt.AlignmentFlag.AlignVCenter
        dark_mode_row.add_widget(dark_mode_label)
        self._dark_mode_switch = Switch()
        self._dark_mode_switch.on_change.connect(self._on_change_dark_mode)
        dark_mode_row.add_widget(self._dark_mode_switch)
        stack.add_widget(dark_mode_row)

        self.overlay_widget(stack)

    @effect(settings)
    def _apply_state(self) -> None:
        self._dark_mode_switch.selected = self.settings.is_dark
        self._color_hex_textfield.value = self.settings.color_hex

    def _on_change_dark_mode(self, selected: bool) -> None:  # noqa: FBT001
        new_state = replace(self.settings, is_dark=selected)
        self.on_change_settings.emit(new_state)

    def _on_change_color_hex(self, value: str) -> None:
        new_state = replace(self.settings, color_hex=value)
        self.on_change_settings.emit(new_state)


class DemoColorPalette(Component):
    settings = use_state(Settings())

    def __init__(self) -> None:
        super().__init__()

        # Clear the focus when clicking outside any input widget.
        self.clicked.connect(lambda: self.setFocus())

        row = Row()

        color_grid = ColorGrid()
        row.add_widget(color_grid)

        side_bar = SettingsSideBar()
        side_bar.settings = self.settings
        side_bar.on_change_settings.connect(self.set_state("settings"))
        row.add_widget(side_bar)

        self.overlay_widget(row)

    @effect(settings)
    def _apply_dynamic_color_scheme(self) -> None:
        color_hex = self.settings.color_hex
        is_dark = self.settings.is_dark
        scheme = SchemeTonalSpot(
            Hct.from_int(int(color_hex.replace("#", "0xFF"), 16)),
            is_dark=is_dark,
            contrast_level=0.0,
        )
        apply_dynamic_color_scheme(scheme)


def main() -> None:
    app = QApplication()
    window = DemoColorPalette()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
