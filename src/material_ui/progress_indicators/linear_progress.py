"""Linear progress indicator."""

from typing import cast

from qtpy.QtGui import QColor, QPainter, QPaintEvent
from qtpy.QtWidgets import QSizePolicy

from material_ui.progress_indicators._base_progress import BaseProgress
from material_ui.tokens import md_comp_linear_progress_indicator as tokens
from material_ui.tokens._utils import resolve_token


class LinearProgress(BaseProgress):
    """Linear progress indicator component."""

    def __init__(self) -> None:
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        height = cast("int", resolve_token(tokens.track_height))
        self.setFixedHeight(height)

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Overridden QWidget.paintEvent."""
        super().paintEvent(event)
        painter = QPainter(self)

        active_color = cast("QColor", resolve_token(tokens.track_color))
        painter.setBrush(active_color)
        painter.drawRect(self.rect())

        active_color = cast("QColor", resolve_token(tokens.active_indicator_color))
        painter.setBrush(active_color)
        painter.drawRect(0, 0, self.value * self.width(), self.height())

        painter.end()
