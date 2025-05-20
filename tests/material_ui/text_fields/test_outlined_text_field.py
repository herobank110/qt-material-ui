from pytestqt.qtbot import QtBot

from material_ui.text_fields import OutlinedTextField


def test_OutlinedTextField_basic_api(qtbot: QtBot):
    text_field = OutlinedTextField()
    text_field.label = "Label"
    text_field.value = "Value"
    qtbot.addWidget(text_field)
