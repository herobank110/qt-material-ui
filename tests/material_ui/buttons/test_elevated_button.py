from pytestqt.qtbot import QtBot

from material_ui.buttons import ElevatedButton


def test_ElevatedButton_basic_api(qtbot: QtBot):
    button = ElevatedButton()
    button.text = "Hi"
    button.clicked.connect(lambda: None)
    qtbot.addWidget(button)
