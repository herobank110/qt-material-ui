"""Filled button."""

from material_ui._button_base import ButtonBase
from material_ui._component import effect
from material_ui.tokens import md_comp_filled_button as tokens


class FilledButton(ButtonBase):
    def __init__(self):
        super().__init__()
        self._drop_shadow.color = tokens.container_shadow_color
        self._drop_shadow.elevation = tokens.container_elevation
        self._container.sx = {"background-color": tokens.container_color}

    @effect(ButtonBase.hovered, ButtonBase.pressed)
    def _update_drop_shadow_elevation(self) -> None:
        self._drop_shadow.animate_elevation_to(
            {
                True: tokens.container_elevation,
                self.hovered.get(): tokens.hover_container_elevation,
                self.pressed.get(): tokens.pressed_container_elevation,
            }[True]
        )
