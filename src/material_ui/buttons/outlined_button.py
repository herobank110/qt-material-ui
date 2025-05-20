"""Outlined Button component."""

from material_ui.buttons._button_base import ButtonBase
from material_ui.tokens import md_comp_outlined_button as tokens


class OutlinedButton(ButtonBase):
    """OutlinedButton."""

    def __init__(self) -> None:
        super().__init__()
        self._container.sx = {
            **self._container.sx,
            "border-color": tokens.outline_color,
            "border-width": tokens.outline_width,
            "border-style": "solid",
        }
        self._container.opacity = 0.0
        self._ripple.color = tokens.pressed_state_layer_color
        self._label.sx = {
            **self._label.sx,
            "color": tokens.label_text_color,
            "font-size": tokens.label_text_size,
            "font-weight": tokens.label_text_weight,
        }
