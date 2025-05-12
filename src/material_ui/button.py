from typing import Literal, cast
from material_ui._lab import DropShadow
from material_ui.shape import Shape
from material_ui.tokens import md_comp_elevated_button as tokens
from material_ui._component import Component, Signal, effect, use_state
from material_ui.tokens._utils import resolve_token
from material_ui.typography import Typography
from qtpy import QtCore, QtGui, QtWidgets


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

    # elevation = use_state(
    #     lambda self: elevated_tokens.hover_container_elevation if self.hovered else 0
    # )

    # _elevation = use_state(tokens.container_elevation)

    # @effect(hovered)
    # def elevation(self):
    #     if self.hovered:
    #         return tokens.hover_container_elevation
    #     return tokens.container_elevation

    def __init__(self) -> None:
        super().__init__()

        self.sx.set(
            {
                "margin": f"{_TOUCH_AREA_Y_PADDING}px 0px",
            }
        )
        # self.setFixedSize(100, 60)

        self._container = Shape()
        self._container.corner_shape.set("full")
        self._container.sx.set({"background-color": tokens.container_color})
        self._container.setParent(self)
        self._container.move(0, _TOUCH_AREA_Y_PADDING)
        self._drop_shadow = DropShadow()
        self._drop_shadow.color = tokens.container_shadow_color
        self._drop_shadow.elevation = tokens.container_elevation
        # container_drop_shadow.elevation = lambda: (
        #     tokens.hover_container_elevation
        #     if self.hovered
        #     else tokens.container_elevation
        # )
        # self._container.setGraphicsEffect(container_drop_shadow)
        self.setGraphicsEffect(self._drop_shadow)

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
        # margins = QtCore.QMargins(24, 0, 24, 0)
        # self.overlay_widget(self._label, margins)

    def sizeHint(self) -> QtCore.QSize:
        base_height = resolve_token(tokens.container_height)
        y = base_height + _TOUCH_AREA_Y_PADDING * 2

        x = self._label.sizeHint().width() + 24 * 2

        return QtCore.QSize(x, y)

    def resizeEvent(self, event):
        print("resizeEvent", event.size())
        container_size = event.size().shrunkBy(
            QtCore.QMargins(0, _TOUCH_AREA_Y_PADDING, 0, _TOUCH_AREA_Y_PADDING)
        )
        self._container.resize(container_size)
        self._label.move(24, _TOUCH_AREA_Y_PADDING)
        self._label.resize(container_size.shrunkBy(QtCore.QMargins(24, 0, 24, 0)))
        return super().resizeEvent(event)

    @effect(hovered)
    def _update_drop_shadow_elevation(self) -> None:
        self._drop_shadow.animate_elevation_to(
            tokens.hover_container_elevation
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
