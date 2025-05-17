"""Material Icons (symbols)."""

from typing import cast, Literal
from material_ui._component import Component, effect, use_state
from material_ui._font_utils import install_default_fonts
from material_ui.tokens import md_sys_color
from qtpy.QtWidgets import QLabel
from qtpy.QtGui import QFont

# TODO: add all the icons...?
IconName = Literal[
    "star",
    "arrow_drop_down",
    "more_vert",
    "check",
    "close",
    "add",
]


IconStyle = Literal[
    "outlined",
    "rounded",
    "sharp",
]


class Icon(Component):
    """Material icon component."""

    icon_name = use_state(cast(IconName, "star"))
    icon_style = use_state(cast(IconStyle, "outlined"))
    color = use_state(md_sys_color.on_surface)

    def __init__(self) -> None:
        super().__init__()

        # Ensure fonts are installed (blocking!).
        install_default_fonts()

        self._label = QLabel()
        self.overlay_widget(self._label)

    @effect(color)
    def _apply_color(self) -> None:
        self.sx.set(lambda prev: prev | {"color": self.color.get()})

    @effect(icon_name)
    def _apply_icon_name(self):
        self._label.setText(self.icon_name.get())

    @effect(icon_style)
    def _apply_font(self):
        font = QFont(
            "Material Symbols " + self.icon_style.get().title(),
            pointSize=24,
            weight=400,
        )
        # font.setVariableAxis(QFont.Tag("FILL"), 1)
        # font.setVariableAxis(QFont.Tag("GRAD"), 200)
        self._label.setFont(font)
