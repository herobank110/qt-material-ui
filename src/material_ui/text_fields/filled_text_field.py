"""Filled text field component."""

from qtpy.QtCore import QMargins, QPoint

from material_ui._component import Component, effect
from material_ui.layout_basics import Row
from material_ui.shape import Line, Shape
from material_ui.text_fields._base_text_field import BaseTextField
from material_ui.tokens import md_comp_filled_text_field as tokens


class FilledTextField(BaseTextField):
    """Filled text field component."""

    _RESTING_LABEL_POS = QPoint(16, 18)
    _FLOATING_LABEL_POS = QPoint(18, 8)

    def __init__(self) -> None:
        super().__init__()

        self._background = Shape()
        self._background.corner_shape = tokens.container_shape
        self._background.color = tokens.container_color
        self._background.setParent(self)

        state_layer = Shape()
        state_layer.corner_shape = tokens.container_shape
        state_layer.visible = self.hovered
        state_layer.color = tokens.hover_state_layer_color
        state_layer.opacity = tokens.hover_state_layer_opacity
        self._background.overlay_widget(state_layer)

        self._active_indicator = Line()
        self._active_indicator.setParent(self._background)

        self._floating_label.setParent(self._background)
        self._floating_label.sx = {
            "font-family": tokens.label_text_font,
            "font-size": tokens.label_text_populated_size,
            "font-weight": tokens.label_text_weight,
        }
        self._floating_label.move(self._FLOATING_LABEL_POS)
        self._resting_label.setParent(self._background)
        self._resting_label.sx = {
            "font-family": tokens.label_text_font,
            "font-size": tokens.label_text_size,
            "font-weight": tokens.label_text_weight,
        }
        self._resting_label.move(self._RESTING_LABEL_POS)

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
            "margin-top": "14px",
        }
        line_edit_wrapper.overlay_widget(self._line_edit)
        row.add_widget(line_edit_wrapper)

    @effect(Component.size)
    def _apply_size(self) -> None:
        self._background.resize(self.size())
        self._active_indicator.setFixedWidth(self._background.width())

    @effect(Component.size, Component.focused)
    def _refresh_active_indicator(self) -> None:
        if self.focused:
            self._active_indicator.color = tokens.focus_active_indicator_color
            self._active_indicator.thickness = tokens.focus_active_indicator_thickness
        else:
            self._active_indicator.color = tokens.active_indicator_color
            self._active_indicator.thickness = tokens.active_indicator_height
        # TODO: use an overlay layout that will just handle anchoring to
        #   bottom of background
        self._active_indicator.move(
            0,
            self._background.height() - self._active_indicator.resolved_thickness(),
        )

    @effect(Component.focused)
    def _refresh_label(self) -> None:
        color = (
            tokens.focus_label_text_color if self.focused else tokens.label_text_color
        )
        self._floating_label.sx = {**self._floating_label.sx, "color": color}
        self._resting_label.sx = {**self._resting_label.sx, "color": color}
