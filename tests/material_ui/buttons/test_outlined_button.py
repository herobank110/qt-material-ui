from pytestqt.qtbot import QtBot

from material_ui.buttons import OutlinedButton


def test_OutlinedButton_basic_api(qtbot: QtBot):
    button = OutlinedButton()
    button.text = "Hi"

    def on_click() -> None:
        pass

    button.clicked.connect(on_click)
    qtbot.addWidget(button)
