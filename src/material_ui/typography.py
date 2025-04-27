"""Typography module."""

from material_ui._component import Component
from qtpy.QtWidgets import QLabel
from typing import Literal


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

    def __init__(self, *, text: str = "", typescale: Typescale = "body") -> None:
        super().__init__()

        qt_label = QLabel(text)
        # qt_label.setStyleSheet()
        self.overlay_widget(qt_label)
