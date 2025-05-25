"""Main app component."""

from pathlib import Path

from material_ui._component import Component, effect, use_state
from material_ui.buttons.filled_button import FilledButton
from material_ui.icon import Icon
from material_ui.layout_basics import Row, Stack
from material_ui.shape import Shape
from material_ui.tokens import md_sys_color, md_sys_shape
from material_ui.typography import Typography
from qtpy.QtCore import QMargins, QPointF, Qt, QUrl
from qtpy.QtGui import QImage, QPainter, QPixmap, QRadialGradient
from qtpy.QtMultimedia import QAudioOutput, QMediaPlayer
from qtpy.QtWidgets import QLabel, QSizePolicy

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


class PlaybackControls(Component):
    def __init__(self) -> None:
        super().__init__()

        self.setMinimumWidth(290)

        background = Shape()
        background.corner_shape = md_sys_shape.corner_extra_large
        background.color = md_sys_color.surface_container

        stack = Stack(
            alignment=Qt.AlignmentFlag.AlignCenter,
            margins=QMargins(20, 20, 20, 20),
            gap=15,
        )

        track_name_label = Typography()
        track_name_label.variant = "title-medium"
        track_name_label.alignment = Qt.AlignmentFlag.AlignCenter
        track_name_label.text = "Track Name"
        stack.add_widget(track_name_label)

        buttons_row = Row()
        buttons_row.alignment = Qt.AlignmentFlag.AlignCenter
        buttons_row.gap = 30

        skip_previous_button = Icon()
        skip_previous_button.icon_name = "skip_previous"
        skip_previous_button.icon_style = "rounded"
        buttons_row.add_widget(skip_previous_button)

        play_pause_button = Icon()
        play_pause_button.icon_name = "play_arrow"
        play_pause_button.icon_style = "rounded"
        play_pause_button.filled = True
        buttons_row.add_widget(play_pause_button)

        skip_next_button = Icon()
        skip_next_button.icon_name = "skip_next"
        skip_next_button.icon_style = "rounded"
        buttons_row.add_widget(skip_next_button)

        stack.add_widget(buttons_row)

        seek_bar = Shape()
        seek_bar.color = md_sys_color.primary
        seek_bar.corner_shape = md_sys_shape.corner_full
        seek_bar.setFixedHeight(11)
        seek_bar.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        stack.add_widget(seek_bar)

        background.overlay_widget(stack)
        self.overlay_widget(background)


class MusicPlayerApp(Component):
    def __init__(self) -> None:
        super().__init__()
        # self.setMinimumSize(300, 400)
        self.sx = {"background-color": md_sys_color.background}

        stack = Stack(
            alignment=Qt.AlignmentFlag.AlignCenter,
            margins=QMargins(20, 20, 20, 20),
        )

        playback_controls = PlaybackControls()
        stack.add_widget(playback_controls)

        self.overlay_widget(stack)

        # title = Typography()
        # title.alignment = Qt.AlignmentFlag.AlignCenter
        # title.variant = "headline-medium"
        # title.text = "Music Player"
        # stack.add_widget(title)

        # image_label = QLabel()
        # image_label.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        # image_label.setFixedSize(200, 200)
        # image = QImage(200, 200, QImage.Format.Format_ARGB32_Premultiplied)
        # painter = QPainter(image)
        # painter.fillRect(image.rect(), "transparent")
        # grad = QRadialGradient(QPointF(100, 100), 100)
        # grad.setColorAt(0.0, "white")
        # grad.setColorAt(1.0, "black")
        # painter.setBrush(grad)
        # painter.drawEllipse(QPointF(100, 100), 100, 100)
        # painter.end()
        # image_label.setPixmap(QPixmap(image))
        # stack.add_widget(image_label)

        # play_button = FilledButton()
        # play_button.text = "Play"
        # stack.add_widget(play_button)

        # media_player = QMediaPlayer()
        # media_player.setParent(self)
        # audio_output = QAudioOutput()
        # audio_output.setParent(media_player)
        # print(audio_output.device().description())
        # media_player.setAudioOutput(audio_output)
        # media_player.setSource(QUrl("https://www.freecol.org/images/FreeCol-menu.ogg"))
        # media_player.hasAudioChanged.connect(
        #     lambda: print("hasAudioChanged", media_player.hasAudio())
        # )
        # audio_output.setVolume(100.0)
        # media_player.play()
