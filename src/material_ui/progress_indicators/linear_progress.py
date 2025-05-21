"""Linear progress indicator."""

from typing import cast

from qtpy.QtCore import QSize
from qtpy.QtGui import QPainter, QPaintEvent
from qtpy.QtWidgets import QSizePolicy

from material_ui._component import Component, effect, use_state
from material_ui.tokens import md_comp_linear_progress_indicator as tokens
from material_ui.tokens._utils import resolve_token


class LinearProgress(Component):
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
        painter.fillRect(self.rect(), "red")
        painter.end()
