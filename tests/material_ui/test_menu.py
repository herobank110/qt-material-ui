from pytestqt.qtbot import QtBot

from material_ui.menu import Menu, MenuItem


def test_Menu_basic_api(qtbot: QtBot):
    menu = Menu()

    item1 = MenuItem()
    item1.text = "Item 1"
    item1.setParent(menu)

    qtbot.addWidget(menu)
