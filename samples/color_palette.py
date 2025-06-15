"""Sample of the dynamic color palette system."""

from dataclasses import dataclass, replace

from material_ui._component import Component, effect, use_state
from material_ui.layout_basics import Row, Stack
from material_ui.switch import Switch
from material_ui.text_fields.outlined_text_field import OutlinedTextField
from material_ui.tokens import md_sys_color
from material_ui.typography import Typography
from qtpy.QtCore import QMargins, Qt
from qtpy.QtWidgets import QApplication


class ColorGrid(Component):
    def __init__(self) -> None:
        super().__init__()


@dataclass
class ControlsState:
    color_hex: str = "#4181EE"
    is_dark: bool = False


class Controls(Component):
    state = use_state(ControlsState())

    def __init__(self) -> None:
        super().__init__()

        self.sx = {"background-color": md_sys_color.background}

        stack = Stack()
        stack.alignment = Qt.AlignmentFlag.AlignTop
        stack.gap = 15
        stack.margins = QMargins(20, 20, 20, 20)

        title = Typography()
        title.variant = "title-large"
        title.text = "Color Palette"
        stack.add_widget(title)

        self._color_hex_textfield = OutlinedTextField()
        self._color_hex_textfield.label = "Color (Hex)"
        self._color_hex_textfield.on_change.connect(self._on_change_color_hex)
        stack.add_widget(self._color_hex_textfield)

        dark_mode_row = Row()
        dark_mode_row.gap = 5
        dark_mode_label = Typography()
        dark_mode_label.variant = "body-large"
        dark_mode_label.text = "Dark Mode"
        dark_mode_label.alignment = Qt.AlignmentFlag.AlignVCenter
        dark_mode_row.add_widget(dark_mode_label)
        self._dark_mode_switch = Switch()
        self._dark_mode_switch.on_change.connect(self._on_change_dark_mode)
        dark_mode_row.add_widget(self._dark_mode_switch)
        stack.add_widget(dark_mode_row)

        self.overlay_widget(stack)

    @effect(state)
    def _apply_state(self) -> None:
        self._dark_mode_switch.selected = self.state.is_dark
        self._color_hex_textfield.value = self.state.color_hex

    def _on_change_dark_mode(self, selected: bool) -> None:  # noqa: FBT001
        self.state = replace(self.state, is_dark=selected)

    def _on_change_color_hex(self, value: str) -> None:
        self.state = replace(self.state, color_hex=value)


class DemoColorPalette(Component):
    def __init__(self) -> None:
        super().__init__()

        row1 = Row()

        color_grid = ColorGrid()
        row1.add_widget(color_grid)

        controls = Controls()
        row1.add_widget(controls)

        self.overlay_widget(row1)


def main() -> None:
    app = QApplication()
    window = DemoColorPalette()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
