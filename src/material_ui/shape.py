"""Basic shape utility widget."""

from typing import cast

from qtpy.QtCore import Qt
from qtpy.QtGui import QColor

from material_ui._component import Component, effect, use_state
from material_ui.theming.theme_hook import ThemeHook
from material_ui.tokens import md_sys_color, md_sys_shape
from material_ui.tokens._utils import (
    DesignToken,
    find_root_token,
    resolve_token,
    resolve_token_or_value,
)


class Shape(Component):
    """A blank component with common shape features."""

    visible = use_state(True)
    corner_shape = use_state(md_sys_shape.corner_none)
    color = use_state(cast("QColor | DesignToken", QColor("transparent")))
    opacity = use_state(cast("float | DesignToken", 1.0))

    @effect(corner_shape, Component.size)
    def _apply_corner_shape(self) -> None:
        token = find_root_token(self.corner_shape)
        # TODO: make the shape non identical tokens not compare equal
        if token is md_sys_shape.corner_none:
            update = {"border-radius": 0}
        elif token is md_sys_shape.corner_extra_extra_small:
            update = {"border-radius": 2}
        elif token is md_sys_shape.corner_extra_small:
            update = {"border-radius": 4}
        elif token is md_sys_shape.corner_extra_small_top:
            update = {"border-top-left-radius": 4, "border-top-right-radius": 4}
        elif token is md_sys_shape.corner_small:
            update = {"border-radius": 8}
        elif token is md_sys_shape.corner_medium:
            update = {"border-radius": 12}
        elif token is md_sys_shape.corner_large:
            update = {"border-radius": 16}
        elif token is md_sys_shape.corner_large_top:
            update = {"border-top-left-radius": 16, "border-top-right-radius": 16}
        elif token is md_sys_shape.corner_large_start:
            update = {"border-top-left-radius": 16, "border-bottom-left-radius": 16}
        elif token is md_sys_shape.corner_large_end:
            update = {"border-top-right-radius": 16, "border-bottom-right-radius": 16}
        elif token is md_sys_shape.corner_extra_large:
            update = {"border-radius": 28}
        elif token is md_sys_shape.corner_extra_large_top:
            update = {"border-top-left-radius": 28, "border-top-right-radius": 28}
        elif token is md_sys_shape.corner_full:
            half_size = min(self.width(), self.height()) // 2
            update = {"border-radius": half_size}
        else:
            raise ValueError
        self.sx = {**self.sx, **update}

    @effect(visible)
    def _apply_visible(self) -> None:
        self.setVisible(self.visible)

    @effect(color, opacity, ThemeHook)
    def _apply_background_color(self) -> None:
        color = resolve_token_or_value(self.color)
        opacity = resolve_token_or_value(self.opacity)
        # Make a copy to keep the design token's value unmodified.
        color = QColor(color)
        color.setAlphaF(opacity)
        self.sx = {**self.sx, "background-color": color}


class Line(Component):
    """A straight line."""

    color = use_state(md_sys_color.outline)
    thickness = use_state(cast("int | DesignToken", 1))
    orientation = use_state(Qt.Orientation.Horizontal)

    @effect(color, thickness, orientation)
    def _apply_line(self) -> None:
        self.sx = {"background-color": self.color}

        # Set one of the dimensions to the thickness. Parent component
        # will have to set the other dimension.
        match self.orientation:
            case Qt.Orientation.Horizontal:
                self.setFixedHeight(self.resolved_thickness())
            case Qt.Orientation.Vertical:
                self.setFixedWidth(self.resolved_thickness())
            case _:
                raise ValueError

    def resolved_thickness(self) -> int:
        """Return the resolved thickness of the line."""
        if isinstance(self.thickness, DesignToken):
            if isinstance(resolved := resolve_token(self.thickness), int):
                return resolved
            raise TypeError
        return self.thickness
