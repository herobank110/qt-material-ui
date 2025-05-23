from pytestqt.qtbot import QtBot

from material_ui.buttons import ElevatedButton


def test_ElevatedButton_basic_api(qtbot: QtBot):
    button = ElevatedButton()
    button.text = "Hi"

    def on_click() -> None:
        pass

    button.clicked.connect(on_click)
    qtbot.addWidget(button)
