"""Components to simplify layout of a few items."""

from typing import cast
from material_ui._component import Component, effect, use_state
from qtpy import QtCore, QtWidgets


class Row(Component):
    """A horizontal container."""

    alignment = use_state(cast(QtCore.Qt.AlignmentFlag, QtCore.Qt.AlignmentFlag()))
    gap = use_state(0)

    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(self.gap.get())
        self.gap.changed.connect(layout.setSpacing)
        layout.setAlignment(self.alignment.get())
        self.alignment.changed.connect(layout.setAlignment)

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        """Add a widget to the row."""
        self.layout().addWidget(widget)


class Stack(Component):
    """A vertical container."""

    alignment = use_state(cast(QtCore.Qt.AlignmentFlag, QtCore.Qt.AlignmentFlag()))
    gap = use_state(0)
    margins = use_state(QtCore.QMargins())

    def __init__(
        self,
        *,
        alignment: QtCore.Qt.AlignmentFlag | None = None,
        gap: int | None = None,
        margins: QtCore.QMargins | None = None,
    ) -> None:
        super().__init__()

        if alignment is not None:
            self.alignment.set(alignment)
        if gap is not None:
            self.gap.set(gap)
        if margins is not None:
            self.margins.set(margins)

        self._vbox = QtWidgets.QVBoxLayout(self)

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        """Add a widget to the stack."""
        self.layout().addWidget(widget)

    @effect(gap, alignment, margins)
    def _update_vbox(self) -> None:
        self._vbox.setSpacing(self.gap.get())
        self._vbox.setAlignment(self.alignment.get())
        self._vbox.setContentsMargins(self.margins.get())
