"""Checkbox component."""

from typing import cast

from qtpy.QtCore import QEasingCurve, QPointF, Qt
from qtpy.QtGui import QColor, QLinearGradient, QMouseEvent
from qtpy.QtWidgets import QGraphicsOpacityEffect

from material_ui._component import Component, effect, use_state
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

        container = Shape()
        container.corner_shape = tokens.container_shape
        container.setFixedSize(
            resolve_token(tokens.container_height),
            resolve_token(tokens.container_width),
        )
        container.color = resolve_token(tokens.selected_container_color)
        container.setParent(self)
        container.move(12, 12)
        ripple = Ripple()
        ripple.ripple_origin = self._ripple_origin
        ripple.color = tokens.unselected_pressed_state_layer_color
        ripple.setFixedSize(
            resolve_token(tokens.state_layer_size),
            resolve_token(tokens.state_layer_size),
        )
        ripple.setParent(self)

        state_layer = Shape()
        state_layer.setParent(self)
        state_layer.setFixedSize(
            resolve_token(tokens.state_layer_size),
            resolve_token(tokens.state_layer_size),
        )
        state_layer.corner_shape = tokens.state_layer_shape
        state_layer.color = self._state_layer_color
        state_layer.opacity = tokens.unselected_hover_state_layer_opacity
        state_layer.visible = self.hovered

        icon = Icon()
        icon.icon_name = self._icon_name
        icon.font_size = 14
        icon.color = tokens.selected_icon_color
        self._icon_opacity_effect = QGraphicsOpacityEffect()
        # Set opacity at 1 so only the mask has effect (default is 0.7).
        self._icon_opacity_effect.setOpacity(1.0)
        self._icon_opacity_effect.setParent(icon)
        icon.setGraphicsEffect(self._icon_opacity_effect)

        container.overlay_widget(icon)

    def _on_clicked(self) -> None:
        if self.indeterminate:
            self.indeterminate = False
            self.selected = True
        else:
            self.selected = not self.selected

    @effect(selected, indeterminate)
    def _apply_icon(self) -> None:
        if self.indeterminate:
            self._icon_name = "check_indeterminate_small"
        elif self.selected:
            self._icon_name = "check"
        else:
            self._icon_name = ""

    @effect(Component.pressed)
    def _apply_ripple_origin(self) -> None:
        if self.pressed:
            self._ripple_origin = QPointF(self.width() / 2 - 2, self.height() / 2 - 2)
        else:
            self._ripple_origin = None

    @effect(selected)
    def _animate_tick_fade_in(self) -> None:
        self._tick_fade_in_value = 1.0 if self.selected else 0.0

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
