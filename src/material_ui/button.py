from typing import Literal, cast
from material_ui._lab import DropShadow
from material_ui.ripple import Ripple
from material_ui.shape import Shape
from material_ui.tokens import md_comp_elevated_button as tokens
from material_ui._component import Component, Signal, effect, use_state
from material_ui.tokens._utils import resolve_token
from material_ui.typography import Typography
from qtpy import QtCore, QtGui
from qtpy.QtCore import QSize, QMargins
from qtpy.QtWidgets import QHBoxLayout


ButtonVariant = Literal[
    "elevated",
    "filled",
    "filled-tonal",
    "outlined",
    "text",
]


_TOUCH_AREA_Y_PADDING = 8
_TOUCH_AREA_MARGINS = QMargins(0, _TOUCH_AREA_Y_PADDING, 0, _TOUCH_AREA_Y_PADDING)


class ElevatedButton(Component):
    """Buttons let people take action and make choices with one tap."""

    clicked: Signal

    text = use_state("")
    variant = use_state(cast(ButtonVariant, "elevated"))

    hovered = use_state(False)
    pressed = use_state(False)

    def __init__(self) -> None:
        super().__init__()

        self.sx = {
            "margin": f"{_TOUCH_AREA_Y_PADDING}px 0px",
        }

        self._drop_shadow = DropShadow()
        self._drop_shadow.color = tokens.container_shadow_color
        self._drop_shadow.elevation = tokens.container_elevation
        self.setGraphicsEffect(self._drop_shadow)

        self._container = Shape()
        self._container.corner_shape = "full"
        self._container.sx = {"background-color": tokens.container_color}
        self._container.setParent(self)
        self._container.move(0, _TOUCH_AREA_Y_PADDING)

        self._state_layer = Shape()
        self._state_layer.setParent(self._container)
        self._state_layer.corner_shape = "full"

        self._ripple = Ripple()
        self._ripple.setParent(self._container)
        self._ripple.color = tokens.pressed_state_layer_color
        self._ripple.corner_shape = "full"

        container_layout = QHBoxLayout(self._container)
        container_layout.setContentsMargins(QMargins(24, 0, 24, 0))
        container_layout.setSpacing(0)

        self._label = Typography()
        self._label.text.bind(self.text)
        self._label.alignment = QtCore.Qt.AlignmentFlag.AlignCenter
        self._label.sx = {
            "color": tokens.label_text_color,
            "font-size": tokens.label_text_size,
            "font-weight": tokens.label_text_weight,
        }
        container_layout.addWidget(self._label)

    def sizeHint(self) -> QtCore.QSize:
        return (
            self._container.sizeHint()
            # For some reason, setting the fixedHeight on the container
            # won't apply to its sizeHint, so set the height here.
            .expandedTo(QSize(0, resolve_token(tokens.container_height)))
            .grownBy(_TOUCH_AREA_MARGINS)
        )

    @effect(Component.size)
    def _apply_element_sizes(self) -> None:
        # Since Qt has no 'overlay' layout, manually set these sizes.
        container_size = self.size().shrunkBy(_TOUCH_AREA_MARGINS)
        self._container.resize(container_size)
        self._state_layer.resize(container_size)
        self._ripple.resize(container_size)

    @effect(hovered, pressed)
    def _update_drop_shadow_elevation(self) -> None:
        self._drop_shadow.animate_elevation_to(
            {
                True: tokens.container_elevation,
                self.hovered.get(): tokens.hover_container_elevation,
                self.pressed.get(): tokens.pressed_container_elevation,
            }[True]
        )

    @effect(hovered)
    def _update_state_layer(self) -> None:
        color = QtGui.QColor(resolve_token(tokens.hover_state_layer_color))
        hover_opacity = resolve_token(tokens.hover_state_layer_opacity)
        color.setAlphaF(hover_opacity if self.hovered.get() else 0.0)
        self._state_layer.sx.set(lambda prev: prev | {"background-color": color})

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        if event.button() == QtCore.Qt.LeftButton:
            self.pressed = True
            self._ripple.ripple_origin = event.position()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        self.pressed = False
        self._ripple.ripple_origin = None
        mouse_inside = self.rect().contains(event.pos())
        if event.button() == QtCore.Qt.LeftButton and mouse_inside:
            self.clicked.emit()
        return super().mouseReleaseEvent(event)

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:  # noqa: N802
        self.hovered = True
        return super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:  # noqa: N802
        self.hovered = False
        return super().leaveEvent(event)
