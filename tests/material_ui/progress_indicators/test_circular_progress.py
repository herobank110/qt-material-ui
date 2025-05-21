from pytestqt.qtbot import QtBot

from material_ui.progress_indicators import CircularProgress

# Taking a screenshot will cause the widget to be painted.


def test_CircularProgress_determinate_screenshot(qtbot: QtBot):
    progress_indicator = CircularProgress()
    progress_indicator.value = 0.5
    qtbot.addWidget(progress_indicator)
    assert qtbot.screenshot(progress_indicator) is not None


def test_CircularProgress_indeterminate_screenshot(qtbot: QtBot):
    progress_indicator = CircularProgress()
    progress_indicator.indeterminate = True
    qtbot.addWidget(progress_indicator)
    assert qtbot.screenshot(progress_indicator) is not None
