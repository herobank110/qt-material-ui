"""Typography module."""

from typing import Literal, cast

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel

from material_ui._component import Component, effect, use_state
from material_ui.tokens import md_sys_typescale

Typescale = Literal[
    "display",
    "display-small",
    "display-medium",
    "display-large",
    "headline",
    "headline-small",
    "headline-medium",
    "headline-large",
    "title",
    "title-small",
    "title-medium",
    "title-large",
    "body",
    "body-small",
    "body-medium",
    "body-large",
    "label",
    "label-small",
    "label-medium",
    "label-large",
]


class Typography(Component):
    """Typography helps make writing legible and beautiful."""

    text = use_state("")
    typescale = use_state(cast("Typescale", "body"))
    alignment = use_state(cast("Qt.AlignmentFlag", Qt.AlignmentFlag()))  # type: ignore[call-arg]

    def __init__(
        self,
        *,
        text: str | None = None,
        typescale: Typescale | None = None,
    ) -> None:
        super().__init__()

        if text:
            self.text = text
        if typescale:
            self.typescale = typescale

        self.sx = {
            "font-size": md_sys_typescale.body_medium_size,
            "color": "black",
        }

        self._label = QLabel()
        self.overlay_widget(self._label)

    @effect(alignment)
    def _apply_alignment(self) -> None:
        self._label.setAlignment(self.alignment)

    @effect(text)
    def _apply_text(self) -> None:
        self._label.setText(self.text)
