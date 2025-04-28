"""Basic shape utility widget."""

from qtpy import QtGui
from typing import cast
from material_ui._component import Component, use_state
from material_ui.design_tokens import CornerShape


class Shape(Component):
    """A blank component with common shape features."""

    visible = use_state(True)
    corner_shape = use_state(cast(CornerShape, "none"))

    def __init__(self) -> None:
        super().__init__()

        self.visible.changed.connect(lambda value: self.setVisible(value))

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        if self.corner_shape.get() == "full":
            half_width = min(self.width(), self.height()) // 2
            self.sx.set(lambda prev: prev | {"border-radius": f"{half_width}px"})
        return super().resizeEvent(event)
