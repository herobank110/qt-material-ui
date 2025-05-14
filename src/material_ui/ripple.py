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
    _draw_origin = use_state(QPointF(0, 0))
    _scale = use_state(0.0)

    @effect(ripple_origin, color, opacity)
    def _animate_ripple(self) -> None:
        # Tell Qt to call paintEvent.
        self.update()

    @effect(ripple_origin)
    def _ripple_effect(self) -> None:
        origin = self.ripple_origin.get()
        if origin is None:
            # Fade out the ripple when the origin is reset. I.e., when
            # the button is released.
            self._opacity_value.animate_to(0.0, 400, QEasingCurve.OutCubic)
            return
        self._draw_origin = origin
        self._opacity_value.animate_to(
            resolve_token(self.opacity.get()), 100, QEasingCurve.OutCubic
        )
        self._scale.set(3.0)
        print(self.size())
        ripple_total_scale = max(self.width(), self.height()) * 2.2
        self._scale.animate_to(ripple_total_scale, 1000, QEasingCurve.OutCubic)

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
        painter.drawEllipse(
            self._draw_origin.get(), self._scale.get(), self._scale.get()
        )
        print(f"{self._scale.get()}\r", end="")
