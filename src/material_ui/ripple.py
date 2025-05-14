"""Ripple (for pressing)."""

from typing import cast
from material_ui._component import Component, effect, use_state
from material_ui.shape import Shape
from material_ui.tokens import md_sys_color, md_sys_state
from qtpy.QtCore import QPointF, Qt, QEasingCurve
from qtpy.QtGui import QPaintEvent, QPainter, QPainterPath, QColor

from material_ui.tokens._utils import resolve_token


class Ripple(Shape):
    """Ripple to overlay on a widget when pressed."""

    ripple_origin = use_state(cast(QPointF | None, None))
    color = use_state(md_sys_color.primary)
    opacity = use_state(md_sys_state.pressed_state_layer_opacity)

    _opacity_value = use_state(0.0)
    _ripple_scale = use_state(0.0)

    def __init__(self) -> None:
        super().__init__()
        # self.ripple_origin.changed.connect(lambda: self.update())

    @effect(ripple_origin, color, opacity)
    def _animate_ripple(self) -> None:
        # Tell Qt to call paintEvent.
        self.update()

    @effect(ripple_origin)
    def _ripple_effect(self) -> None:
        if self.ripple_origin.get() is None:
            # Fade out the ripple when the origin is reset. I.e., when
            # the button is released.
            self._opacity_value.animate_to(0.0, 200, QEasingCurve.OutCubic)
            return
        self._opacity_value.animate_to(
            resolve_token(self.opacity.get()), 100, QEasingCurve.OutCubic
        )
        self._ripple_scale.set(5.0)
        ripple_total_scale = max(self.width(), self.height())
        self._ripple_scale.animate_to(ripple_total_scale, 200, QEasingCurve.OutCubic)

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        super().paintEvent(event)
        if self.ripple_origin.get() is None and self._opacity_value.get() == 0.0:
            # Nothing to draw.
            return
        painter = QPainter(self)
        clip_path = QPainterPath()
        half_size = min(self.width(), self.height()) // 2
        clip_path.addRoundedRect(self.rect(), half_size, half_size)
        painter.setClipPath(clip_path)
        painter.setPen(Qt.NoPen)
        color = QColor(resolve_token(self.color.get()))
        color.setAlphaF(self._opacity_value.get())
        painter.setBrush(color)
        origin = self.ripple_origin.get() or QPointF(0, 0) # Full rect...
        painter.drawEllipse(origin, self._ripple_scale.get(), self._ripple_scale.get())
