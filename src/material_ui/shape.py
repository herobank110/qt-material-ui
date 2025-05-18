"""Basic shape utility widget."""

from typing import TYPE_CHECKING, cast

from qtpy import QtGui

from material_ui._component import Component, effect, use_state
from material_ui.tokens import md_sys_shape
from material_ui.tokens._utils import find_root_token


class Shape(Component):
    """A blank component with common shape features."""

    visible = use_state(True)
    corner_shape = use_state(md_sys_shape.corner_none)

    def __init__(self) -> None:
        super().__init__()

    @effect(corner_shape, Component.size)
    def _apply_corner_shape(self) -> None:
        token = find_root_token(self.corner_shape)
        # TODO: make the shape non identical tokens not compare equal
        if token is md_sys_shape.corner_none:
            update = {"border-radius": "none"}
        elif token is md_sys_shape.corner_extra_small:
            update = {"border-radius": "4px"}
        elif token is md_sys_shape.corner_extra_small_top:
            update = {
                "border-top-left-radius": "4px",
                "border-top-right-radius": "4px",
            }
        elif token is md_sys_shape.corner_small:
            update = {"border-radius": "8px"}
        elif token is md_sys_shape.corner_medium:
            update = {"border-radius": "12px"}
        elif token is md_sys_shape.corner_large:
            update = {"border-radius": "16px"}
        elif token is md_sys_shape.corner_large_top:
            update = {
                "border-top-left-radius": "16px",
                "border-top-right-radius": "16px",
            }
        elif token is md_sys_shape.corner_large_start:
            update = {
                "border-top-left-radius": "16px",
                "border-bottom-left-radius": "16px",
            }
        elif token is md_sys_shape.corner_large_end:
            update = {
                "border-top-right-radius": "16px",
                "border-bottom-right-radius": "16px",
            }
        elif token is md_sys_shape.corner_extra_large:
            update = {"border-radius": "28px"}
        elif token is md_sys_shape.corner_extra_large_top:
            update = {
                "border-top-left-radius": "28px",
                "border-top-right-radius": "28px",
            }
        elif token is md_sys_shape.corner_full:
            half_size = min(self.width(), self.height()) // 2
            update = {"border-radius": f"{half_size}px"}
        else:
            raise ValueError
        self.sx = {**self.sx, **update}

    @effect(visible)
    def _apply_visible(self) -> None:
        self.setVisible(self.visible)
