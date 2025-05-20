from pytestqt.qtbot import QtBot

from material_ui.buttons import FilledTonalButton


def test_FilledTonalButton_basic_api(qtbot: QtBot):
    button = FilledTonalButton()
    button.text = "Hi"
    button.clicked.connect(lambda: None)
    qtbot.addWidget(button)
