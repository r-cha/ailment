from pathlib import Path

import pynecone as pc

from ailment import styles
from ailment.components import card, page
from ailment.state import State
from ailment.util.moises import MoisesClient

model_options = ["Whisper", "Moises"]


class AudioState(State):
    file: str
    model: str
    file_processing = False
    file_processed = False
    audio_urls: list[str]

    _moises_client: MoisesClient

    def _do_stem_separation(self, data: bytes):
        self._moises_client = (
            MoisesClient(
                name=f"Ailment {self.file}",
                data=data,
                download_directory=Path(".web/public/audio"),
            )
            .upload_file()
            .start_workflow()
        )
        self.file_processing = True
        self._moises_client.await_result()
        self.file_processing = False
        self.file_processed = True
        self.audio_urls = self._moises_client.files

    async def handle_upload(self, file: pc.UploadFile):
        self.file = file.filename
        upload_data = await file.read()

        if self.model == "Moises":
            self._do_stem_separation(upload_data)


def file_card(url: str):
    return pc.box(
        pc.button(
            text="DOWNLOAD",
            href=url,
        )
    )


def audio_card():
    return card(
        pc.text(
            "Process some audio.",
            font_size=styles.H3_FONT_SIZE,
            font_weight=styles.BOLD_WEIGHT,
        ),
        pc.vstack(
            pc.select(
                model_options,
                placeholder="Select a model.",
                on_change=AudioState.set_model,
            ),
            pc.upload(
                pc.vstack(
                    pc.button(
                        "Select File",
                        color=styles.ACCENT_COLOR,
                        bg="white",
                        border=f"1px solid {styles.ACCENT_COLOR}",
                    ),
                    pc.text("Drag and drop files here or click to select files"),
                    border=f"1px dotted {styles.ACCENT_COLOR}",
                    padding="5em",
                    width="100%",
                ),
                width="100%",
            ),
            pc.button(
                "Upload",
                on_click=lambda: AudioState.handle_upload(pc.upload_files()),
                width="100%",
            ),
            pc.divider(),
            pc.cond(
                AudioState.file_processing,
                pc.circular_progress(is_indeterminate=True),
                pc.cond(
                    AudioState.file_processed,
                    pc.hstack(
                        pc.foreach(AudioState.audio_urls, file_card),
                        width="100%",
                    ),
                ),
            ),
            align_items="start",
        ),
        height="100%",
        margin_bottom="1em",
        background="white",
    )


def audio_page():
    return page(audio_card())
