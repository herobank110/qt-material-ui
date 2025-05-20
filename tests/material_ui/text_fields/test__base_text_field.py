from pytest_mock import MockerFixture
from pytestqt.qtbot import QtBot
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QSizePolicy

from material_ui.text_fields._base_text_field import BaseTextField


def test_BaseTextField_value_set_from_typing(qtbot: QtBot):
    text_field = BaseTextField()
    qtbot.addWidget(text_field)
    # QTest doesn't seem to support focus, so type the text directly on
    # the line edit.
    qtbot.keyClicks(text_field._line_edit, "Hello")
    assert text_field.value == "Hello"


def test_BaseTextField_click_to_focus(qtbot: QtBot, mocker: MockerFixture):
    text_field = BaseTextField()
    qtbot.addWidget(text_field)
    # Assume the focus is propagated correctly if setFocus is called.
    spy = mocker.spy(text_field, "setFocus")
    qtbot.mouseClick(text_field, Qt.MouseButton.LeftButton)
    assert spy.called


def test_BaseTextField_size_hint(qtbot: QtBot):
    text_field = BaseTextField()
    text_field.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    qtbot.addWidget(text_field)
    size_hint = text_field.sizeHint()
    assert 190 < size_hint.width() < 210
    assert 40 < size_hint.height() < 70
