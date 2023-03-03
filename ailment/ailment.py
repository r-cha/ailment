"""
Sources:
- https://github.com/pynecone-io/pynecone-examples/blob/main/dalle/dalle/dalle.py
"""
import pynecone as pc

from ailment.pages.index import index
from ailment.pages.image_gen import images
from ailment.pages.text_gen import text
from ailment.state import State


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, route="/", title="ailment")
app.add_page(images, title="ailment::images")
app.add_page(text, title="ailment::text")
app.compile()