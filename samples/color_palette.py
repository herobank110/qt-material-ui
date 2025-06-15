"""Sample of the dynamic color palette system."""

from dataclasses import dataclass, replace

from material_ui._component import Component, effect, use_state
from material_ui.layout_basics import Row, Stack
from material_ui.switch import Switch
from material_ui.typography import Typography
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

        stack = Stack()

        dark_mode_row = Row()
        dark_mode_label = Typography()
        dark_mode_label.variant = "body-large"
        dark_mode_label.text = "Dark Mode"
        dark_mode_row.add_widget(dark_mode_label)
        self._dark_mode_switch = Switch()
        self._dark_mode_switch.on_change.connect(self._on_change_dark_mode)
        dark_mode_row.add_widget(self._dark_mode_switch)
        stack.add_widget(dark_mode_row)

        self.overlay_widget(stack)

    @effect(state)
    def _apply_state(self) -> None:
        self._dark_mode_switch.selected = self.state.is_dark

    def _on_change_dark_mode(self, selected: bool) -> None:  # noqa: FBT001
        self.state = replace(self.state, is_dark=selected)


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
