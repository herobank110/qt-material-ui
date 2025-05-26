"""Checkbox component."""

from typing import cast

from qtpy.QtCore import QEasingCurve, QPointF, Qt
from qtpy.QtGui import QColor, QLinearGradient
from qtpy.QtWidgets import QGraphicsOpacityEffect

from material_ui._component import Component, Signal, effect, use_state
from material_ui.icon import Icon
from material_ui.ripple import Ripple
from material_ui.shape import Shape
from material_ui.tokens import md_comp_checkbox as tokens
from material_ui.tokens._utils import resolve_token


class Checkbox(Component):
    """Checkbox component."""

    selected = use_state(False)
    """Whether the checkbox is checked."""

    indeterminate = use_state(False)
    """Whether the checkbox is in an indeterminate state."""

    on_change: Signal[bool]
    """Emitted when the user toggles the checkbox."""

    _outline_width = use_state(tokens.unselected_outline_width)
    _container_fill_opacity = use_state(1.0)
    _icon_name = use_state("check")
    _ripple_origin = use_state(cast("QPointF | None", None))
    _state_layer_color = use_state(tokens.unselected_hover_state_layer_color)
    _tick_fade_in_value = use_state(
        0.0,
        transition=100,
        easing=QEasingCurve.Type.InCubic,
    )

    def __init__(self) -> None:
        super().__init__()

        self.setFixedSize(48, 48)
        self.clicked.connect(self._on_clicked)
        self.should_propagate_click = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._container = Shape()
        self._container.corner_shape = tokens.container_shape
        self._container.setFixedSize(
            cast("int", resolve_token(tokens.container_height)),
            cast("int", resolve_token(tokens.container_width)),
        )
        self._container.color = tokens.selected_container_color
        self._container.opacity = self._container_fill_opacity
        self._container.setParent(self)
        self._container.move(15, 15)

        ripple = Ripple()
        ripple.ripple_origin = self._ripple_origin
        ripple.color = tokens.unselected_pressed_state_layer_color
        ripple.setParent(self)
        ripple.setFixedSize(
            cast("int", resolve_token(tokens.state_layer_size)),
            cast("int", resolve_token(tokens.state_layer_size)),
        )
        ripple.move(4, 4)

        state_layer = Shape()
        state_layer.setParent(self)
        state_layer.move(4, 4)
        state_layer.setFixedSize(
            cast("int", resolve_token(tokens.state_layer_size)),
            cast("int", resolve_token(tokens.state_layer_size)),
        )
        state_layer.corner_shape = tokens.state_layer_shape
        state_layer.color = self._state_layer_color
        state_layer.opacity = tokens.unselected_hover_state_layer_opacity
        state_layer.visible = self.hovered

        icon = Icon()
        icon.icon_name = self._icon_name
        icon.font_size = 14
        icon.weight = 600
        icon.color = tokens.selected_icon_color
        self._icon_opacity_effect = QGraphicsOpacityEffect()
        # Set opacity at 1 so only the mask has effect (default is 0.7).
        self._icon_opacity_effect.setOpacity(1.0)
        self._icon_opacity_effect.setParent(icon)
        icon.setGraphicsEffect(self._icon_opacity_effect)
        self._container.overlay_widget(icon, center=True)

    def _on_clicked(self) -> None:
        if self.indeterminate:
            self.indeterminate = False
            self.selected = True
        else:
            self.selected = not self.selected
        self.on_change.emit(not self.selected)

    @effect(selected, indeterminate)
    def _apply_main_visual_states(self) -> None:
        self._tick_fade_in_value = 1.0 if self.selected else 0.0
        self._outline_width = (
            tokens.selected_outline_width
            if self.selected or self.indeterminate
            else tokens.unselected_outline_width
        )
        self._container_fill_opacity = (
            1.0 if self.selected or self.indeterminate else 0.0
        )
        self._icon_name = (
            "check_indeterminate_small"
            if self.indeterminate
            else "check"
            if self.selected
            else ""
        )

    @effect(Component.pressed)
    def _set_ripple_origin(self) -> None:
        if self.pressed:
            self._ripple_origin = QPointF(self.width() / 2 - 2, self.height() / 2 - 2)
        else:
            self._ripple_origin = None

    @effect(_tick_fade_in_value, indeterminate)
    def _apply_icon_opacity_mask(self) -> None:
        if self.indeterminate or self._tick_fade_in_value == 1.0:
            self._icon_opacity_effect.setOpacityMask(QColor("white"))
            return
        grad = QLinearGradient()
        grad.setStart(0, 0)
        grad.setFinalStop(18, 0)
        grad.setColorAt(self._tick_fade_in_value, "white")
        grad.setColorAt(1, "transparent")
        self._icon_opacity_effect.setOpacityMask(grad)

    @effect(_outline_width)
    def _apply_outline_width(self) -> None:
        self._container.sx = {
            **self._container.sx,
            "border-width": self._outline_width,
            "border-color": tokens.unselected_outline_color,
            "border-style": "solid",
        }
