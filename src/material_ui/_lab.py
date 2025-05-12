"""Experimental file for figuring things out."""

from material_ui.tokens import DesignToken, resolve_token
from qtpy.QtWidgets import QGraphicsDropShadowEffect
from qtpy.QtGui import QColor
from qtpy.QtCore import QPropertyAnimation, QEasingCurve, QPoint
from material_ui.tokens import md_sys_elevation, md_sys_color


class DropShadow(QGraphicsDropShadowEffect):
    """Drop shadow supporting Material design tokens.

    TODO:
      transition for elevation
      2 shadows per elevation level - key and ambient
        see: https://github.com/material-components/material-web/blob/main/elevation/internal/_elevation.scss#L63
    """

    def __init__(self) -> None:
        super().__init__()

        self._elevation = md_sys_elevation.level0
        self._shadow_color = md_sys_color.shadow

    @property
    def elevation(self) -> DesignToken:
        """Get the elevation value."""
        return self._elevation

    @elevation.setter
    def elevation(self, value: DesignToken) -> None:
        """Set the elevation value."""
        if self._elevation == value:
            return
        self._elevation = value
        self._apply_elevation()

    def _apply_elevation(self) -> None:
        self.setBlurRadius(self._get_computed_blur_radius())
        self.setOffset(self._get_computed_offset())

    def _get_computed_blur_radius(self):
        return resolve_token(self._elevation)

    def _get_computed_offset(self):
        _ELEVATION_OFFSET_MAP = {
            md_sys_elevation.level0: QPoint(0, 0),
            md_sys_elevation.level1: QPoint(0, 1),
            md_sys_elevation.level2: QPoint(0, 1),
            md_sys_elevation.level3: QPoint(0, 1),
            md_sys_elevation.level4: QPoint(0, 2),
            # TODO: implement token generator overrides for missing tokens
            # md_sys_elevation.level5: QPoint(0, 4),
        }

        return _ELEVATION_OFFSET_MAP[self._elevation]

    def animate_elevation_to(self, value: DesignToken) -> None:
        """Animate the elevation to a new value."""
        self.elevation = value

        blur_radius_animation = QPropertyAnimation()
        blur_radius_animation.setParent(self)
        blur_radius_animation.setTargetObject(self)
        blur_radius_animation.setPropertyName(b"blurRadius")
        blur_radius_animation.setEndValue(self._get_computed_blur_radius())
        blur_radius_animation.setDuration(280)
        blur_radius_animation.setEasingCurve(QEasingCurve.OutCubic)
        blur_radius_animation.start()

        offset_animation = QPropertyAnimation()
        offset_animation.setParent(self)
        offset_animation.setTargetObject(self)
        offset_animation.setPropertyName(b"offset")
        offset_animation.setEndValue(self._get_computed_offset())
        offset_animation.setDuration(280)
        offset_animation.setEasingCurve(QEasingCurve.OutCubic)
        offset_animation.start()

    @property
    def shadow_color(self) -> DesignToken:
        """Get the shadow color value."""
        return self._shadow_color

    @shadow_color.setter
    def shadow_color(self, value: DesignToken) -> None:
        """Set the shadow color value."""
        if self._shadow_color == value:
            return
        self._shadow_color = value

        resolved_color = resolve_token(self._shadow_color)
        if not isinstance(resolved_color, QColor):
            raise RuntimeError(
                f"Unexpected shadow_color token value (expected QColor, got "
                f"{type(resolved_color).__name__})"
            )
        resolved_color.setAlphaF(0.3)
        self.setColor(resolved_color)
