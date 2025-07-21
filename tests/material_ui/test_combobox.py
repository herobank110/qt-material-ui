from pytestqt.qtbot import QtBot

from material_ui.combobox import ComboBox


def test_ComboBox_basic_api(qtbot: QtBot):
    combo = ComboBox()
    combo.items = ["Option 1", "Option 2", "Option 3"]
    combo.label = "Select an option"
    qtbot.addWidget(combo)
