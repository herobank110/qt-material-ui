"""Checkbox component."""

from material_ui._component import Component, use_state
from material_ui.icon import Icon
from material_ui.shape import Shape
from material_ui.tokens import md_comp_checkbox as tokens
from material_ui.tokens._utils import resolve_token


class Checkbox(Component):
    """Checkbox component."""

    selected = use_state(False)
    """Whether the checkbox is checked."""

    indeterminate = use_state(False)
    """Whether the checkbox is in an indeterminate state."""

    def __init__(self) -> None:
        super().__init__()

        self._container = Shape()
        self._container.setFixedSize(
            resolve_token(tokens.container_height),
            resolve_token(tokens.container_width),
        )
        self._container.color = resolve_token(tokens.selected_container_color)
        self.overlay_widget(self._container)

        self._icon = Icon()
        self._icon.icon_name = "check"
        self._container.overlay_widget(self._icon)
