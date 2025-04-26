"""Components to simplify layout of a few items."""

from material_ui._component import Component
from qtpy import QtWidgets


class Row(Component):
    """A horizontal container."""

    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        """Add a widget to the row."""
        self.layout().addWidget(widget)


class Stack(Component):
    """A vertical container."""

    def __init__(self) -> None:
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

    def add_widget(self, widget: QtWidgets.QWidget) -> None:
        """Add a widget to the stack."""
        self.layout().addWidget(widget)
