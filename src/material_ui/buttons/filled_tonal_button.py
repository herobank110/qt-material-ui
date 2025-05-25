"""FilledTonalButton component."""

from material_ui._component import effect
from material_ui.buttons._button_base import ButtonBase
from material_ui.tokens import md_comp_filled_tonal_button as tokens


class FilledTonalButton(ButtonBase):
    """FilledTonalButton."""

    def __init__(self) -> None:
        super().__init__()
        self._drop_shadow.shadow_color = tokens.container_shadow_color
        self._drop_shadow.elevation = tokens.container_elevation
        self._container.color = tokens.container_color
        self._ripple.color = tokens.pressed_state_layer_color
        self._label.font_family = tokens.label_text_font
        self._label.font_size = tokens.label_text_size
        self._label.font_weight = tokens.label_text_weight
        self._label.color = tokens.label_text_color

    @effect(ButtonBase.hovered, ButtonBase.pressed)
    def _update_drop_shadow_elevation(self) -> None:
        self._drop_shadow.animate_elevation_to(
            {
                True: tokens.container_elevation,
                self.hovered: tokens.hover_container_elevation,
                self.pressed: tokens.pressed_container_elevation,
            }[True],
        )
