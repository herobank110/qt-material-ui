"""Ripple (for pressing)."""

from typing import cast

from qtpy.QtCore import QEasingCurve, QPointF, Qt
from qtpy.QtGui import QColor, QPainter, QPainterPath, QPaintEvent

from material_ui._component import Component, effect, use_state
from material_ui.tokens import md_sys_color, md_sys_state
from material_ui.tokens._utils import resolve_token


class Ripple(Component):
    """Ripple to overlay on a widget when pressed."""

    ripple_origin = use_state(cast("QPointF | None", None))
    color = use_state(md_sys_color.primary)
    opacity = use_state(md_sys_state.pressed_state_layer_opacity)

    _opacity_value = use_state(0.0)
    _draw_origin = use_state(QPointF(0, 0))
    _scale = use_state(0.0)

    @effect(_opacity_value, _draw_origin, _scale)
    def _update_widget(self) -> None:
        # Tell Qt to call paintEvent.
        self.update()

    @effect(ripple_origin)
    def _animate_ripple_values(self) -> None:
        origin = self.ripple_origin
        if origin is None:
            # Fade out the ripple when the origin is reset. I.e., when
            # the button is released.
            self._find_state("_opacity_value").animate_to(
                0.0,
                800,
                QEasingCurve.Type.OutCubic,
            )
            return
        self._draw_origin = QPointF(origin)  # copy not bind
        self._find_state("_opacity_value").animate_to(
            resolve_token(self.opacity), 50, QEasingCurve.Type.OutCubic
        )
        self._scale = 1.0
        ripple_total_scale = max(self.width(), self.height()) * 2
        self._find_state("_scale").animate_to(
            ripple_total_scale, 1200, QEasingCurve.Type.OutCubic
        )

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Draw the ripple effect."""
        super().paintEvent(event)
        painter = QPainter(self)
        clip_path = QPainterPath()
        half_size = min(self.width(), self.height()) // 2
        clip_path.addRoundedRect(self.rect(), half_size, half_size)
        painter.setClipPath(clip_path)
        painter.setPen(Qt.PenStyle.NoPen)
        color = QColor(resolve_token(self.color))
        color.setAlphaF(self._opacity_value)
        painter.setBrush(color)
        painter.drawEllipse(self._draw_origin, self._scale, self._scale)
        painter.end()
