"""File browser demo app."""

from material_ui._component import Component
from material_ui.layout_basics import Stack
from qtpy.QtCore import QMargins, Qt
from qtpy.QtWidgets import QApplication

FILE = object()

MOCK_FILE_SYSTEM = {
    "Pictures": {
        "Vacation": {
            "Beach": FILE,
            "Mountains": FILE,
        },
        "Birthday": FILE,
        "Wedding": FILE,
    },
    "Documents": {
        "Projects": {
            "Project 1": {
                "Report": FILE,
                "Presentation": FILE,
            },
        },
        "Resume": FILE,
    },
    "Music": {
        "Song1": FILE,
        "Song2": FILE,
        "Song3": FILE,
        "Song4": FILE,
    },
}


class FileBrowserApp(Component):
    def __init__(self) -> None:
        super().__init__()

        self.stack = Stack(
            alignment=Qt.AlignmentFlag.AlignTop,
            margins=QMargins(20, 20, 20, 20),
            gap=10,
        )


def main() -> None:
    app = QApplication()
    window = FileBrowserApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
