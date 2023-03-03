import pynecone as pc

from ailment import styles

def container(*children, **kwargs):
    kwargs = {"max_width": "1440px", "padding_x": ["1em", "2em", "3em"], **kwargs}
    return pc.container(
        *children,
        **kwargs,
    )

def card(*args, **kwargs):
    kwargs.update(
        {
            "padding": ["1em", "2em"],
            "border": "1px solid #E3E3E3",
            "border_radius": "1em",
            "box_shadow": styles.DOC_SHADOW_LIGHT,
            "align_items": "left",
            "_hover": {"box_shadow": styles.DOC_SHADOW},
        }
    )
    return pc.vstack(*args, **kwargs)

def navbar() -> pc.Component:
    return pc.box(
        pc.hstack(
            pc.hstack(
                pc.heading("Ailment Dashboard"),
            ),
            pc.menu(
                pc.menu_button(
                    "Menu", bg="black", color="white", border_radius="md", px=4, py=2
                ),
                pc.menu_list(
                    pc.link(pc.menu_item("Home"), href="/"),
                    pc.menu_divider(),
                    pc.link(pc.menu_item("DALL-E"), href="/dalle"),
                    pc.link(pc.menu_item("ChatGPT"), href="/gpt"),
                ),
            ),
            justify="space-between",
            border_bottom="0.2em solid #F0F0F0",
            padding_x="2em",
            padding_y="1em",
            bg="rgba(255,255,255, 0.97)",
        ),
        position="fixed",
        width="100%",
        top="0px",
        z_index="500",
    )
