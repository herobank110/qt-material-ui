"""Record gifs for docs.

Importing pyautogui locally as it breaks CI. Even though the record_gif
tests are skipped, this module has be imported to discover tests.
"""

import time
from collections.abc import Callable, Generator
from functools import partial
from threading import Thread

import pytest
from pytestqt.qtbot import QtBot

from sample_buttons import SampleButtons


class MousePlaybackThread(Thread):
    """Playback mouse movement coordinates."""

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
def mouse_playback() -> Generator[MousePlaybackThread, None, None]:
    thread = MousePlaybackThread()
    thread.start()
    yield thread
    thread.kill = True


def click() -> None:
    import pyautogui

    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()


def move_to(x: int, y: int, *, instant: bool = False) -> Callable[[], None]:
    import pyautogui

    return partial(
        pyautogui.moveTo,
        x,
        y,
        duration=0 if instant else 0.5,
        tween=pyautogui.easeInOutQuad,
    )


@pytest.mark.record_gif
def test_sample_buttons_gif(qtbot: QtBot, mouse_playback: MousePlaybackThread) -> None:
    """Test the sample buttons."""
    window = SampleButtons()
    qtbot.addWidget(window)
    window.show()
    with qtbot.wait_exposed(window):
        dpr = window.devicePixelRatioF()
        x = int(window.x() * dpr)
        y = int((window.y() + window.height() / 2 + 30) * dpr)
        mouse_playback.movements = [
            move_to(x - 50, y, instant=True),
            lambda: time.sleep(1.5),
            move_to(x + (120 * dpr), y),
            click,
            move_to(x + (240 * dpr), y),
            click,
            move_to(x + (350 * dpr), y),
            click,
            move_to(x + (470 * dpr), y),
            click,
            move_to(x + (590 * dpr), y),
            click,
            move_to(x + (750 * dpr), y),
        ]
        qtbot.wait(12000)
