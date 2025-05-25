"""Components to simplify layout of a few items."""

from typing import cast

from qtpy.QtCore import QMargins, Qt
from qtpy.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from material_ui._component import Component, effect, use_state

_DefaultAlignment = cast("Qt.AlignmentFlag", Qt.AlignmentFlag())  # type: ignore[assignment, call-arg]


class Row(Component):
    """A horizontal container."""

    alignment = use_state(_DefaultAlignment)
    gap = use_state(0)
    margins = use_state(QMargins())

    def __init__(self) -> None:
        super().__init__()
        self._hbox = QHBoxLayout(self)

    def add_widget(self, widget: QWidget) -> None:
        """Add a widget to the row."""
        self._hbox.addWidget(widget)

    @effect(gap, alignment, margins)
    def _update_hbox(self) -> None:
        self._hbox.setSpacing(self.gap)
        self._hbox.setAlignment(self.alignment)
        self._hbox.setContentsMargins(self.margins)


class Stack(Component):
    """A vertical container."""

    alignment = use_state(_DefaultAlignment)
    gap = use_state(0)
    margins = use_state(QMargins())

    def __init__(
        self,
        *,
        alignment: Qt.AlignmentFlag | None = None,
        gap: int | None = None,
        margins: QMargins | None = None,
    ) -> None:
        super().__init__()

        self._vbox = QVBoxLayout(self)

        if alignment is not None:
            self.alignment = alignment
        if gap is not None:
            self.gap = gap
        if margins is not None:
            self.margins = margins

    def add_widget(self, widget: QWidget) -> None:
        """Add a widget to the stack."""
        self._vbox.addWidget(widget)

    @effect(gap, alignment, margins)
    def _update_vbox(self) -> None:
        self._vbox.setSpacing(self.gap)
        self._vbox.setAlignment(self.alignment)
        self._vbox.setContentsMargins(self.margins)
