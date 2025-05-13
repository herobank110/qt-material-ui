"""A 'hidden' component that provides drop shadow."""

from qtpy import QtGui
from qtpy.QtWidgets import QWidget
from material_ui._component import Component, effect, use_state
from material_ui.shape import Shape
from material_ui.tokens import md_sys_elevation, md_sys_color, md_sys_shape


class Elevation(Component):
    """Elevation (aka drop shadow)."""

    elevation = use_state(md_sys_elevation.level0)
    shadow_color = use_state(md_sys_color.shadow)
    corner_shape = use_state(md_sys_shape.corner_none)

    def __init__(self) -> None:
        super().__init__()

    @effect(elevation, Component.size, QWidget.hasFocus)
    def f():
        pass
    # def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
    #     self.size
    #     return super().resizeEvent(event)
