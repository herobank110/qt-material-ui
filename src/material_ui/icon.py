"""Material Icons (symbols)."""

from typing import Literal, cast

from qtpy.QtGui import QColor, QFont
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
    """Icon name to display. See: https://fonts.google.com/icons."""

    icon_style = use_state(cast("IconStyle", "outlined"))
    """Icon style. Either 'outlined', 'rounded', or 'sharp'."""

    font_size = use_state(cast("DesignToken | int", 24))
    """Font size of icon."""

    color = use_state(cast("DesignToken | QColor", md_sys_color.on_surface))
    """Color of the icon."""

    weight = use_state(400)
    """Main control of thickness. 400 is default, 100 is thin, 700 is thick."""

    filled = use_state(False)
    """Whether the icon should be filled."""

    grade = use_state(0)
    """Thickness. 0 is default, -25 is thin, 200 is thick."""

    use_optical_size = use_state(True)
    """Whether to set the optical size to match the font size."""

    def __init__(self) -> None:
        super().__init__()

        # Ensure fonts are installed (blocking!).
        install_default_fonts()

        self._label = QLabel()
        self.overlay_widget(self._label, center=True)

    @effect(color)
    def _apply_color(self) -> None:
        self.sx = {**self.sx, "color": resolve_token_or_value(self.color)}

    @effect(icon_name)
    def _apply_icon_name(self) -> None:
        self._label.setText(self.icon_name)

    @effect(icon_style, filled, font_size, weight, grade, use_optical_size)
    def _apply_font(self) -> None:
        font_size = resolve_token_or_value(self.font_size)
        font = QFont("Material Symbols " + self.icon_style.title())
        font.setPixelSize(font_size)
        font.setVariableAxis(QFont.Tag("FILL"), 1 if self.filled else 0)
        font.setVariableAxis(QFont.Tag("wght"), self.weight)
        font.setVariableAxis(QFont.Tag("GRAD"), self.grade)
        optical_size = font_size if self.use_optical_size else 24
        font.setVariableAxis(QFont.Tag("opsz"), optical_size)
        self._label.setFont(font)
