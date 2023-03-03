import pynecone as pc

from ailment.components import navbar, container
from ailment import styles
from ailment.pages.image_gen import images_card
from ailment.pages.text_gen import text_card


def grid():
    return pc.flex(
        container(
            pc.grid(
                pc.grid_item(
                    images_card(),
                    col_span=2,
                ),
                pc.grid_item(
                    text_card(),
                    col_span=3,
                ),
                h="60em",
                template_rows="repeat(2, 1fr)",
                template_columns="repeat(5, 1fr)",
                width="100%",
                gap=4,
            ),
            min_height="60em",
            template_rows="repeat(2, 1fr)",
            template_columns="repeat(5, 1fr)",
            width="100%",
            gap=4,
        ),
        margin_y="60px",
    )



def index():
    return  pc.box(
        navbar(),
        pc.heading("Ailment", font_size="1.5em"),
        grid(),
        width="100%",
        height="100vh",
        background=styles.background,
    )