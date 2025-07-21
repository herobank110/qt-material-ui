"""Components to simplify layout of a few items."""

from qtpy.QtCore import QMargins, Qt
from qtpy.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from material_ui._component import Component, effect, use_state
from material_ui._utils import default_alignment


class Row(Component):
    """A horizontal container."""

    alignment: Qt.AlignmentFlag = use_state(default_alignment)
    gap: int = use_state(0)
    margins: QMargins = use_state(QMargins())

    def _create(self) -> None:
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

    alignment: Qt.AlignmentFlag = use_state(default_alignment)
    gap: int = use_state(0)
    margins: QMargins = use_state(QMargins())

    def _create(self) -> None:
        self._vbox = QVBoxLayout(self)

    def add_widget(self, widget: QWidget) -> None:
        """Add a widget to the stack."""
        self._vbox.addWidget(widget)

    @effect(gap, alignment, margins)
    def _update_vbox(self) -> None:
        self._vbox.setSpacing(self.gap)
        self._vbox.setAlignment(self.alignment)
        self._vbox.setContentsMargins(self.margins)
