"""Components to simplify layout of a few items."""

from typing import cast

from qtpy import QtCore, QtWidgets

from material_ui._component import Component, effect, use_state


class Row(Component):
    """A horizontal container."""

    alignment = use_state(cast(QtCore.Qt.AlignmentFlag, QtCore.Qt.AlignmentFlag()))
    gap = use_state(0)
    margins = use_state(QtCore.QMargins())

    def __init__(self) -> None:
        super().__init__()
        self._hbox = QtWidgets.QHBoxLayout(self)

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        """Add a widget to the row."""
        self.layout().addWidget(widget)

    @effect(gap, alignment, margins)
    def _update_hbox(self) -> None:
        self._hbox.setSpacing(self.gap)
        self._hbox.setAlignment(self.alignment)
        self._hbox.setContentsMargins(self.margins)


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
        self._vbox.setSpacing(self.gap)
        self._vbox.setAlignment(self.alignment)
        self._vbox.setContentsMargins(self.margins)
