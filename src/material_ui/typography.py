"""Typography module."""

from material_ui._component import Component, use_state
from qtpy.QtWidgets import QLabel
from typing import Literal, cast


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
    typescale = use_state(cast(Typescale, "body"))

    def __init__(
        self, *, text: str | None = None, typescale: Typescale | None = None
    ) -> None:
        super().__init__()

        if text is not None:
            self.text.set(text)
        if typescale is not None:
            self.typescale.set(typescale)

        self.sx.set({
            "font-size": "14px",
            "color": "black",
        })

        self._label = QLabel()
        self._label.setText(self.text.get())
        self.text.changed.connect(self._label.setText)
        self.overlay_widget(self._label)
