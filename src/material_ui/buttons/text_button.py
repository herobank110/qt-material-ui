"""Text Button component."""

from material_ui.buttons._button_base import ButtonBase
from material_ui.tokens import md_comp_text_button as tokens


class TextButton(ButtonBase):
    """TextButton."""

    def __init__(self) -> None:
        super().__init__()
        self._ripple.color = tokens.pressed_state_layer_color
        self._label.sx = {
            "color": tokens.label_text_color,
            "font-size": tokens.label_text_size,
            "font-weight": tokens.label_text_weight,
        }
