"""Sample of using the menu component."""

from material_ui._component import Component, effect, use_state
from material_ui.buttons import FilledButton
from material_ui.layout_basics import Stack
from material_ui.menu import Menu, MenuItem
from material_ui.tokens import md_sys_color
from material_ui.typography import Typography
from qtpy.QtCore import QMargins, Qt
from qtpy.QtWidgets import QApplication


class SampleMenu(Component):
    selected_item = use_state("")

    def __init__(self) -> None:
        super().__init__()
        self.sx = {"background-color": md_sys_color.background}

        stack = Stack()
        stack.gap = 20
        stack.margins = QMargins(40, 40, 40, 40)
        stack.alignment = Qt.AlignmentFlag.AlignCenter
        self.overlay_widget(stack)

        self._show_menu_button = FilledButton()
        self._show_menu_button.text = "Open Menu"
        self._show_menu_button.clicked.connect(self._on_click_show_menu_button)
        stack.add_widget(self._show_menu_button)

        self._selected_label = Typography()
        self._selected_label.alignment = Qt.AlignmentFlag.AlignCenter
        stack.add_widget(self._selected_label)

    def _on_click_show_menu_button(self) -> None:
        menu = Menu()

        item1 = MenuItem()
        item1.text = "Item 1"
        item1.clicked.connect(self._on_click_item1)
        item1.setParent(menu)

        item2 = MenuItem()
        item2.text = "Item 2"
        item2.clicked.connect(self._on_click_item2)
        item2.setParent(menu)

        item3 = MenuItem()
        item3.text = "Item 3"
        item3.clicked.connect(self._on_click_item3)
        item3.setParent(menu)

        menu.open(anchor_widget=self._show_menu_button)

    def _on_click_item1(self) -> None:
        self.selected_item = "Item 1"

    def _on_click_item2(self) -> None:
        self.selected_item = "Item 2"

    def _on_click_item3(self) -> None:
        self.selected_item = "Item 3"

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
