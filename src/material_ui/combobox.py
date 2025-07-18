from typing import cast

from qtpy.QtCore import Qt

from material_ui._component import Component, effect, use_state
from material_ui.menu import Menu, MenuItem
from material_ui.text_fields.outlined_text_field import OutlinedTextField


class ComboBox(Component):
    """Select a string from multiple options."""

    label = use_state("")
    value = use_state("")
    items = use_state(cast("list[str]", []))

    def __init__(self) -> None:
        super().__init__()

        self._text_field = OutlinedTextField()
        # Don't let the textfield itself get focused.
        self._text_field.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._text_field._line_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._text_field._line_edit.setReadOnly(True)
        self._text_field.setCursor(Qt.CursorShape.PointingHandCursor)
        self._text_field._line_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        self._text_field.clicked.connect(lambda: self._show_menu())
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
        menu.open(anchor_widget=self._text_field)

    @effect(label)
    def _apply_label(self) -> None:
        self._text_field.label = self.label

    @effect(value)
    def _apply_value(self) -> None:
        self._text_field.value = self.value
