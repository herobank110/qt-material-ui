"""Record gifs for docs."""

import time
from collections.abc import Callable, Generator
from threading import Thread

import pyautogui
import pytest
from pytestqt.qtbot import QtBot
from qtpy.QtCore import QPoint

from sample_buttons import SampleButtons


class MousePlaybackThread(Thread):
    """Playback mouse movement coordinates."""

    def __init__(self) -> None:
        super().__init__()
        self.window_pos = QPoint()
        self.movements = []
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
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.mouseUp()


def move_to(x: int, y: int, duration: float = 0.5) -> Callable[[], None]:
    def inner():
        pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)

    return inner


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
            move_to(x - 50, y, duration=0),
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
