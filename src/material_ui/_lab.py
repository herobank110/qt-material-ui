"""Experimental file for figuring things out."""

from material_ui.tokens._utils import DesignToken


class ElevationEffect:
    def __init__(self, color: DesignToken) -> None:
        shadow_color = resolve_token(tokens.container_shadow_color)
        shadow_color.setAlphaF(0.3)
        container_drop_shadow = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=resolve_token(tokens.container_elevation),
            color=shadow_color,
            offset=QtCore.QPointF(1, 1),
        )
