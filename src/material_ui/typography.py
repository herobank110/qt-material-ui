"""Typography module."""

from material_ui._widget import Widget
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


class Typography(Widget):
    """Typography helps make writing legible and beautiful."""

    def __init__(self, *, text: str = "", typescale: Typescale = "body") -> None:
        super().__init__()

        self.text = self.add_state(text)
        """The text to display."""

        self.typescale = self.add_state(typescale)
        """Typescale class to use. Exact styling can be configured in the theme."""

        qt_label = QLabel(self.text.get())
        self.text.changed.connect(self._label.setText)
        self.overlay_widget(qt_label)
