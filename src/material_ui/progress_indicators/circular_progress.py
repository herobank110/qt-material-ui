"""Circular progress indicator."""

from qtpy.QtCore import QSize
from qtpy.QtGui import QPainter, QPaintEvent
from qtpy.QtWidgets import QSizePolicy

from material_ui._component import Component, use_state
from material_ui.tokens import md_comp_circular_progress_indicator as tokens
from material_ui.tokens import md_comp_progress_indicator as base_tokens
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

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Paint the circular progress indicator."""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), "red")
