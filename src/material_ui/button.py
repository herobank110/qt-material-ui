from typing import Literal, cast
from material_ui._button_base import ButtonBase
from material_ui._component import Component, Signal, effect, use_state
from material_ui._elevated_button import ElevatedButton
from material_ui._filled_button import FilledButton


ButtonVariant = Literal[
    "elevated",
    "filled",
    "filled-tonal",
    "outlined",
    "text",
]


class Button(Component):
    """Buttons let"""

    clicked: Signal

    variant = use_state(cast(ButtonVariant, "elevated"))
    text = use_state("")

    _button_widget = use_state(cast(ButtonBase | None, None))

    @effect(variant)
    def _create_button_widget(self) -> None:
        """Create the button widget."""
        if self._button_widget.get() is not None:
            self._button_widget.get().deleteLater()
            self._button_widget.get().setParent(None)

        klass = {
            "elevated": ElevatedButton,
            "filled": FilledButton,
            # "filled-tonal": FilledTonalButton,
            # "outlined": OutlinedButton,
            # "text": TextButton,
        }[self.variant.get()]
        button = klass()
        button.text = self.text.get()
        button.clicked.connect(self.clicked)
        button.setParent(self)
        self._button_widget = button
