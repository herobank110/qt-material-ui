"""Filled text field component."""

from material_ui._component import Component
from material_ui.shape import Shape
from material_ui.text_fields._base_text_field import BaseTextField
from material_ui.tokens import md_comp_filled_text_field as tokens
from material_ui.layout_basics import Row
from material_ui.shape import Shape
from qtpy.QtCore import QSize, QMargins, Qt, QPoint


class FilledTextField(BaseTextField):
    """Filled text field component."""

    _RESTING_LABEL_POS = QPoint(0, 16)
    _FLOATING_LABEL_POS = QPoint(0, 8)

    def __init__(self) -> None:
        super().__init__()

        background = Shape()
        background.corner_shape = tokens.container_shape
        background.sx = {
            "background-color": tokens.container_color,
            "height": tokens.container_height,
        }
        background.setParent(self)

        self._floating_label.setParent(background)
        self._floating_label.sx = {
            "color": tokens.label_text_color,
            "font-family": tokens.label_text_font,
            "font-size": tokens.label_text_populated_size,
            "font-weight": tokens.label_text_weight,
        }
        self._resting_label.setParent(background)
        self._resting_label.sx = {
            "color": tokens.label_text_color,
            "font-family": tokens.label_text_font,
            "font-size": tokens.label_text_populated_size,
            "font-weight": tokens.label_text_weight,
        }

        row = Row()
        row.gap = 16
        row.margins = QMargins(16, 8, 16, 8)
        self.overlay_widget(row)

        # Use a wrapper to use the sx property, which Qt will propagate
        # to children by default.
        line_edit_wrapper = Component()
        line_edit_wrapper.sx = {
            "color": tokens.input_text_color,
            "font-family": tokens.input_text_font,
            "font-size": tokens.input_text_size,
            "font-weight": tokens.input_text_weight,
        }
        line_edit_wrapper.overlay_widget(self._line_edit)
        row.add_widget(line_edit_wrapper)
