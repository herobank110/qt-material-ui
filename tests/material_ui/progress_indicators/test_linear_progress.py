from pytestqt.qtbot import QtBot

from material_ui.progress_indicators import LinearProgress

# Taking a screenshot will cause the widget to be painted.


def test_LinearProgress_determinate_screenshot(qtbot: QtBot):
    progress_indicator = LinearProgress()
    progress_indicator.value = 0.5
    qtbot.addWidget(progress_indicator)
    assert qtbot.screenshot(progress_indicator) is not None


def test_LinearProgress_indeterminate_screenshot(qtbot: QtBot):
    progress_indicator = LinearProgress()
    progress_indicator.indeterminate = True
    qtbot.addWidget(progress_indicator)
    assert qtbot.screenshot(progress_indicator) is not None
