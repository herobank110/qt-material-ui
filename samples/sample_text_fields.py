"""Sample usage of Text Field components."""

from material_ui import Component
from material_ui.icon import Icon
from material_ui.layout_basics import Row
from material_ui.text_fields import FilledTextField, OutlinedTextField
from material_ui.tokens import md_sys_color
from qtpy.QtCore import QMargins
from qtpy.QtWidgets import QApplication


class SampleTextFields(Component):
    """Sample usage of Text Field components."""

    def __init__(self) -> None:
        super().__init__()

        self.sx = {"background-color": md_sys_color.background}

        row = Row()
        row.gap = 30
        row.margins = QMargins(40, 30, 40, 30)
        self.overlay_widget(row)

        filled = FilledTextField()
        filled.label = "Filled"
        filled.value = ""
        row.add_widget(filled)

        outlined = OutlinedTextField()
        outlined.label = "Outlined"
        outlined.value = ""
        row.add_widget(outlined)

        # Add text fields with trailing icons
        filled_with_icon = FilledTextField()
        filled_with_icon.label = "Search"
        filled_with_icon.value = ""
        
        search_icon = Icon()
        search_icon.icon_name = "search"
        filled_with_icon.trailing_icon = search_icon
        row.add_widget(filled_with_icon)

        outlined_with_icon = OutlinedTextField()
        outlined_with_icon.label = "Clear"
        outlined_with_icon.value = ""
        
        clear_icon = Icon()
        clear_icon.icon_name = "clear"
        outlined_with_icon.trailing_icon = clear_icon
        row.add_widget(outlined_with_icon)

        # Take the initial focus away from the first text field.
        self.setFocus()
        # Steal focus when the empty area is clicked.
        self.clicked.connect(lambda: self.setFocus())


def main() -> None:
    app = QApplication()
    window = SampleTextFields()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
