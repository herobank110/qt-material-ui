"""Base class for button variants."""

from typing import cast

from qtpy.QtCore import QMargins, QSize, Qt
from qtpy.QtGui import QMouseEvent
from qtpy.QtWidgets import QHBoxLayout

from material_ui._component import Component, Signal, effect, use_state
from material_ui._lab import DropShadow
from material_ui.ripple import Ripple
from material_ui.shape import Shape

# Use the tokens from elevated_button for code completion, but they will
# get overridden by the subclasses.
from material_ui.tokens import md_comp_elevated_button as tokens
from material_ui.tokens._utils import resolve_token
from material_ui.typography import Typography

_TOUCH_AREA_Y_PADDING = 8
_TOUCH_AREA_MARGINS = QMargins(0, _TOUCH_AREA_Y_PADDING, 0, _TOUCH_AREA_Y_PADDING)


class ButtonBase(Component):
    """Base class for button variants."""

    clicked: Signal

    text = use_state("")

    hovered = use_state(False)
    pressed = use_state(False)

    def __init__(self) -> None:
        super().__init__()

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sx = {"margin": f"{_TOUCH_AREA_Y_PADDING}px 0px"}

        self._drop_shadow = DropShadow()
        self.setGraphicsEffect(self._drop_shadow)

        self._container = Shape()
        self._container.corner_shape = tokens.container_shape
        self._container.setParent(self)
        self._container.move(0, _TOUCH_AREA_Y_PADDING)

        self._state_layer = Shape()
        self._state_layer.setParent(self._container)
        self._state_layer.corner_shape = tokens.container_shape

        self._ripple = Ripple()
        self._ripple.setParent(self._container)

        container_layout = QHBoxLayout(self._container)
        container_layout.setContentsMargins(QMargins(24, 0, 24, 0))
        container_layout.setSpacing(0)

        self._label = Typography()
        self._label.text = self.text
        self._label.alignment = Qt.AlignmentFlag.AlignCenter
        container_layout.addWidget(self._label)

    def sizeHint(self) -> QSize:  # noqa: N802
        height = cast("int", resolve_token(tokens.container_height))
        return (
            self._container.sizeHint()
            # For some reason, setting the fixedHeight on the container
            # won't apply to its sizeHint, so set the height here.
            .expandedTo(QSize(0, height))
            .grownBy(_TOUCH_AREA_MARGINS)
        )

    @effect(Component.size)
    def _apply_element_sizes(self) -> None:
        # Since Qt has no 'overlay' layout, manually set these sizes.
        container_size = self.size().shrunkBy(_TOUCH_AREA_MARGINS)
        self._container.resize(container_size)
        self._state_layer.resize(container_size)
        self._ripple.resize(container_size)

    @effect(hovered)
    def _update_state_layer(self) -> None:
        self._state_layer.color = tokens.hover_state_layer_color
        self._state_layer.opacity = (
            tokens.hover_state_layer_opacity if self.hovered else 0.0
        )

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._ripple.ripple_origin = event.position()
        return super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        if event.button() == Qt.MouseButton.LeftButton:
            self._ripple.ripple_origin = None
        return super().mouseReleaseEvent(event)
