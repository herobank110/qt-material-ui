from pytestqt.qtbot import QtBot

from material_ui.buttons import FilledButton


def test_FilledButton_basic_api(qtbot: QtBot):
    button = FilledButton()
    button.text = "Hi"

    def on_click() -> None:
        pass

    button.clicked.connect(on_click)
    qtbot.addWidget(button)
