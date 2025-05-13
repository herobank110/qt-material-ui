"""A 'hidden' component that provides drop shadow."""

from qtpy.QtCore import QPointF
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QGraphicsDropShadowEffect
from material_ui._component import Component, effect, use_state
from material_ui.shape import Shape
from material_ui.tokens import md_sys_elevation, md_sys_color, md_sys_shape
from material_ui.tokens._utils import DesignToken, resolve_token

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

# // level0: box-shadow: 0px 0px 0px 0px;
# // level1: box-shadow: 0px 1px 3px 1px;
# // level2: box-shadow: 0px 2px 6px 2px;
# // level3: box-shadow: 0px 4px 8px 3px;
# // level4: box-shadow: 0px 6px 10px 4px;
# // level5: box-shadow: 0px 8px 12px 6px;

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

        self._key_shape = Shape()
        self._key_shape.setParent(self)
        self._key_shape.corner_shape.bind(self.corner_shape)
        self._key_shape._size.bind(self._size)
        self._key_shadow = QGraphicsDropShadowEffect()
        self._key_shape.setGraphicsEffect(self._key_shadow)

        self._ambient_shape = Shape()
        self._ambient_shape.setParent(self)
        self._ambient_shape.corner_shape.bind(self.corner_shape)
        self._ambient_shape._size.bind(self._size)
        self._ambient_shadow = QGraphicsDropShadowEffect()
        self._ambient_shape.setGraphicsEffect(self._ambient_shadow)

    @effect(shadow_color)
    def _apply_shadow_colors(self):
        """Apply shadow colors."""
        color = resolve_token(self.shadow_color.get())
        if not isinstance(color, QColor):
            raise RuntimeError(
                f"invalid shadow_color token: expected QColor, got {type(color).__name__}"
            )

        key_color = QColor(color)
        key_color.setAlphaF(0.3)
        self._key_shadow.setColor(key_color)

        ambient_color = QColor(color)
        ambient_color.setAlphaF(0.15)
        self._ambient_shadow.setColor(color)
