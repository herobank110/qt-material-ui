from pytestqt.qtbot import QtBot

from material_ui.text_fields import FilledTextField


def test_FilledTextField_basic_api(qtbot: QtBot):
    text_field = FilledTextField()
    text_field.label = "Label"
    text_field.value = "Value"
    qtbot.addWidget(text_field)
