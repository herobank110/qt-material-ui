from typing import Literal, cast
from material_ui._lab import DropShadow
from material_ui.ripple import Ripple
from material_ui.shape import Shape
from material_ui.tokens import md_comp_elevated_button as tokens
from material_ui._component import Component, Signal, effect, use_state
from material_ui.tokens._utils import resolve_token
from material_ui.typography import Typography
from qtpy import QtCore, QtGui


ButtonVariant = Literal[
    "elevated",
    "filled",
    "filled-tonal",
    "outlined",
    "text",
]


_TOUCH_AREA_Y_PADDING = 8


class ElevatedButton(Component):
    """Buttons let people take action and make choices with one tap."""

    clicked: Signal

    text = use_state("")
    variant = use_state(cast(ButtonVariant, "elevated"))

    hovered = use_state(False)
    pressed = use_state(False)

    def __init__(self) -> None:
        super().__init__()

        self.sx.set(
            {
                "margin": f"{_TOUCH_AREA_Y_PADDING}px 0px",
            }
        )

        self._drop_shadow = DropShadow()
        self._drop_shadow.color = tokens.container_shadow_color
        self._drop_shadow.elevation = tokens.container_elevation
        self.setGraphicsEffect(self._drop_shadow)

        self._ripple = Ripple()
        self._ripple.setParent(self)
        self._ripple.color = tokens.pressed_state_layer_color
        self._ripple.corner_shape.set("full")
        self._ripple.move(0, _TOUCH_AREA_Y_PADDING)
        self._ripple._size.bind(self._size)
        # self._ripple.opacity = tokens.pressed_state_layer_opacity

        self._container = Shape()
        self._container.corner_shape.set("full")
        self._container.sx.set({"background-color": tokens.container_color})
        self._container.setParent(self)
        self._container.move(0, _TOUCH_AREA_Y_PADDING)

        self._label = Typography()
        self._label.text.bind(self.text)
        self._label.sx.set(
            {
                "color": tokens.label_text_color,
                "font-size": tokens.label_text_size,
                "font-weight": tokens.label_text_weight,
            }
        )
        self._label.setParent(self)

    def sizeHint(self) -> QtCore.QSize:
        width = self._label.sizeHint().width() + 24 * 2
        base_height = resolve_token(tokens.container_height)
        height = base_height + _TOUCH_AREA_Y_PADDING * 2
        return QtCore.QSize(width, height)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        container_size = event.size().shrunkBy(
            QtCore.QMargins(0, _TOUCH_AREA_Y_PADDING, 0, _TOUCH_AREA_Y_PADDING)
        )
        self._container.resize(container_size)
        self._label.move(24, _TOUCH_AREA_Y_PADDING)
        self._label.resize(container_size.shrunkBy(QtCore.QMargins(24, 0, 24, 0)))

    @effect(hovered, pressed)
    def _update_drop_shadow_elevation(self) -> None:
        self._drop_shadow.animate_elevation_to(
            tokens.pressed_container_elevation
            if self.pressed.get()
            else tokens.hover_container_elevation
            if self.hovered.get()
            else tokens.container_elevation
        )

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        if event.button() == QtCore.Qt.LeftButton:
            self.pressed.set(True)
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        self.pressed.set(False)
        mouse_inside = self.rect().contains(event.pos())
        if event.button() == QtCore.Qt.LeftButton and mouse_inside:
            self.clicked.emit()
        return super().mouseReleaseEvent(event)

    def enterEvent(self, event: QtGui.QEnterEvent) -> None:  # noqa: N802
        self.hovered.set(True)
        return super().enterEvent(event)

    def leaveEvent(self, event: QtCore.QEvent) -> None:  # noqa: N802
        self.hovered.set(False)
        return super().leaveEvent(event)
