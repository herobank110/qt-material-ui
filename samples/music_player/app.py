"""Main app component."""

import asyncio
from pathlib import Path

import httpx
from material_ui._component import Component, effect, use_state
from material_ui.buttons.filled_button import FilledButton
from material_ui.layout_basics import Stack
from material_ui.tokens import md_sys_color
from material_ui.typography import Typography
from PySide6 import QtAsyncio
from qtpy.QtCore import Qt, QUrl
from qtpy.QtMultimedia import QMediaDevices
from qtpy.QtWidgets import QLabel


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

        image_label = QLabel()
        image_label.setFixedSize(200, 200)
        stack.add_widget(image_label)

        play_button = FilledButton()
        play_button.text = "Play"
        stack.add_widget(play_button)

        self.overlay_widget(stack)

        audio_files = asyncio.run(download_songs())
        # print(audio_files)
        # from audioplayer import AudioPlayer
        # player = AudioPlayer(r"C:\Users\davk1\Downloads\song18.mp3")
        # player.play()
        from qtpy.QtMultimedia import QAudioOutput, QMediaPlayer

        media_player = QMediaPlayer()
        media_player.setParent(self)
        audio_output = QAudioOutput()
        audio_output.setParent(media_player)
        print(audio_output.device().description())
        media_player.setAudioOutput(audio_output)
        media_player.setSource(QUrl("https://www.freecol.org/images/FreeCol-menu.ogg"))
        media_player.hasAudioChanged.connect(lambda: print("hasAudioChanged", media_player.hasAudio()))
        audio_output.setVolume(100.0)
        media_player.play()

    # @effect(image_url)
    # def _load_image(self) -> None:
    #     if self.image_url:
    #         future = asyncio.ensure_future(fetch(self.image_url))
    #         future.add_done_callback(lambda _: print("done!"))


async def download_songs() -> list[Path]:
    download_path = Path(__file__).parent / "downloaded"
    if not download_path.exists():
        print("Downloading songs...")
        download_path.mkdir(parents=True, exist_ok=True)
        async with httpx.AsyncClient() as client:
            responses = await asyncio.gather(
                client.get("https://www.freecol.org/images/fearless-sailors.ogg"),
                client.get("https://www.freecol.org/images/founders.ogg"),
                client.get("https://www.freecol.org/images/settlers-routine.ogg"),
                client.get("https://www.freecol.org/images/sunrise.ogg"),
                client.get("https://www.freecol.org/images/tailwind.ogg"),
                client.get("https://www.freecol.org/images/musicbox.ogg"),
                client.get("https://www.freecol.org/images/FreeCol-opening.ogg"),
                client.get("https://www.freecol.org/images/FreeCol-menu.ogg"),
            )
        for response in responses:
            file_name = Path(str(response.request.url)).name
            file_path = download_path / file_name
            with file_path.open("wb") as fp:
                fp.write(response.content)
    return list(download_path.glob("*.ogg"))
