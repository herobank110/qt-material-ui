"""Text Button component."""

from material_ui.buttons._button_base import ButtonBase
from material_ui.tokens import md_comp_text_button as tokens


class TextButton(ButtonBase):
    """TextButton."""

    def _create(self) -> None:
        super()._create()
        self._container.opacity = 0.0
        self._ripple.color = tokens.pressed_state_layer_color
        self._label.font_family = tokens.label_text_font
        self._label.font_size = tokens.label_text_size
        self._label.font_weight = tokens.label_text_weight
        self._label.color = tokens.label_text_color
