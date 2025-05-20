from pytestqt.qtbot import QtBot

from material_ui.buttons import FilledButton


def test_FilledButton_basic_api(qtbot: QtBot):
    button = FilledButton()
    button.text = "Hi"
    button.clicked.connect(lambda: None)
    qtbot.addWidget(button)
