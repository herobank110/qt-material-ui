"""Ripple (for pressing)."""

from material_ui._component import Component, effect, use_state
from material_ui.shape import Shape
from material_ui.tokens import md_sys_color, md_sys_state
from qtpy.QtCore import QPointF, Qt
from qtpy.QtGui import QPaintEvent, QPainter, QPainterPath, QColor

from material_ui.tokens._utils import resolve_token


class Ripple(Shape):
    """Ripple to overlay on a widget when pressed."""

    ripple_origin = use_state(QPointF())
    color = use_state(md_sys_color.primary)
    opacity = use_state(md_sys_state.pressed_state_layer_opacity)

    def __init__(self) -> None:
        super().__init__()
        # self.ripple_origin.changed.connect(lambda: self.update())

    @effect(ripple_origin, color, opacity)
    def _animate_ripple(self) -> None:
        # Tell Qt to call paintEvent.
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        super().paintEvent(event)
        painter = QPainter(self)
        clip_path = QPainterPath()
        half_size = min(self.width(), self.height()) // 2
        clip_path.addRoundedRect(self.rect(), half_size, half_size)
        painter.setClipPath(clip_path)
        painter.setPen(Qt.NoPen)
        color = QColor(resolve_token(self.color.get()))
        color.setAlphaF(resolve_token(self.opacity.get()))
        painter.setBrush(color)
        painter.drawEllipse(self.ripple_origin.get(), 50, 50)
