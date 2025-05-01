from typing import Literal, cast
from material_ui._component import Component, use_state
from material_ui.typography import Typography


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
                "background-color": "red",
                "border-radius": "8px",
                "padding": "8px 16px",
                "border": "none",
            }
        )

        self._label = Typography()
        self._label.text.bind(self.text)
        self.overlay_widget(self._label)
