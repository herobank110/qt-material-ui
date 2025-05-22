"""Circular progress indicator."""

import math
import time
from typing import cast

from qtpy.QtCore import (
    QEasingCurve,
    QMargins,
    QPropertyAnimation,
    QRect,
    QSize,
    QTimerEvent,
)
from qtpy.QtGui import QPainter, QPaintEvent, QPen
from qtpy.QtWidgets import QSizePolicy

from material_ui._component import effect, use_state
from material_ui.progress_indicators._base_progress import BaseProgress
from material_ui.tokens import md_comp_circular_progress_indicator as tokens
from material_ui.tokens._utils import resolve_token


class CircularProgress(BaseProgress):
    """Circular progress indicator."""

    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size = resolve_token(tokens.size)
        self.setFixedSize(QSize(size, size))

        self._timer_id: int | None = None

    _start_angle = use_state(0)
    _span_angle = use_state(0)
    _t = use_state(0.0)

    @effect(BaseProgress.indeterminate)
    def _start_stop_indeterminate_animation(self) -> None:
        """Start or stop the indeterminate animation."""
        if self.indeterminate:
            # Use a short interval to make sure animations are applied.
            # Because we are using update to enqueue the paint, Qt will
            # supposedly optimize the actual paint calls until
            # necessary.
            self._timer_id = self.startTimer(10)
        elif self._timer_id:
            self.killTimer(self._timer_id)

    def timerEvent(self, event: QTimerEvent) -> None:  # noqa: N802
        """Animate the indeterminate progress."""
        if event.timerId() == self._timer_id:
            self._t = time.time_ns() / 1_000_000_000
        else:
            super().timerEvent(event)

    @effect(BaseProgress.value, BaseProgress.indeterminate)
    def _update_draw_parameters(self) -> None:
        if not (0.0 <= self.value <= 1.0):
            raise ValueError
        # Qt angles start at 3 o'clock, go counterclockwise and use
        # 1/16th of a degree as units.
        if not self.indeterminate:
            self._start_angle = 90 * 16
            self._span_angle = -int(self.value * 360 * 16)
        else:
            start_angle_animation = QPropertyAnimation()
            start_angle_animation.setParent(self)
            start_angle_animation.setTargetObject(self._find_state("_start_angle"))
            start_angle_animation.setPropertyName(b"_qt_property")
            start_angle_animation.setStartValue(-45 * 16)
            start_angle_animation.setKeyValueAt(0.45, -105 * 16)
            start_angle_animation.setKeyValueAt(0.65, -105 * 16)
            start_angle_animation.setEndValue(-405 * 16)
            start_angle_animation.setDuration(1333)
            start_angle_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            start_angle_animation.setLoopCount(-1)
            start_angle_animation.start()

            span_angle_animation = QPropertyAnimation()
            span_angle_animation.setParent(self)
            span_angle_animation.setTargetObject(self._find_state("_span_angle"))
            span_angle_animation.setPropertyName(b"_qt_property")
            span_angle_animation.setStartValue(-10 * 16)
            span_angle_animation.setKeyValueAt(0.45, -270 * 16)
            span_angle_animation.setKeyValueAt(0.65, -270 * 16)
            span_angle_animation.setEndValue(-10 * 16)
            span_angle_animation.setDuration(1333)
            span_angle_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            span_angle_animation.setLoopCount(-1)
            span_angle_animation.start()

    @effect(_start_angle, _span_angle, _t)
    def _update_on_angles_change(self) -> None:
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Paint the circular progress indicator."""
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = resolve_token(tokens.active_indicator_color)
        painter.setPen(QPen(color, float(self._thickness)))

        # For indeterminate

        start_angle = self._start_angle + self._indeterminate_angle_offset()
        painter.drawArc(self._arc_rect, start_angle, self._span_angle)

        painter.end()

    @property
    def _thickness(self) -> int:
        """Returns the thickness of the line."""
        return cast("int", resolve_token(tokens.active_indicator_width))

    @property
    def _arc_rect(self) -> QRect:
        """Returns the rectangle for the arc."""
        # Subtract padding so the line isn't drawn half out of bounds.
        p = self._thickness + 1
        return self.rect().marginsRemoved(QMargins(p, p, p, p))

    def _indeterminate_angle_offset(self) -> int:
        if not self.indeterminate:
            return 0

        layer1 = (self._t * 0.34) % 1
        layer2 = (math.sin(self._t * math.pi * 3) + 1) * 0.024
        return int((layer1 + layer2) * 360 * -16)
