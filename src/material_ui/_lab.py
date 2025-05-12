"""Experimental file for figuring things out."""

from material_ui.tokens import DesignToken, resolve_token
from qtpy.QtWidgets import QGraphicsDropShadowEffect
from qtpy.QtGui import QColor
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

        self.setBlurRadius(resolve_token(self._elevation))
        self.setOffset(0, resolve_token(self._elevation) / 2)

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
