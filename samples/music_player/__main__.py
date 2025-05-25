"""Entry point."""

from app import MusicPlayerApp
from qtpy.QtWidgets import QApplication


def main() -> None:
    app = QApplication()
    window = MusicPlayerApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
