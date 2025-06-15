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

        self.setFixedWidth(1200)

        grid = QGridLayout()
        grid.setContentsMargins(QMargins(40, 40, 40, 40))
        grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        grid.setSpacing(5)

        # TODO: cleanup repetitive quick code

        primary_cell = Shape()
        primary_cell.setFixedHeight(100)
        primary_cell.color = md_sys_color.primary
        primary_label = Typography()
        primary_label.variant = "label-large"
        primary_label.color = md_sys_color.on_primary
        primary_label.text = "Primary"
        primary_label.setParent(primary_cell)
        primary_label.move(10, 10)
        grid.addWidget(primary_cell, 0, 0, 1, 15)

        on_primary_cell = Shape()
        on_primary_cell.setFixedHeight(50)
        on_primary_cell.color = md_sys_color.on_primary
        on_primary_label = Typography()
        on_primary_label.variant = "label-large"
        on_primary_label.color = md_sys_color.primary
        on_primary_label.text = "On Primary"
        on_primary_label.setParent(on_primary_cell)
        on_primary_label.move(10, 10)
        grid.addWidget(on_primary_cell, 1, 0, 1, 15)

        secondary_cell = Shape()
        secondary_cell.setFixedHeight(100)
        secondary_cell.color = md_sys_color.secondary
        secondary_label = Typography()
        secondary_label.variant = "label-large"
        secondary_label.color = md_sys_color.on_secondary
        secondary_label.text = "Secondary"
        secondary_label.setParent(secondary_cell)
        secondary_label.move(10, 10)
        grid.addWidget(secondary_cell, 0, 15, 1, 15)

        on_secondary_cell = Shape()
        on_secondary_cell.setFixedHeight(50)
        on_secondary_cell.color = md_sys_color.on_secondary
        on_secondary_label = Typography()
        on_secondary_label.variant = "label-large"
        on_secondary_label.color = md_sys_color.secondary
        on_secondary_label.text = "On Secondary"
        on_secondary_label.setParent(on_secondary_cell)
        on_secondary_label.move(10, 10)
        grid.addWidget(on_secondary_cell, 1, 15, 1, 15)

        tertiary_cell = Shape()
        tertiary_cell.setFixedHeight(100)
        tertiary_cell.color = md_sys_color.tertiary
        tertiary_label = Typography()
        tertiary_label.variant = "label-large"
        tertiary_label.color = md_sys_color.on_tertiary
        tertiary_label.text = "Tertiary"
        tertiary_label.setParent(tertiary_cell)
        tertiary_label.move(10, 10)
        grid.addWidget(tertiary_cell, 0, 30, 1, 15)

        on_tertiary_cell = Shape()
        on_tertiary_cell.setFixedHeight(50)
        on_tertiary_cell.color = md_sys_color.on_tertiary
        on_tertiary_label = Typography()
        on_tertiary_label.variant = "label-large"
        on_tertiary_label.color = md_sys_color.tertiary
        on_tertiary_label.text = "On Tertiary"
        on_tertiary_label.setParent(on_tertiary_cell)
        on_tertiary_label.move(10, 10)
        grid.addWidget(on_tertiary_cell, 1, 30, 1, 15)

        error_cell = Shape()
        error_cell.setFixedHeight(100)
        error_cell.color = md_sys_color.error
        error_label = Typography()
        error_label.variant = "label-large"
        error_label.color = md_sys_color.on_error
        error_label.text = "Error"
        error_label.setParent(error_cell)
        error_label.move(10, 10)
        grid.addWidget(error_cell, 0, 45, 1, 15)

        on_error_cell = Shape()
        on_error_cell.setFixedHeight(50)
        on_error_cell.color = md_sys_color.on_error
        on_error_label = Typography()
        on_error_label.variant = "label-large"
        on_error_label.color = md_sys_color.error
        on_error_label.text = "On Error"
        on_error_label.setParent(on_error_cell)
        on_error_label.move(10, 10)
        grid.addWidget(on_error_cell, 1, 45, 1, 15)

        primary_container_cell = Shape()
        primary_container_cell.setFixedHeight(100)
        primary_container_cell.color = md_sys_color.primary_container
        primary_container_label = Typography()
        primary_container_label.variant = "label-large"
        primary_container_label.color = md_sys_color.on_primary_container
        primary_container_label.text = "Primary Container"
        primary_container_label.setParent(primary_container_cell)
        primary_container_label.move(10, 10)
        grid.addWidget(primary_container_cell, 2, 0, 1, 15)

        on_primary_container_cell = Shape()
        on_primary_container_cell.setFixedHeight(50)
        on_primary_container_cell.color = md_sys_color.on_primary_container
        on_primary_container_label = Typography()
        on_primary_container_label.variant = "label-large"
        on_primary_container_label.color = md_sys_color.primary_container
        on_primary_container_label.text = "On Primary Container"
        on_primary_container_label.setParent(on_primary_container_cell)
        on_primary_container_label.move(10, 10)
        grid.addWidget(on_primary_container_cell, 3, 0, 1, 15)

        secondary_container_cell = Shape()
        secondary_container_cell.setFixedHeight(100)
        secondary_container_cell.color = md_sys_color.secondary_container
        secondary_container_label = Typography()
        secondary_container_label.variant = "label-large"
        secondary_container_label.color = md_sys_color.on_secondary_container
        secondary_container_label.text = "Secondary Container"
        secondary_container_label.setParent(secondary_container_cell)
        secondary_container_label.move(10, 10)
        grid.addWidget(secondary_container_cell, 2, 15, 1, 15)

        on_secondary_container_cell = Shape()
        on_secondary_container_cell.setFixedHeight(50)
        on_secondary_container_cell.color = md_sys_color.on_secondary_container
        on_secondary_container_label = Typography()
        on_secondary_container_label.variant = "label-large"
        on_secondary_container_label.color = md_sys_color.secondary_container
        on_secondary_container_label.text = "On Secondary Container"
        on_secondary_container_label.setParent(on_secondary_container_cell)
        on_secondary_container_label.move(10, 10)
        grid.addWidget(on_secondary_container_cell, 3, 15, 1, 15)

        tertiary_container_cell = Shape()
        tertiary_container_cell.setFixedHeight(100)
        tertiary_container_cell.color = md_sys_color.tertiary_container
        tertiary_container_label = Typography()
        tertiary_container_label.variant = "label-large"
        tertiary_container_label.color = md_sys_color.on_tertiary_container
        tertiary_container_label.text = "Tertiary Container"
        tertiary_container_label.setParent(tertiary_container_cell)
        tertiary_container_label.move(10, 10)
        grid.addWidget(tertiary_container_cell, 2, 30, 1, 15)

        on_tertiary_container_cell = Shape()
        on_tertiary_container_cell.setFixedHeight(50)
        on_tertiary_container_cell.color = md_sys_color.on_tertiary_container
        on_tertiary_container_label = Typography()
        on_tertiary_container_label.variant = "label-large"
        on_tertiary_container_label.color = md_sys_color.tertiary_container
        on_tertiary_container_label.text = "On Tertiary Container"
        on_tertiary_container_label.setParent(on_tertiary_container_cell)
        on_tertiary_container_label.move(10, 10)
        grid.addWidget(on_tertiary_container_cell, 3, 30, 1, 15)

        error_container_cell = Shape()
        error_container_cell.setFixedHeight(100)
        error_container_cell.color = md_sys_color.error_container
        error_container_label = Typography()
        error_container_label.variant = "label-large"
        error_container_label.color = md_sys_color.on_error_container
        error_container_label.text = "Error Container"
        error_container_label.setParent(error_container_cell)
        error_container_label.move(10, 10)
        grid.addWidget(error_container_cell, 2, 45, 1, 15)

        on_error_container_cell = Shape()
        on_error_container_cell.setFixedHeight(50)
        on_error_container_cell.color = md_sys_color.on_error_container
        on_error_container_label = Typography()
        on_error_container_label.variant = "label-large"
        on_error_container_label.color = md_sys_color.error_container
        on_error_container_label.text = "On Error Container"
        on_error_container_label.setParent(on_error_container_cell)
        on_error_container_label.move(10, 10)
        grid.addWidget(on_error_container_cell, 3, 45, 1, 15)

        surface_dim_cell = Shape()
        surface_dim_cell.setFixedHeight(100)
        surface_dim_cell.color = md_sys_color.surface_dim
        surface_dim_label = Typography()
        surface_dim_label.variant = "label-large"
        surface_dim_label.color = md_sys_color.on_surface
        surface_dim_label.text = "Surface Dim"
        surface_dim_label.setParent(surface_dim_cell)
        surface_dim_label.move(10, 10)
        grid.addWidget(surface_dim_cell, 4, 0, 1, 20)

        surface_cell = Shape()
        surface_cell.setFixedHeight(100)
        surface_cell.color = md_sys_color.surface
        surface_label = Typography()
        surface_label.variant = "label-large"
        surface_label.color = md_sys_color.on_surface
        surface_label.text = "Surface"
        surface_label.setParent(surface_cell)
        surface_label.move(10, 10)
        grid.addWidget(surface_cell, 4, 20, 1, 20)

        surface_bright_cell = Shape()
        surface_bright_cell.setFixedHeight(100)
        surface_bright_cell.color = md_sys_color.surface_bright
        surface_bright_label = Typography()
        surface_bright_label.variant = "label-large"
        surface_bright_label.color = md_sys_color.on_surface
        surface_bright_label.text = "Surface Bright"
        surface_bright_label.setParent(surface_bright_cell)
        surface_bright_label.move(10, 10)
        grid.addWidget(surface_bright_cell, 4, 40, 1, 20)

        surface_container_lowest_cell = Shape()
        surface_container_lowest_cell.setFixedHeight(100)
        surface_container_lowest_cell.color = md_sys_color.surface_container_lowest
        surface_container_lowest_label = Typography()
        surface_container_lowest_label.variant = "label-large"
        surface_container_lowest_label.color = md_sys_color.on_surface
        surface_container_lowest_label.text = "Surface Container Lowest"
        surface_container_lowest_label.setParent(surface_container_lowest_cell)
        surface_container_lowest_label.move(10, 10)
        grid.addWidget(surface_container_lowest_cell, 5, 0, 1, 12)

        surface_container_low_cell = Shape()
        surface_container_low_cell.setFixedHeight(100)
        surface_container_low_cell.color = md_sys_color.surface_container_low
        surface_container_low_label = Typography()
        surface_container_low_label.variant = "label-large"
        surface_container_low_label.color = md_sys_color.on_surface
        surface_container_low_label.text = "Surface Container Low"
        surface_container_low_label.setParent(surface_container_low_cell)
        surface_container_low_label.move(10, 10)
        grid.addWidget(surface_container_low_cell, 5, 12, 1, 12)

        surface_container_cell = Shape()
        surface_container_cell.setFixedHeight(100)
        surface_container_cell.color = md_sys_color.surface_container
        surface_container_label = Typography()
        surface_container_label.variant = "label-large"
        surface_container_label.color = md_sys_color.on_surface
        surface_container_label.text = "Surface Container"
        surface_container_label.setParent(surface_container_cell)
        surface_container_label.move(10, 10)
        grid.addWidget(surface_container_cell, 5, 24, 1, 12)

        surface_container_high_cell = Shape()
        surface_container_high_cell.setFixedHeight(100)
        surface_container_high_cell.color = md_sys_color.surface_container_high
        surface_container_high_label = Typography()
        surface_container_high_label.variant = "label-large"
        surface_container_high_label.color = md_sys_color.on_surface
        surface_container_high_label.text = "Surface Container High"
        surface_container_high_label.setParent(surface_container_high_cell)
        surface_container_high_label.move(10, 10)
        grid.addWidget(surface_container_high_cell, 5, 36, 1, 12)

        surface_container_highest_cell = Shape()
        surface_container_highest_cell.setFixedHeight(100)
        surface_container_highest_cell.color = md_sys_color.surface_container_highest
        surface_container_highest_label = Typography()
        surface_container_highest_label.variant = "label-large"
        surface_container_highest_label.color = md_sys_color.on_surface
        surface_container_highest_label.text = "Surface Container Highest"
        surface_container_highest_label.setParent(surface_container_highest_cell)
        surface_container_highest_label.move(10, 10)
        grid.addWidget(surface_container_highest_cell, 5, 48, 1, 12)

        on_surface_cell = Shape()
        on_surface_cell.setFixedHeight(60)
        on_surface_cell.color = md_sys_color.on_surface
        on_surface_label = Typography()
        on_surface_label.variant = "label-large"
        on_surface_label.color = md_sys_color.surface
        on_surface_label.text = "On Surface"
        on_surface_label.setParent(on_surface_cell)
        on_surface_label.move(10, 10)
        grid.addWidget(on_surface_cell, 6, 0, 1, 15)

        on_surface_variant_cell = Shape()
        on_surface_variant_cell.setFixedHeight(60)
        on_surface_variant_cell.color = md_sys_color.on_surface_variant
        on_surface_variant_label = Typography()
        on_surface_variant_label.variant = "label-large"
        on_surface_variant_label.color = md_sys_color.surface_variant
        on_surface_variant_label.text = "On Surface Variant"
        on_surface_variant_label.setParent(on_surface_variant_cell)
        on_surface_variant_label.move(10, 10)
        grid.addWidget(on_surface_variant_cell, 6, 15, 1, 15)

        outline_cell = Shape()
        outline_cell.setFixedHeight(60)
        outline_cell.color = md_sys_color.outline
        outline_label = Typography()
        outline_label.variant = "label-large"
        outline_label.color = md_sys_color.surface_variant
        outline_label.text = "Outline"
        outline_label.setParent(outline_cell)
        outline_label.move(10, 10)
        grid.addWidget(outline_cell, 6, 30, 1, 15)

        outline_variant_cell = Shape()
        outline_variant_cell.setFixedHeight(60)
        outline_variant_cell.color = md_sys_color.outline_variant
        outline_variant_label = Typography()
        outline_variant_label.variant = "label-large"
        outline_variant_label.color = md_sys_color.on_surface
        outline_variant_label.text = "Outline Variant"
        outline_variant_label.setParent(outline_variant_cell)
        outline_variant_label.move(10, 10)
        grid.addWidget(outline_variant_cell, 6, 45, 1, 15)

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
