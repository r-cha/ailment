"""
Sources:
- https://github.com/pynecone-io/pynecone-examples/blob/main/dalle/dalle/dalle.py
"""
import pynecone as pc

from ailment.pages.index import index
from ailment.pages.audio import audio_page
from ailment.pages.image_gen import images_page
from ailment.pages.text_gen import text_page
from ailment.state import State


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, route="/", title="ailment")
app.add_page(images_page, title="ailment::images")
app.add_page(text_page, title="ailment::text")
app.add_page(audio_page, title="ailment::audio")
app.compile()
