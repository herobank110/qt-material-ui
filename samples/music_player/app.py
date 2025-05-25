"""Main app component."""

from pathlib import Path

from material_ui._component import Component, effect, use_state
from material_ui.buttons.filled_button import FilledButton
from material_ui.layout_basics import Stack
from material_ui.tokens import md_sys_color
from material_ui.typography import Typography
from qtpy.QtCore import QPointF, Qt, QUrl
from qtpy.QtGui import QImage, QPainter, QPixmap, QRadialGradient
from qtpy.QtMultimedia import QAudioOutput, QMediaPlayer
from qtpy.QtWidgets import QLabel

songs = [
    "https://www.freecol.org/images/fearless-sailors.ogg",
    "https://www.freecol.org/images/founders.ogg",
    "https://www.freecol.org/images/settlers-routine.ogg",
    "https://www.freecol.org/images/sunrise.ogg",
    "https://www.freecol.org/images/tailwind.ogg",
    "https://www.freecol.org/images/musicbox.ogg",
    "https://www.freecol.org/images/FreeCol-opening.ogg",
    "https://www.freecol.org/images/FreeCol-menu.ogg",
]


class MusicPlayerApp(Component):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumSize(300, 400)
        self.sx = {"background-color": md_sys_color.background}

        stack = Stack(alignment=Qt.AlignmentFlag.AlignCenter)

        title = Typography()
        title.alignment = Qt.AlignmentFlag.AlignCenter
        title.variant = "headline-medium"
        title.text = "Music Player"
        stack.add_widget(title)

        image_label = QLabel()
        image_label.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        image_label.setFixedSize(200, 200)
        image = QImage(200, 200, QImage.Format.Format_ARGB32_Premultiplied)
        painter = QPainter(image)
        painter.fillRect(image.rect(), "transparent")
        grad = QRadialGradient(QPointF(100, 100), 100)
        grad.setColorAt(0.0, "white")
        grad.setColorAt(1.0, "black")
        painter.setBrush(grad)
        painter.drawEllipse(QPointF(100, 100), 100, 100)
        painter.end()
        image_label.setPixmap(QPixmap(image))
        stack.add_widget(image_label)

        play_button = FilledButton()
        play_button.text = "Play"
        stack.add_widget(play_button)

        self.overlay_widget(stack)

        media_player = QMediaPlayer()
        media_player.setParent(self)
        audio_output = QAudioOutput()
        audio_output.setParent(media_player)
        print(audio_output.device().description())
        media_player.setAudioOutput(audio_output)
        media_player.setSource(QUrl("https://www.freecol.org/images/FreeCol-menu.ogg"))
        media_player.hasAudioChanged.connect(
            lambda: print("hasAudioChanged", media_player.hasAudio())
        )
        audio_output.setVolume(100.0)
        media_player.play()
