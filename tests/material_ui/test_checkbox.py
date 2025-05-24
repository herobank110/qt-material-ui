from pytestqt.qtbot import QtBot

from material_ui.checkbox import Checkbox


def test_Checkbox_basic_api(qtbot: QtBot):
    checkbox = Checkbox()
    checkbox.selected = True
    qtbot.addWidget(checkbox)
