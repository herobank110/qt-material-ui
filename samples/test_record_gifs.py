"""Record gifs for docs.

Importing pyautogui locally as it breaks CI. Even though the record_gif
tests are skipped, this module has be imported to discover tests.
"""

import time
from collections.abc import Callable, Generator
from threading import Thread

import pytest
from pytestqt.qtbot import QtBot

from sample_buttons import SampleButtons
from sample_checkbox import SampleCheckbox
from sample_text_fields import SampleTextFields


class Controller(Thread):
    """Play back pyautogui actions in a separate thread."""

    def __init__(self) -> None:
        super().__init__()
        self.movements: list[Callable[[], None]] = []
        self.kill = False

    def run(self) -> None:
        """Execute movements."""
        while not self.kill:
            time.sleep(0.001)
            if self.movements:
                for movement in self.movements:
                    movement()
                return


@pytest.fixture
def controller() -> Generator[Controller, None, None]:
    thread = Controller()
    thread.start()
    yield thread
    thread.kill = True


def wait(duration_secs: float) -> Callable[[], None]:
    return lambda: time.sleep(duration_secs)


def click() -> None:
    import pyautogui

    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()


def move_to(x: int, y: int, *, instant: bool = False) -> Callable[[], None]:
    import pyautogui

    return lambda: pyautogui.moveTo(
        x,
        y,
        duration=0 if instant else 0.5,
        tween=pyautogui.easeInOutQuad,  # pyright: ignore[reportUnknownArgumentType]
    )


def typewrite(string: str) -> Callable[[], None]:
    import pyautogui

    return lambda: pyautogui.typewrite(string, interval=0.1)


def keypress(key: str) -> Callable[[], None]:
    import pyautogui

    return lambda: pyautogui.press(key)


@pytest.mark.record_gif
def test_sample_buttons_gif(qtbot: QtBot, controller: Controller) -> None:
    window = SampleButtons()
    qtbot.addWidget(window)
    window.show()
    with qtbot.wait_exposed(window):
        dpr = window.devicePixelRatioF()
        x = int(window.x() * dpr)
        y = int((window.y() + window.height() / 2 + 30) * dpr)
        controller.movements = [
            move_to(x - 50, y, instant=True),
            wait(1.5),
            move_to(x + (115 * dpr), y),
            click,
            move_to(x + (240 * dpr), y),
            click,
            move_to(x + (355 * dpr), y),
            click,
            move_to(x + (475 * dpr), y),
            click,
            move_to(x + (595 * dpr), y),
            click,
            move_to(x + (750 * dpr), y),
        ]
        qtbot.wait(12000)


@pytest.mark.record_gif
def test_sample_text_fields_gif(qtbot: QtBot, controller: Controller) -> None:
    window = SampleTextFields()
    qtbot.addWidget(window)
    window.show()
    with qtbot.wait_exposed(window):
        dpr = window.devicePixelRatioF()
        x = int(window.x() * dpr)
        y = int((window.y() + window.height() / 2 + 30) * dpr)
        controller.movements = [
            move_to(x + 200 * dpr, y + 100 * dpr, instant=True),
            wait(3),
            move_to(x + 200 * dpr, y),
            click,
            typewrite("Hello"),
            wait(0.75),
            move_to(x + 350 * dpr, y),
            click,
            wait(0.5),
            typewrite("world"),
            wait(1),
            move_to(x + 350 * dpr, y + 100 * dpr),
        ]
        qtbot.wait(14000)


@pytest.mark.record_gif
def test_sample_checkbox_gif(qtbot: QtBot, controller: Controller) -> None:
    window = SampleCheckbox()
    qtbot.addWidget(window)
    window.show()
    with qtbot.wait_exposed(window):
        dpr = window.devicePixelRatioF()
        x = int(window.x() * dpr)
        y = int((window.y() + window.height() / 2 + 30) * dpr)
        controller.movements = [
            move_to(x + 142 * dpr, y + 100 * dpr, instant=True),
            wait(2),
            move_to(x + 142 * dpr, y + 5),
            click,
            wait(1.5),
            click,
            wait(0.75),
            move_to(x + 142 * dpr, y + 100 * dpr),
        ]
        qtbot.wait(12000)
