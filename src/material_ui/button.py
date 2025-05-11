from typing import Literal, cast
from material_ui.shape import Shape
from material_ui.tokens import md_comp_elevated_button as elevated_tokens
from material_ui._component import Component, use_state
from material_ui.typography import Typography
from qtpy import QtCore


ButtonVariant = Literal[
    "elevated",
    "filled",
    "filled-tonal",
    "outlined",
    "text",
]


class Button(Component):
    """Buttons let people take action and make choices with one tap."""

    text = use_state("")
    variant = use_state(cast(ButtonVariant, "elevated"))

    def __init__(self) -> None:
        super().__init__()

        self.sx.set(
            {
        #         "background-color": elevated_tokens.container_color,
        #         "border-radius": "8px",
                "padding": "8px 16px",
        #         "border": "none",
            }
        )
        self.setFixedHeight(40)

        self._container = Shape()
        self._container.corner_shape.set("full")
        self._container.sx.set({
            "background-color": elevated_tokens.container_color,
            "padding": "8px 16px",
        })
        self._container.setParent(self)
        self._container.resize(self.size())
        # self._container.resize(80, 40)
        # self.overlay_widget(self._container)

        self._label = Typography()
        self._label.text.bind(self.text)
        self._label.sx.set({
            "color": elevated_tokens.label_text_color,
            "font-size": elevated_tokens.label_text_size,
            "font-weight": elevated_tokens.label_text_weight,
        })
        margins = QtCore.QMargins(24, 0, 24, 0)
        self.overlay_widget(self._label, margins)
