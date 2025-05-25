"""Main app component."""

from material_ui._component import Component
from material_ui.buttons.filled_button import FilledButton
from material_ui.layout_basics import Stack
from material_ui.tokens import md_sys_color
from material_ui.typography import Typography
from qtpy.QtCore import Qt

"https://www.freecol.org/images/screen-1.0.0.jpg"


class MusicPlayerApp(Component):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(200, 400)
        self.sx = {"background-color": md_sys_color.background}

        stack = Stack(alignment=Qt.AlignmentFlag.AlignCenter)

        title = Typography()
        title.variant = "headline-medium"
        title.text = "Music Player"
        stack.add_widget(title)

        play_button = FilledButton()
        play_button.text = "Play"
        stack.add_widget(play_button)

        self.overlay_widget(stack)
