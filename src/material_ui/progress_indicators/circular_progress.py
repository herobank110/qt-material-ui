"""Circular progress indicator."""

import time
from typing import cast

from qtpy.QtCore import (
    QEasingCurve,
    QMargins,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
    QTimerEvent,
)
from qtpy.QtGui import QPainter, QPaintEvent, QPen
from qtpy.QtWidgets import QSizePolicy

from material_ui._component import Component, effect, use_state
from material_ui.tokens import md_comp_circular_progress_indicator as tokens
from material_ui.tokens._utils import resolve_token


class CircularProgress(Component):
    """Circular progress indicator."""

    value = use_state(0.0)
    """Progress percentage, in range [0, 1]."""

    indeterminate = use_state(False)
    """Whether the progress is indeterminate (looping animation)."""

    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        size = resolve_token(tokens.size)
        self.setFixedSize(QSize(size, size))

        self._timer_id: int | None = None

    _start_angle = use_state(0)
    _span_angle = use_state(0)
    _t = use_state(0)

    @effect(indeterminate)
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
            self._t = time.time_ns()
        else:
            super().timerEvent(event)

    @effect(value, indeterminate)
    def _update_draw_parameters(self) -> None:
        if not (0.0 <= self.value <= 1.0):
            raise ValueError
        # Qt angles start at 3 o'clock, go counterclockwise and use
        # 1/16th of a degree as units.
        if not self.indeterminate:
            self._start_angle = 90 * 16
            self._span_angle = -int(self.value * 360 * 16)
        else:
            # a = self._t
            # self.animate(self._start_angle,
            #              start_value=2,
            #              num_loops="infinite")

            start_angle_animation = QPropertyAnimation()
            start_angle_animation.setParent(self)
            start_angle_animation.setTargetObject(self._find_state("_start_angle"))
            start_angle_animation.setPropertyName(b"_qt_property")
            start_angle_animation.setStartValue(-45 * 16)
            start_angle_animation.setKeyValueAt(0.5, -105 * 16)
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
            span_angle_animation.setKeyValueAt(0.5, -270 * 16)
            span_angle_animation.setEndValue(-10 * 16)
            span_angle_animation.setDuration(1333)
            span_angle_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            span_angle_animation.setLoopCount(-1)
            span_angle_animation.start()
            # self._span_angle = -10 * 16

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
        time_seconds = self._t / 1_000_000_000
        import math
        # painter.rotate(math.sin(time_seconds) * math.pi / 2)
        painter.drawArc(self._arc_rect, self._start_angle + ((time_seconds*0.333) % 1 * 360) * -16, self._span_angle)

        painter.end()

    @property
    def _thickness(self) -> int:
        """Returns the thickness of the line."""
        return cast("int", resolve_token(tokens.active_indicator_width))

    @property
    def _arc_rect(self) -> QRect:
        """Returns the rectangle for the arc."""
        # Subtract padding so the line isn't drawn half out of bounds.
        p = self._thickness // 2
        return self.rect().marginsRemoved(QMargins(p, p, p, p))
