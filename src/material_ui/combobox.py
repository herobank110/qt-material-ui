from typing import cast

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QSizePolicy

from material_ui._component import Component, Signal, effect, use_state
from material_ui.menu import Menu, MenuItem
from material_ui.text_fields.outlined_text_field import OutlinedTextField


class ComboBox(Component):
    """Select a string from multiple options."""

    label = use_state("")
    """Label for the textfield of the combobox."""

    value = use_state("")
    """Currently selected value."""

    items = use_state(cast("list[str]", []))
    """List of items to select from."""

    on_change: Signal[str]
    """Called when the value is changed."""

    def __init__(self) -> None:
        super().__init__()

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.clicked.connect(self._show_menu)

        self._text_field = OutlinedTextField()
        # TODO: trailing icon
        # drop_down_icon = Icon()
        # drop_down_icon.icon_name = "arrow_drop_down"
        # self._text_field.trailing_icon = drop_down_icon
        # Don't let the textfield itself get focused.
        self._text_field.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            on=True,
        )
        self._text_field.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.overlay_widget(self._text_field)

    def _show_menu(self) -> None:
        """Open the selection menu."""
        menu = Menu()
        for item_text in self.items:
            menu_item = MenuItem()
            menu_item.text = item_text
            menu_item.clicked.connect(
                lambda text=item_text: self.set_state("value", text),
            )
            menu_item.setParent(menu)
        menu.open(anchor_widget=self._text_field, stretch_width=True)

    @effect(label)
    def _apply_label(self) -> None:
        self._text_field.label = self.label

    @effect(value)
    def _apply_value(self) -> None:
        self._text_field.value = self.value

    @effect(Component.hovered)
    def _propagate_hovered(self) -> None:
        # Forward the hover state manually because we made it
        # transparent for mouse events.
        self._text_field.hovered = self.hovered
