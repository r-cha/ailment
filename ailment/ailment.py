"""
Sources:
- https://github.com/pynecone-io/pynecone-examples/blob/main/dalle/dalle/dalle.py
"""
import pynecone as pc

from ailment.pages.index import index
from ailment.state import State


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, route="/", title="ailment")
app.compile()