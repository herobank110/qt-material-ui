"""Circular progress indicator."""

from typing import cast

from qtpy.QtCore import QMargins, QRect, QSize
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

    _start_angle = use_state(0)
    _span_angle = use_state(0)

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
            raise NotImplementedError

    @effect(_start_angle, _span_angle)
    def _update_on_angles_change(self) -> None:
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Paint the circular progress indicator."""
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = resolve_token(tokens.active_indicator_color)
        painter.setPen(QPen(color, float(self._thickness)))
        painter.drawArc(self._arc_rect, self._start_angle, self._span_angle)

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
