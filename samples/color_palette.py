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

        primary_cell = Shape(color=md_sys_color.primary)
        primary_cell.setFixedHeight(100)
        primary_label = Typography(
            parent=primary_cell,
            variant="label-large",
            color=md_sys_color.on_primary,
            text="Primary",
        )
        primary_label.move(10, 10)
        grid.addWidget(primary_cell, 0, 0, 1, 15)

        on_primary_cell = Shape(color=md_sys_color.on_primary)
        on_primary_cell.setFixedHeight(50)
        on_primary_label = Typography(
            parent=on_primary_cell,
            variant="label-large",
            color=md_sys_color.primary,
            text="On Primary",
        )
        on_primary_label.move(10, 10)
        grid.addWidget(on_primary_cell, 1, 0, 1, 15)

        secondary_cell = Shape(color=md_sys_color.secondary)
        secondary_cell.setFixedHeight(100)
        secondary_label = Typography(
            parent=secondary_cell,
            variant="label-large",
            color=md_sys_color.on_secondary,
            text="Secondary",
        )
        secondary_label.move(10, 10)
        grid.addWidget(secondary_cell, 0, 15, 1, 15)

        on_secondary_cell = Shape(color=md_sys_color.on_secondary)
        on_secondary_cell.setFixedHeight(50)
        on_secondary_label = Typography(
            parent=on_secondary_cell,
            variant="label-large",
            color=md_sys_color.secondary,
            text="On Secondary",
        )
        on_secondary_label.move(10, 10)
        grid.addWidget(on_secondary_cell, 1, 15, 1, 15)

        tertiary_cell = Shape(color=md_sys_color.tertiary)
        tertiary_cell.setFixedHeight(100)
        tertiary_label = Typography(
            parent=tertiary_cell,
            variant="label-large",
            color=md_sys_color.on_tertiary,
            text="Tertiary",
        )
        tertiary_label.move(10, 10)
        grid.addWidget(tertiary_cell, 0, 30, 1, 15)

        on_tertiary_cell = Shape(color=md_sys_color.on_tertiary)
        on_tertiary_cell.setFixedHeight(50)
        on_tertiary_label = Typography(
            parent=on_tertiary_cell,
            variant="label-large",
            color=md_sys_color.tertiary,
            text="On Tertiary",
        )
        on_tertiary_label.move(10, 10)
        grid.addWidget(on_tertiary_cell, 1, 30, 1, 15)

        error_cell = Shape(color=md_sys_color.error)
        error_cell.setFixedHeight(100)
        error_label = Typography(
            parent=error_cell,
            variant="label-large",
            color=md_sys_color.on_error,
            text="Error",
        )
        error_label.move(10, 10)
        grid.addWidget(error_cell, 0, 45, 1, 15)

        on_error_cell = Shape(color=md_sys_color.on_error)
        on_error_cell.setFixedHeight(50)
        on_error_label = Typography(
            parent=on_error_cell,
            variant="label-large",
            color=md_sys_color.error,
            text="On Error",
        )
        on_error_label.move(10, 10)
        grid.addWidget(on_error_cell, 1, 45, 1, 15)

        primary_container_cell = Shape(color=md_sys_color.primary_container)
        primary_container_cell.setFixedHeight(100)
        primary_container_label = Typography(
            parent=primary_container_cell,
            variant="label-large",
            color=md_sys_color.on_primary_container,
            text="Primary Container",
        )
        primary_container_label.move(10, 10)
        grid.addWidget(primary_container_cell, 2, 0, 1, 15)

        on_primary_container_cell = Shape(color=md_sys_color.on_primary_container)
        on_primary_container_cell.setFixedHeight(50)
        on_primary_container_label = Typography(
            parent=on_primary_container_cell,
            variant="label-large",
            color=md_sys_color.primary_container,
            text="On Primary Container",
        )
        on_primary_container_label.move(10, 10)
        grid.addWidget(on_primary_container_cell, 3, 0, 1, 15)

        secondary_container_cell = Shape(color=md_sys_color.secondary_container)
        secondary_container_cell.setFixedHeight(100)
        secondary_container_label = Typography(
            parent=secondary_container_cell,
            variant="label-large",
            color=md_sys_color.on_secondary_container,
            text="Secondary Container",
        )
        secondary_container_label.move(10, 10)
        grid.addWidget(secondary_container_cell, 2, 15, 1, 15)

        on_secondary_container_cell = Shape(color=md_sys_color.on_secondary_container)
        on_secondary_container_cell.setFixedHeight(50)
        on_secondary_container_label = Typography(
            parent=on_secondary_container_cell,
            variant="label-large",
            color=md_sys_color.secondary_container,
            text="On Secondary Container",
        )
        on_secondary_container_label.move(10, 10)
        grid.addWidget(on_secondary_container_cell, 3, 15, 1, 15)

        tertiary_container_cell = Shape(color=md_sys_color.tertiary_container)
        tertiary_container_cell.setFixedHeight(100)
        tertiary_container_label = Typography(
            parent=tertiary_container_cell,
            variant="label-large",
            color=md_sys_color.on_tertiary_container,
            text="Tertiary Container",
        )
        tertiary_container_label.move(10, 10)
        grid.addWidget(tertiary_container_cell, 2, 30, 1, 15)

        on_tertiary_container_cell = Shape(color=md_sys_color.on_tertiary_container)
        on_tertiary_container_cell.setFixedHeight(50)
        on_tertiary_container_label = Typography(
            parent=on_tertiary_container_cell,
            variant="label-large",
            color=md_sys_color.tertiary_container,
            text="On Tertiary Container",
        )
        on_tertiary_container_label.move(10, 10)
        grid.addWidget(on_tertiary_container_cell, 3, 30, 1, 15)

        error_container_cell = Shape(color=md_sys_color.error_container)
        error_container_cell.setFixedHeight(100)
        error_container_label = Typography(
            parent=error_container_cell,
            variant="label-large",
            color=md_sys_color.on_error_container,
            text="Error Container",
        )
        error_container_label.move(10, 10)
        grid.addWidget(error_container_cell, 2, 45, 1, 15)

        on_error_container_cell = Shape(color=md_sys_color.on_error_container)
        on_error_container_cell.setFixedHeight(50)
        on_error_container_label = Typography(
            parent=on_error_container_cell,
            variant="label-large",
            color=md_sys_color.error_container,
            text="On Error Container",
        )
        on_error_container_label.move(10, 10)
        grid.addWidget(on_error_container_cell, 3, 45, 1, 15)

        surface_dim_cell = Shape(color=md_sys_color.surface_dim)
        surface_dim_cell.setFixedHeight(100)
        surface_dim_label = Typography(
            parent=surface_dim_cell,
            variant="label-large",
            color=md_sys_color.on_surface,
            text="Surface Dim",
        )
        surface_dim_label.move(10, 10)
        grid.addWidget(surface_dim_cell, 4, 0, 1, 20)

        surface_cell = Shape(color=md_sys_color.surface)
        surface_cell.setFixedHeight(100)
        surface_label = Typography(
            parent=surface_cell,
            variant="label-large",
            color=md_sys_color.on_surface,
            text="Surface",
        )
        surface_label.move(10, 10)
        grid.addWidget(surface_cell, 4, 20, 1, 20)

        surface_bright_cell = Shape(color=md_sys_color.surface_bright)
        surface_bright_cell.setFixedHeight(100)
        surface_bright_label = Typography(
            parent=surface_bright_cell,
            variant="label-large",
            color=md_sys_color.on_surface,
            text="Surface Bright",
        )
        surface_bright_label.move(10, 10)
        grid.addWidget(surface_bright_cell, 4, 40, 1, 20)

        surface_container_lowest_cell = Shape(
            color=md_sys_color.surface_container_lowest,
        )
        surface_container_lowest_cell.setFixedHeight(100)
        surface_container_lowest_label = Typography(
            parent=surface_container_lowest_cell,
            variant="label-large",
            color=md_sys_color.on_surface,
            text="Surface Container Lowest",
        )
        surface_container_lowest_label.move(10, 10)
        grid.addWidget(surface_container_lowest_cell, 5, 0, 1, 12)

        surface_container_low_cell = Shape(color=md_sys_color.surface_container_low)
        surface_container_low_cell.setFixedHeight(100)
        surface_container_low_label = Typography(
            parent=surface_container_low_cell,
            variant="label-large",
            color=md_sys_color.on_surface,
            text="Surface Container Low",
        )
        surface_container_low_label.move(10, 10)
        grid.addWidget(surface_container_low_cell, 5, 12, 1, 12)

        surface_container_cell = Shape(color=md_sys_color.surface_container)
        surface_container_cell.setFixedHeight(100)
        surface_container_label = Typography(
            parent=surface_container_cell,
            variant="label-large",
            color=md_sys_color.on_surface,
            text="Surface Container",
        )
        surface_container_label.move(10, 10)
        grid.addWidget(surface_container_cell, 5, 24, 1, 12)

        surface_container_high_cell = Shape(color=md_sys_color.surface_container_high)
        surface_container_high_cell.setFixedHeight(100)
        surface_container_high_label = Typography(
            parent=surface_container_high_cell,
            variant="label-large",
            color=md_sys_color.on_surface,
            text="Surface Container High",
        )
        surface_container_high_label.move(10, 10)
        grid.addWidget(surface_container_high_cell, 5, 36, 1, 12)

        surface_container_highest_cell = Shape(
            color=md_sys_color.surface_container_highest,
        )
        surface_container_highest_cell.setFixedHeight(100)
        surface_container_highest_label = Typography(
            parent=surface_container_highest_cell,
            variant="label-large",
            color=md_sys_color.on_surface,
            text="Surface Container Highest",
        )
        surface_container_highest_label.move(10, 10)
        grid.addWidget(surface_container_highest_cell, 5, 48, 1, 12)

        on_surface_cell = Shape(color=md_sys_color.on_surface)
        on_surface_cell.setFixedHeight(60)
        on_surface_label = Typography(
            parent=on_surface_cell,
            variant="label-large",
            color=md_sys_color.surface,
            text="On Surface",
        )
        on_surface_label.move(10, 10)
        grid.addWidget(on_surface_cell, 6, 0, 1, 15)

        on_surface_variant_cell = Shape(color=md_sys_color.on_surface_variant)
        on_surface_variant_cell.setFixedHeight(60)
        on_surface_variant_label = Typography(
            parent=on_surface_variant_cell,
            variant="label-large",
            color=md_sys_color.surface_variant,
            text="On Surface Variant",
        )
        on_surface_variant_label.move(10, 10)
        grid.addWidget(on_surface_variant_cell, 6, 15, 1, 15)

        outline_cell = Shape(color=md_sys_color.outline)
        outline_cell.setFixedHeight(60)
        outline_label = Typography(
            parent=outline_cell,
            variant="label-large",
            color=md_sys_color.surface_variant,
            text="Outline",
        )
        outline_label.move(10, 10)
        grid.addWidget(outline_cell, 6, 30, 1, 15)

        outline_variant_cell = Shape(color=md_sys_color.outline_variant)
        outline_variant_cell.setFixedHeight(60)
        outline_variant_label = Typography(
            parent=outline_variant_cell,
            variant="label-large",
            color=md_sys_color.on_surface,
            text="Outline Variant",
        )
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

        stack = Stack(
            alignment=Qt.AlignmentFlag.AlignTop,
            gap=15,
            margins=QMargins(20, 20, 20, 20),
        )
        stack.add_widget(
            Typography(
                variant="headline-medium",
                text="Color Palette",
                color=md_sys_color.on_surface,
            ),
        )
        self._color_hex_textfield = FilledTextField(
            label="Color (Hex)",
            on_change=self._on_change_color_hex,
        )
        stack.add_widget(self._color_hex_textfield)

        dark_mode_row = Row(gap=5)
        dark_mode_row.add_widget(
            Typography(
                variant="body-large",
                text="Dark Mode",
                color=md_sys_color.on_surface,
                alignment=Qt.AlignmentFlag.AlignVCenter,
            ),
        )
        self._dark_mode_switch = Switch(on_change=self._on_change_dark_mode)
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

    def _create(self) -> None:
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
