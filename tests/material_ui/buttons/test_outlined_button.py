from pytestqt.qtbot import QtBot

from material_ui.buttons import OutlinedButton


def test_OutlinedButton_basic_api(qtbot: QtBot):
    button = OutlinedButton()
    button.text = "Hi"
    button.clicked.connect(lambda: None)
    qtbot.addWidget(button)
