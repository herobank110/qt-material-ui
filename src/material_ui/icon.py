"""Material Icons (symbols)."""

from typing import cast, Literal
from material_ui._component import Component, effect, use_state
from material_ui.tokens import md_sys_color
from qtpy.QtWidgets import QLabel

# TODO: add all the icons...?
IconName = Literal[
    "star",
    "arrow_drop_down",
    "more_vert",
    "check",
    "close",
    "add",
]


class Icon(Component):
    """Material icon component."""

    icon_name = use_state(cast(IconName, "star"))
    color = use_state(md_sys_color.on_surface)

    def __init__(self) -> None:
        super().__init__()

        self._label = QLabel()
        self.overlay_widget(self._label)

    @effect(color)
    def _apply_color(self) -> None:
        self.sx.set(lambda prev: prev | {"color": self.color.get()})

    @effect(icon_name)
    def _apply_icon_name(self):
        self._label.setText(self.icon_name.get())
