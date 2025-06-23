from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot
from qtpy.QtCore import Qt

from material_ui.icon import Icon
from material_ui.menu import Menu, MenuItem


def test_Menu_clicking_item_closes_menu(qtbot: QtBot, mocker: MockerFixture):
    menu = Menu()
    qtbot.addWidget(menu)

    item1 = MenuItem()
    item1.text = "Item"
    item1.setParent(menu)

    menu.open(menu)

    close_menu_spy = mocker.spy(menu, "close_menu")
    qtbot.mouseClick(item1, Qt.MouseButton.LeftButton)
    qtbot.wait_until(lambda: close_menu_spy.call_count == 1, timeout=100)


def test_MenuItem_with_icon(qtbot: QtBot):
    item = MenuItem()
    item.text = "Item"
    icon = Icon()
    icon.icon_name = "check"
    item.leading_icon = icon
    assert item._leading_icon_wrapper.findChild(Icon) is not None
    qtbot.addWidget(item)


def test_MenuItem_with_icon_then_none(qtbot: QtBot):
    item = MenuItem()
    item.text = "Item"
    icon = Icon()
    icon.icon_name = "check"
    item.leading_icon = icon
    assert item._leading_icon_wrapper.findChild(Icon) is not None
    item.leading_icon = None
    assert item._leading_icon_wrapper.findChild(Icon) is None
    qtbot.addWidget(item)
