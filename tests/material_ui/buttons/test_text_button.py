from pytestqt.qtbot import QtBot

from material_ui.buttons import TextButton


def test_TextButton_basic_api(qtbot: QtBot):
    button = TextButton()
    button.text = "Hi"
    button.clicked.connect(lambda: None)
    qtbot.addWidget(button)
