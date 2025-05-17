"""Filled text field component."""

from material_ui.shape import Shape
from material_ui.text_fields._base_text_field import BaseTextField
from material_ui.tokens import md_comp_filled_text_field as tokens


class FilledTextField(BaseTextField):
    """Filled text field component."""

    def __init__(self) -> None:
        super().__init__()

        background = Shape()
        background.corner_shape = tokens.container_shape
        background.sx = {
            "background-color": tokens.container_color,
            "height": tokens.container_height,
        }
