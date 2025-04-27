from typing import Literal
from material_ui._component import Component


ButtonVariant = Literal[
    "elevated",
    "filled",
    "tonal",
    "outlined",
    "text",
]


class Button(Component):
    """Buttons let people take action and make choices with one tap."""

    def __init__(self, *, text: str = "") -> None:
        pass
