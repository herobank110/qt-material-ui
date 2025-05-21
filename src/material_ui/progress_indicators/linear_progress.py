"""Linear progress indicator."""

from functools import partial
from typing import cast

from qtpy.QtCore import QRect, Qt, QVariantAnimation
from qtpy.QtGui import QColor, QPainter, QPaintEvent
from qtpy.QtWidgets import QSizePolicy, QWidget

from material_ui._component import Component, effect, use_state
from material_ui.progress_indicators._base_progress import BaseProgress
from material_ui.shape import Shape
from material_ui.tokens import md_comp_linear_progress_indicator as tokens
from material_ui.tokens._utils import resolve_token


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
        height = cast("int", resolve_token(tokens.track_height))
        self.setFixedHeight(height)

        # self._track = Shape()
        # self._track.color = tokens.track_color
        # self._track._size = self._size
        # self._track.setParent(self)

        # self._bar1_bar = Shape()
        # self._bar1_bar.color = tokens.active_indicator_color
        # # self._bar1_bar.resize(10, 10)
        # self._bar1_bar.setParent(self)

        # self._bar2_bar_wrapper = QWidget()
        # self._bar2_bar_wrapper.setParent(self)
        # hbox2 = QHBoxLayout(self._bar2_bar_wrapper)

        # self._bar2_bar = Shape()
        # self._bar2_bar.color = tokens.active_indicator_color
        # # self._bar2_bar.setParent(self._bar2_bar_wrapper)

    @effect(BaseProgress.value, BaseProgress.indeterminate)
    def _apply_bar_geometry(self) -> None:
        if not self.indeterminate:
            self._bar1_rect = QRect(0, 0, self.value * self.width(), self.height())
            self._bar2_rect = QRect()
        else:
            anim = QVariantAnimation()
            anim.setParent(self)
            anim.setStartValue(0.0)
            anim.setKeyValueAt(0.2, 0.0)
            anim.setKeyValueAt(0.5915, 0.836714)
            anim.setEndValue(2.00611)
            anim.setDuration(2000)
            anim.setLoopCount(-1)
            anim.valueChanged.connect(partial(setattr, self, "_bar1_translate"))
            anim.start()

            anim = QVariantAnimation()
            anim.setParent(self)
            anim.setStartValue(0.08)
            anim.setKeyValueAt(0.3665, 0.08)
            anim.setKeyValueAt(0.6915, 0.661479)
            anim.setEndValue(0.08)
            anim.setDuration(2000)
            anim.setLoopCount(-1)
            anim.valueChanged.connect(partial(setattr, self, "_bar1_scale"))
            anim.start()

            anim = QVariantAnimation()
            anim.setParent(self)
            anim.setStartValue(0.0)
            anim.setKeyValueAt(0.25, 0.376519)
            anim.setKeyValueAt(0.4835, 0.843862)
            anim.setEndValue(1.60278)
            anim.setDuration(2000)
            anim.setLoopCount(-1)
            anim.valueChanged.connect(partial(setattr, self, "_bar2_translate"))
            anim.start()

            anim = QVariantAnimation()
            anim.setParent(self)
            anim.setStartValue(0.08)
            anim.setKeyValueAt(0.1915, 0.457104)
            anim.setKeyValueAt(0.4415, 0.72796)
            anim.setEndValue(0.08)
            anim.setDuration(2000)
            anim.setLoopCount(-1)
            anim.valueChanged.connect(partial(setattr, self, "_bar2_scale"))
            anim.start()

    @effect(_bar1_translate, _bar1_scale, _bar2_translate, _bar2_scale)
    def _apply_animated_bar_geometry(self) -> None:
        w = self.width()
        h = self.height()

        # bar1_rect = QRect(self.rect())
        # bar1_rect.moveTopLeft()
        # # bar1_rect_center
        # bar1_rect.setWidth(w * self._bar1_scale)
        # bar1_rect.moveCenter(bar1_rect_center)

        self._bar1_rect = QRect(
            int(self._bar1_translate * w),
            0,
            int(self._bar1_scale * w),
            h,
        )
        self._bar2_rect = QRect(
            int(self._bar2_translate * w),
            0,
            int(self._bar2_scale * w),
            h,
        )
        print(f"bar1: {self._bar1_translate}                                                                   \r",end="")

    @effect(_bar1_rect, _bar2_rect)
    def _update_on_rect_change(self) -> None:
        self.update()

    # @effect(Component.size)
    # def _refresh_sizes(self) -> None:
    #     self._track.resize(self.size())
    #     self._bar1_bar.setFixedHeight(self.height())
    #     # r = QRect()
    #     # r.setWidth()
    #     # r.moveCenter()
    #     self._bar2_bar.setFixedHeight(self.height())

    # _bar1_line_pos

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Overridden QWidget.paintEvent."""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)

        active_color = cast("QColor", resolve_token(tokens.track_color))
        painter.setBrush(active_color)
        painter.drawRect(self.rect())

        active_color = cast("QColor", resolve_token(tokens.active_indicator_color))
        painter.setBrush(active_color)
        painter.drawRect(self._bar1_rect)
        painter.drawRect(self._bar2_rect)

        painter.end()
