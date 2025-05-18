"""A 'hidden' component that provides drop shadow."""

from qtpy.QtCore import QPointF, QRectF, Qt
from qtpy.QtGui import QColor, QPainter
from qtpy.QtWidgets import QGraphicsDropShadowEffect, QGraphicsEffect

from material_ui._component import Component, effect, use_state
from material_ui.shape import Shape
from material_ui.tokens import md_sys_color, md_sys_elevation, md_sys_shape
from material_ui.tokens._utils import DesignToken, find_root_token, resolve_token

# TODO: implement token generator overrides for missing tokens for level5

_ELEVATION_KEY_OFFSET_MAP: dict[DesignToken, QPointF] = {
    md_sys_elevation.level0: QPointF(0.0, 0.0),
    md_sys_elevation.level1: QPointF(0.0, 1.0),
    md_sys_elevation.level2: QPointF(0.0, 1.0),
    md_sys_elevation.level3: QPointF(0.0, 1.0),
    md_sys_elevation.level4: QPointF(0.0, 2.0),
    # md_sys_elevation.level5: QPointF(0.0, 4.0),
}

_ELEVATION_KEY_BLUR_RADIUS_MAP: dict[DesignToken, int] = {
    md_sys_elevation.level0: 0,
    md_sys_elevation.level1: 2,
    md_sys_elevation.level2: 2,
    md_sys_elevation.level3: 3,
    md_sys_elevation.level4: 3,
    # md_sys_elevation.level5: 4,
}

_ELEVATION_AMBIENT_OFFSET_MAP: dict[DesignToken, QPointF] = {
    md_sys_elevation.level0: QPointF(0.0, 0.0),
    md_sys_elevation.level1: QPointF(0.0, 1.0),
    md_sys_elevation.level2: QPointF(0.0, 2.0),
    md_sys_elevation.level3: QPointF(0.0, 3.0),
    md_sys_elevation.level4: QPointF(0.0, 6.0),
    # md_sys_elevation.level5: QPointF(0.0, 8.0),
}

_ELEVATION_AMBIENT_BLUR_RADIUS_MAP: dict[DesignToken, int] = {
    md_sys_elevation.level0: 0,
    md_sys_elevation.level1: 3,
    md_sys_elevation.level2: 6,
    md_sys_elevation.level3: 8,
    md_sys_elevation.level4: 10,
    # md_sys_elevation.level5: 12,
}


class Elevation(Component):
    """Elevation (aka drop shadow)."""

    elevation = use_state(md_sys_elevation.level0)
    shadow_color = use_state(md_sys_color.shadow)
    corner_shape = use_state(md_sys_shape.corner_none)

    def __init__(self) -> None:
        super().__init__()

        # Have to set a background for Qt's DropShadow to work...!
        # TODO: remove once using custom graphics effect
        self.sx.set({"background-color": "white"})

        # TODO: also add key shadow
        self._ambient_shadow = QGraphicsDropShadowEffect()
        self._ambient_shadow.setParent(self)
        self.setGraphicsEffect(self._ambient_shadow)

    @effect(corner_shape, Component.size)
    def _apply_corner_shape(self):
        """Apply corner shape."""
        # TODO: move to common place?
        shape = find_root_token(self.corner_shape)
        if shape is md_sys_shape.corner_none:
            new_radius = 0
        elif shape is md_sys_shape.corner_full:
            new_radius = min(self.width(), self.height()) // 2
        else:
            raise RuntimeError("unsupported corner shape", shape)
        self.sx.set(lambda prev: prev | {"border-radius": new_radius})

    @effect(shadow_color)
    def _apply_shadow_colors(self):
        """Apply shadow colors."""
        color = resolve_token(self.shadow_color)
        if not isinstance(color, QColor):
            raise RuntimeError(
                f"invalid shadow_color token: expected QColor, got {type(color).__name__}"
            )

        ambient_color = QColor(color)
        # TODO: once using multi shadow, alpha values are: key=0.3, ambient=0.15
        ambient_color.setAlphaF(0.35)
        self._ambient_shadow.setColor(ambient_color)

    @effect(elevation)
    def _apply_elevation(self):
        """Apply elevation."""
        elevation = find_root_token(self.elevation)
        self._ambient_shadow.setBlurRadius(
            _ELEVATION_AMBIENT_BLUR_RADIUS_MAP[elevation]
        )
        self._ambient_shadow.setOffset(_ELEVATION_AMBIENT_OFFSET_MAP[elevation])
