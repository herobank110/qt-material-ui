"""File browser demo app."""

from functools import reduce
from pathlib import Path
from typing import Any

from material_ui._component import Component, Signal, effect, use_state
from material_ui.buttons.text_button import TextButton
from material_ui.layout_basics import Stack
from material_ui.tokens import md_sys_color
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


class DirectoryItem(Component):
    """A component representing a directory item in the file browser."""

    label = use_state("")
    on_click: Signal

    def __init__(self) -> None:
        super().__init__()
        self._button = TextButton()
        self._button.clicked.connect(self.on_click)
        self.overlay_widget(self._button)

    @effect(label)
    def _apply_label(self) -> None:
        self._button.text = self.label


class FileBrowserApp(Component):
    current_path = use_state(Path())

    def __init__(self) -> None:
        super().__init__()

        self.resize(300, 400)
        self.sx = {"background-color": md_sys_color.background}

        self.stack = Stack(
            alignment=Qt.AlignmentFlag.AlignTop,
            margins=QMargins(20, 20, 20, 20),
            gap=3,
        )
        self.overlay_widget(self.stack)

    @effect(current_path)
    def _apply_directory_listing(self) -> None:
        # Delete previous items.
        prev_children = self.stack.findChildren(
            DirectoryItem,
            options=Qt.FindChildOption.FindDirectChildrenOnly,
        )
        for child in prev_children:
            child.setParent(None)
        # Create .. item to go up one directory.
        if self.current_path != Path():
            parent_path = self.current_path.parent
            item = DirectoryItem()
            item.label = ".."
            item.on_click.connect(lambda: self.set_state("current_path", parent_path))
            self.stack.add_widget(item)
        # Create new items.
        for path in listdir(self.current_path):
            item = DirectoryItem()
            item.label = path.name
            if not isfile(path):
                item.on_click.connect(lambda p=path: self.set_state("current_path", p))
            self.stack.add_widget(item)


def listdir(path: Path) -> list[Path]:
    """List directory contents as concatenated paths."""
    current: dict[str, Any] = MOCK_FILE_SYSTEM
    for part in path.parts:
        if (maybe_next := current[part]) is not FILE:
            current = maybe_next
    return [path / x for x in current]


def isfile(path: Path) -> bool:
    """Check if the path is a file."""
    return reduce(lambda x, y: x[y], path.parts, MOCK_FILE_SYSTEM) is FILE


def test_file_system() -> None:
    assert listdir(Path("Pictures")) == [
        Path("Pictures/Vacation"),
        Path("Pictures/Birthday"),
        Path("Pictures/Wedding"),
    ]
    assert isfile(Path("Pictures/Vacation/Beach"))
    assert not isfile(Path("Pictures/Vacation"))
    assert listdir(Path("Documents/Projects/Project 1")) == [
        Path("Documents/Projects/Project 1/Report"),
        Path("Documents/Projects/Project 1/Presentation"),
    ]


def main() -> None:
    app = QApplication()
    window = FileBrowserApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
    # test_file_system()
