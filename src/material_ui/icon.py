"""Material Icons (symbols)."""

from typing import Literal, cast

from qtpy.QtCore import Qt
from qtpy.QtGui import QFont
from qtpy.QtWidgets import QLabel

from material_ui._component import Component, effect, use_state
from material_ui._font_utils import install_default_fonts
from material_ui.tokens import md_sys_color
from material_ui.tokens._utils import DesignToken, resolve_token_or_value

IconStyle = Literal[
    "outlined",
    "rounded",
    "sharp",
]


class Icon(Component):
    """Material icon component.

    Check here for available icons: https://fonts.google.com/icons
    """

    icon_name = use_state("star")
    icon_style = use_state(cast("IconStyle", "outlined"))
    font_size = use_state(cast("DesignToken | int", 24))
    color = use_state(md_sys_color.on_surface)
    filled = use_state(False)

    def __init__(self) -> None:
        super().__init__()

        # Ensure fonts are installed (blocking!).
        install_default_fonts()

        self._label = QLabel()
        self.overlay_widget(self._label)
        self.layout().setAlignment(Qt.AlignCenter)

    @effect(color)
    def _apply_color(self) -> None:
        self.sx = {**self.sx, "color": self.color}

    @effect(icon_name)
    def _apply_icon_name(self) -> None:
        self._label.setText(self.icon_name)

    @effect(icon_style, filled, font_size)
    def _apply_font(self) -> None:
        font = QFont(
            "Material Symbols " + self.icon_style.title(),
            pointSize=resolve_token_or_value(self.font_size),
            weight=400,
        )
        font.setVariableAxis(QFont.Tag("FILL"), 1 if self.filled else 0)
        # font.setVariableAxis(QFont.Tag("GRAD"), 200)
        self._label.setFont(font)
