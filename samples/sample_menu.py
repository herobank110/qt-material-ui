"""Sample of using the menu component."""

from material_ui._component import Component
from material_ui.buttons import FilledButton
from material_ui.layout_basics import Row, Stack
from material_ui.menu import Menu
from qtpy.QtCore import QMargins, QPoint, Qt
from qtpy.QtWidgets import QApplication


class SampleMenu(Component):
    """Sample menu demonstration."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Menu Sample")
        self.resize(400, 300)  # Set up the main layout
        main_layout = Stack()
        main_layout.sx = {"background-color": "white"}
        main_layout.gap = 20
        main_layout.margins = QMargins(20, 20, 20, 20)
        self.overlay_widget(main_layout)

        # Create a row for the button
        button_row = Row()
        button_row.alignment = Qt.AlignmentFlag.AlignCenter
        main_layout.add_widget(button_row)

        # Create a button to open the menu
        self.menu_button = FilledButton()
        self.menu_button.text = "Open Menu"
        self.menu_button.clicked.connect(self._show_menu)
        button_row.add_widget(self.menu_button)

        # Create an information row
        info_row = Row()
        info_row.alignment = Qt.AlignmentFlag.AlignCenter
        main_layout.add_widget(info_row)

        # Selected item display
        self.selected_item = FilledButton()
        self.selected_item.text = "No selection"
        self.selected_item.setEnabled(False)
        info_row.add_widget(self.selected_item)

        # Create the menu
        self.menu = Menu()
        self.menu.items = ["Home", "Profile", "Settings", "Help", "About", "Logout"]
        self.menu.item_icons = ["home", "person", "settings", "help", "info", "logout"]
        self.menu.on_selection_change.connect(self._on_selection_change)

    def _show_menu(self) -> None:
        """Show the menu below the button."""
        # Calculate position below the button
        global_pos = self.menu_button.mapToGlobal(QPoint(0, self.menu_button.height()))
        self.menu.show_at(global_pos)

    def _on_selection_change(self, index: int) -> None:
        """Handle menu selection change."""
        if 0 <= index < len(self.menu.items):
            self.selected_item.text = f"Selected: {self.menu.items[index]}"
            print(f"Selected item: {self.menu.items[index]}")


def main() -> None:
    """Run the sample application."""
    app = QApplication()
    window = SampleMenu()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
