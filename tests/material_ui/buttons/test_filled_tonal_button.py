from pytestqt.qtbot import QtBot

from material_ui.buttons import FilledTonalButton


def test_FilledTonalButton_basic_api(qtbot: QtBot):
    button = FilledTonalButton()
    button.text = "Hi"

    def on_click() -> None:
        pass

    button.clicked.connect(on_click)
    qtbot.addWidget(button)
