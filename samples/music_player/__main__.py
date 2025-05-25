"""Entry point."""

from app import MusicPlayerApp
from qtpy.QtWidgets import QApplication


def main() -> None:
    from PySide6 import QtAsyncio
    app = QApplication()
    window = MusicPlayerApp()
    window.show()
    QtAsyncio.run()
    # app.exec()


if __name__ == "__main__":
    main()
