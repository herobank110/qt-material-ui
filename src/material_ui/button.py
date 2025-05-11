from typing import Literal, cast
from material_ui._lab import ElevationEffect
from material_ui.shape import Shape
from material_ui.tokens import md_comp_elevated_button as tokens
from material_ui._component import Component, effect, use_state
from material_ui.tokens._utils import resolve_token
from material_ui.typography import Typography
from qtpy import QtCore, QtGui, QtWidgets


ButtonVariant = Literal[
    "elevated",
    "filled",
    "filled-tonal",
    "outlined",
    "text",
]


class ElevatedButton(Component):
    """Buttons let people take action and make choices with one tap."""

    text = use_state("")
    variant = use_state(cast(ButtonVariant, "elevated"))

    hovered = use_state(False)
    pressed = use_state(False)

    # elevation = use_state(
    #     lambda self: elevated_tokens.hover_container_elevation if self.hovered else 0
    # )

    # _elevation = use_state(tokens.container_elevation)

    # @effect(hovered)
    # def elevation(self):
    #     if self.hovered:
    #         return tokens.hover_container_elevation
    #     return tokens.container_elevation

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
        self.setFixedSize(100, 50)

        self._container = Shape()
        self._container.corner_shape.set("full")
        self._container.sx.set(
            {
                "background-color": tokens.container_color,
                "padding": "8px 16px",
            }
        )
        self._container.setParent(self)
        self._container.move(5, 5)
        self._container.resize(self.size().shrunkBy(QtCore.QMargins(5, 5, 5, 5)))
        container_drop_shadow = ElevationEffect()
        container_drop_shadow.color = tokens.container_shadow_color
        container_drop_shadow.elevation = lambda: (
            tokens.hover_container_elevation
            if self.hovered
            else tokens.container_elevation
        )

        self._label = Typography()
        self._label.text.bind(self.text)
        self._label.sx.set(
            {
                "color": tokens.label_text_color,
                "font-size": tokens.label_text_size,
                "font-weight": tokens.label_text_weight,
            }
        )
        margins = QtCore.QMargins(24, 0, 24, 0)
        self.overlay_widget(self._label, margins)
