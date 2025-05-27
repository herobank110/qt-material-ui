"""Main app component."""

from material_ui._component import Component, Signal, effect, use_state
from material_ui.icon import Icon
from material_ui.layout_basics import Row, Stack
from material_ui.progress_indicators.linear_progress import LinearProgress
from material_ui.shape import Shape
from material_ui.tokens import md_sys_color, md_sys_shape
from material_ui.typography import Typography
from qtpy.QtCore import QMargins, Qt, QTimer
from qtpy.QtMultimedia import QAudioOutput, QMediaPlayer
from qtpy.QtWidgets import QApplication, QSizePolicy

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
    on_click_skip_previous: Signal
    on_click_skip_next: Signal
    on_click_play_pause: Signal
    is_playing = use_state(False)
    is_loading = use_state(False)

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

        self._track_name_label = Typography()
        self._track_name_label.variant = "title-medium"
        self._track_name_label.alignment = Qt.AlignmentFlag.AlignCenter
        self._track_name_label.text = "Track Name"
        stack.add_widget(self._track_name_label)

        buttons_row = Row()
        buttons_row.alignment = Qt.AlignmentFlag.AlignCenter
        buttons_row.gap = 30

        self._skip_previous_button = Icon()
        self._skip_previous_button.icon_name = "skip_previous"
        self._skip_previous_button.clicked.connect(self.on_click_skip_previous)
        buttons_row.add_widget(self._skip_previous_button)

        self._play_pause_button = Icon()
        self._play_pause_button.clicked.connect(self.on_click_play_pause)
        buttons_row.add_widget(self._play_pause_button)

        self._skip_next_button = Icon()
        self._skip_next_button.icon_name = "skip_next"
        self._skip_next_button.clicked.connect(self.on_click_skip_next)
        buttons_row.add_widget(self._skip_next_button)

        stack.add_widget(buttons_row)

        self._seek_bar = Shape()
        self._seek_bar.color = md_sys_color.primary
        self._seek_bar.corner_shape = md_sys_shape.corner_full
        self._seek_bar.setFixedHeight(11)
        self._seek_bar.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )
        stack.add_widget(self._seek_bar)

        self._loading_bar = LinearProgress()
        self._loading_bar.indeterminate = True
        stack.add_widget(self._loading_bar)

        background.overlay_widget(stack)
        self.overlay_widget(background)

    @effect(is_loading)
    def _apply_loading_state(self) -> None:
        if self.is_loading:
            self._seek_bar.visible = False
            self._loading_bar.show()
        else:
            self._seek_bar.visible = True
            self._loading_bar.hide()

    @effect(is_playing)
    def _apply_play_pause_icon(self) -> None:
        if self.is_playing:
            self._play_pause_button.icon_name = "pause"
        else:
            self._play_pause_button.icon_name = "play_arrow"


class MusicPlayerApp(Component):
    _is_playing = use_state(False)
    _is_loading = use_state(False)
    _active_song_index = use_state(0)

    def __init__(self) -> None:
        super().__init__()
        self.sx = {"background-color": md_sys_color.background}

        stack = Stack(
            alignment=Qt.AlignmentFlag.AlignCenter,
            margins=QMargins(20, 20, 20, 20),
        )

        playback_controls = PlaybackControls()
        playback_controls.is_playing = self._is_playing
        playback_controls.is_loading = self._is_loading
        playback_controls.on_click_skip_previous.connect(self._skip_previous)
        playback_controls.on_click_skip_next.connect(self._skip_next)
        playback_controls.on_click_play_pause.connect(self._toggle_play_pause)
        stack.add_widget(playback_controls)

        self.overlay_widget(stack)

        self._media_player = QMediaPlayer()
        self._media_player.setParent(self)
        audio_output = QAudioOutput()
        audio_output.setParent(self._media_player)
        audio_output.setVolume(100.0)
        self._media_player.setAudioOutput(audio_output)
        self._media_player.mediaStatusChanged.connect(
            self._on_media_player_media_status_changed,
        )

    def _on_media_player_media_status_changed(
        self,
        status: QMediaPlayer.MediaStatus,
    ) -> None:
        # Qt emits a LoadedMedia status with the old source when
        # switching sources - filter these events out.
        is_correct_song = (
            self._media_player.source().toString() == songs[self._active_song_index]
        )
        if status == QMediaPlayer.MediaStatus.LoadedMedia and is_correct_song:
            # Media loaded, we can start playing.
            def delayed_play() -> None:
                self._is_loading = False
                self._is_playing = True

            # Delay otherwise Qt won't actually play anything.
            QTimer.singleShot(0, delayed_play)

    def _toggle_play_pause(self) -> None:
        self._is_playing = not self._is_playing

    def _skip_previous(self) -> None:
        self._active_song_index = (
            self._active_song_index - 1
            if self._active_song_index > 0
            else len(songs) - 1
        )

    def _skip_next(self) -> None:
        self._active_song_index = (
            self._active_song_index + 1
            if self._active_song_index < len(songs) - 1
            else 0
        )

    @effect(_active_song_index)
    def _load_song(self) -> None:
        self._media_player.setSource(songs[self._active_song_index])
        self._is_loading = True
        self._is_playing = False

    @effect(_is_playing)
    def _apply_media_player_play_state(self) -> None:
        if self._is_playing:
            self._media_player.play()
        else:
            self._media_player.pause()


def main() -> None:
    app = QApplication()
    window = MusicPlayerApp()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
