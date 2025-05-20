from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QSizePolicy

from material_ui.buttons._button_base import ButtonBase


def test_ButtonBase_click_is_fired(qtbot: QtBot, mocker: MockerFixture):
    click_stub = mocker.stub()
    button = ButtonBase()
    button.clicked.connect(click_stub)
    qtbot.addWidget(button)
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    assert click_stub.call_count == 1


def test_ButtonBase_click_right_click_does_nothing(qtbot: QtBot, mocker: MockerFixture):
    click_stub = mocker.stub()
    button = ButtonBase()
    button.clicked.connect(click_stub)
    qtbot.addWidget(button)
    qtbot.mouseClick(button, Qt.MouseButton.RightButton)
    assert click_stub.call_count == 0


def test_ButtonBase_hovered(qtbot: QtBot):
    button = ButtonBase()
    qtbot.addWidget(button)
    c1 = button._state_layer.color
    button.hovered = True
    c2 = button._state_layer.color
    assert c1 != c2


def test_ButtonBase_size_hint_with_texts(qtbot: QtBot):
    button = ButtonBase()
    button.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    button.text = "Hello world"
    qtbot.addWidget(button)
    size_hint = button.sizeHint()
    assert 100 < size_hint.width() < 130
    assert 40 < size_hint.height() < 70

    button.text = "Hi"
    qtbot.wait(1)
    size_hint2 = button.sizeHint()
    # Shorter text should be narrower.
    assert size_hint2.width() < size_hint.width()
