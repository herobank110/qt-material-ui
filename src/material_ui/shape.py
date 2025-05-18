"""Basic shape utility widget."""

from typing import TYPE_CHECKING, cast

from qtpy import QtGui

from material_ui._component import Component, effect, use_state

if TYPE_CHECKING:
    from material_ui.design_tokens import CornerShape


class Shape(Component):
    """A blank component with common shape features."""

    visible = use_state(True)
    corner_shape = use_state(cast("CornerShape", "none"))

    def __init__(self) -> None:
        super().__init__()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:  # noqa: N802, D102
        if self.corner_shape == "full":
            half_width = min(self.width(), self.height()) // 2
            self.sx = {**self.sx, "border-radius": f"{half_width}px"}
        return super().resizeEvent(event)

    @effect(visible)
    def _apply_visible(self) -> None:
        self.setVisible(self.visible)
