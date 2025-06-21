"""Sample of using the menu component."""

from material_ui._component import Component, effect, use_state
from material_ui.buttons import FilledButton
from material_ui.layout_basics import Stack
from material_ui.menu import Menu
from material_ui.tokens import md_sys_color
from material_ui.typography import Typography
from qtpy.QtCore import QMargins, QPoint, Qt
from qtpy.QtWidgets import QApplication


class SampleMenu(Component):
    selected_item = use_state("")

    def __init__(self) -> None:
        super().__init__()
        self.sx = {"background-color": md_sys_color.background}

        stack = Stack()
        stack.gap = 20
        stack.margins = QMargins(20, 20, 20, 20)
        stack.alignment = Qt.AlignmentFlag.AlignCenter
        self.overlay_widget(stack)

        self._menu_button = FilledButton()
        self._menu_button.text = "Open Menu"
        self._menu_button.clicked.connect(self._show_menu)
        stack.add_widget(self._menu_button)

        self._selected_label = Typography()
        stack.add_widget(self._selected_label)

        # Create the menu
        self.menu = Menu()
        self.menu.items = ["Home", "Profile", "Settings", "Help", "About", "Logout"]
        self.menu.item_icons = ["home", "person", "settings", "help", "info", "logout"]
        self.menu.on_selection_change.connect(self._on_selection_change)

    def _show_menu(self) -> None:
        """Show the menu below the button."""
        # Calculate position below the button
        global_pos = self._menu_button.mapToGlobal(
            QPoint(0, self._menu_button.height()),
        )
        self.menu.show_at(global_pos)

    def _on_selection_change(self, index: int) -> None:
        """Handle menu selection change."""
        if 0 <= index < len(self.menu.items):
            self.selected_item = self.menu.items[index]
            print(f"Selected item: {self.menu.items[index]}")

    @effect(selected_item)
    def _apply_selected_label_text(self) -> None:
        new_text = (
            "No selection"
            if not self.selected_item
            else f"Selected: {self.selected_item}"
        )
        self._selected_label.text = new_text


def main() -> None:
    app = QApplication()
    window = SampleMenu()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
