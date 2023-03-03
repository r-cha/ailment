import pynecone as pc

from ailment.components import navbar, background


def index():
    return pc.center(
        pc.vstack(
            navbar(),
            pc.heading("Ailment", font_size="1.5em"),
        ),
        width="100%",
        height="100vh",
        background=background,
    )