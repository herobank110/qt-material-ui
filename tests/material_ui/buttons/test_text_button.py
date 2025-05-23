from pytestqt.qtbot import QtBot

from material_ui.buttons import TextButton


def test_TextButton_basic_api(qtbot: QtBot):
    button = TextButton()
    button.text = "Hi"

    def on_click() -> None:
        pass

    button.clicked.connect(on_click)
    qtbot.addWidget(button)
