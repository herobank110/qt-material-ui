"""Linear progress indicator."""

from functools import partial
from typing import cast

from qtpy.QtCore import QEasingCurve, QPointF, QRect, Qt, QVariantAnimation
from qtpy.QtGui import QColor, QPainter, QPaintEvent
from qtpy.QtWidgets import QSizePolicy

from material_ui._component import effect, use_state
from material_ui.progress_indicators._base_progress import BaseProgress
from material_ui.tokens import md_comp_linear_progress_indicator as tokens
from material_ui.tokens._utils import resolve_token

_INDETERMINATE_ANIM_DURATION = 2000
_INDETERMINATE_ANIM_EASING = QEasingCurve(QEasingCurve.Type.BezierSpline)
_INDETERMINATE_ANIM_EASING.addCubicBezierSegment(
    QPointF(0.2, 0.3),
    QPointF(0.9, 1.0),
    QPointF(1.0, 1.0),
)


class LinearProgress(BaseProgress):
    """Linear progress indicator component."""

    _bar1_rect = use_state(QRect())
    _bar2_rect = use_state(QRect())

    _bar1_translate = use_state(0.0)
    _bar1_scale = use_state(0.0)
    _bar2_translate = use_state(0.0)
    _bar2_scale = use_state(0.0)

    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(cast("int", resolve_token(tokens.track_height)))

    @effect(BaseProgress.value, BaseProgress.indeterminate)
    def _apply_bar_geometry(self) -> None:
        if not self.indeterminate:
            self._bar1_rect = QRect(0, 0, int(self.value * self.width()), self.height())
            self._bar2_rect = QRect()
        else:
            # Magic numbers from material-web implementation:
            # https://github.com/material-components/material-web/blob/main/progress/internal/_linear-progress.scss#L141
            anim = QVariantAnimation()
            anim.setParent(self)
            anim.setStartValue(0.0 - 1.45167)
            anim.setKeyValueAt(0.4, 0.0 - 1.45167)
            anim.setKeyValueAt(0.5515, 0.836714 - 1.45167)
            anim.setEndValue(2.00611 - 1.45167)
            anim.setDuration(_INDETERMINATE_ANIM_DURATION)
            anim.setEasingCurve(_INDETERMINATE_ANIM_EASING)
            anim.setLoopCount(-1)
            anim.valueChanged.connect(partial(setattr, self, "_bar1_translate"))
            anim.start()

            anim = QVariantAnimation()
            anim.setParent(self)
            anim.setStartValue(0.08)
            anim.setKeyValueAt(0.3665, 0.08)
            anim.setKeyValueAt(0.6915, 0.561479)
            anim.setKeyValueAt(0.93, 0.08)
            anim.setEndValue(0.08)
            anim.setDuration(_INDETERMINATE_ANIM_DURATION)
            anim.setEasingCurve(_INDETERMINATE_ANIM_EASING)
            anim.setLoopCount(-1)
            anim.valueChanged.connect(partial(setattr, self, "_bar1_scale"))
            anim.start()

            anim = QVariantAnimation()
            anim.setParent(self)
            anim.setStartValue(0.0 - 0.548889)
            anim.setKeyValueAt(0.25, 0.376519 - 0.548889)
            anim.setKeyValueAt(0.4835, 0.843862 - 0.548889)
            anim.setEndValue(1.60278 - 0.548889)
            anim.setDuration(_INDETERMINATE_ANIM_DURATION)
            anim.setEasingCurve(_INDETERMINATE_ANIM_EASING)
            anim.setLoopCount(-1)
            anim.valueChanged.connect(partial(setattr, self, "_bar2_translate"))
            anim.start()

            anim = QVariantAnimation()
            anim.setParent(self)
            anim.setStartValue(0.08)
            anim.setKeyValueAt(0.1915, 0.457104)
            anim.setKeyValueAt(0.4415, 0.72796)
            anim.setEndValue(0.08)
            anim.setDuration(_INDETERMINATE_ANIM_DURATION)
            anim.setEasingCurve(_INDETERMINATE_ANIM_EASING)
            anim.setLoopCount(-1)
            anim.valueChanged.connect(partial(setattr, self, "_bar2_scale"))
            anim.start()

    @effect(_bar1_translate, _bar1_scale, _bar2_translate, _bar2_scale)
    def _apply_animated_bar_geometry(self) -> None:
        w = self.width()
        h = self.height()

        # Condense 2 nested rects into 1 by offsetting the position so
        # that the inner rect would appear centered.
        self._bar1_rect = QRect(
            int((self._bar1_translate + (1 - self._bar1_scale) / 2) * w),
            0,
            int(self._bar1_scale * w),
            h,
        )

        self._bar2_rect = QRect(
            int((self._bar2_translate + (1 - self._bar2_scale) / 2) * w),
            0,
            int(self._bar2_scale * w),
            h,
        )

    @effect(_bar1_rect, _bar2_rect)
    def _update_on_rect_change(self) -> None:
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Overridden QWidget.paintEvent."""
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(cast("QColor", resolve_token(tokens.track_color)))
        painter.drawRect(self.rect())

        painter.setBrush(cast("QColor", resolve_token(tokens.active_indicator_color)))
        painter.drawRect(self._bar1_rect)
        painter.drawRect(self._bar2_rect)

        painter.end()
