"""
Sources:
- https://github.com/pynecone-io/pynecone-examples/blob/main/dalle/dalle/dalle.py
"""
import pynecone as pc

from ailment.pages import index, dalle, gpt
from ailment.state import State


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index, route="/", title="ailment")
app.add_page(dalle, title="ailment: dall-e")
app.add_page(gpt, title="ailment: chatgpt")
app.compile()