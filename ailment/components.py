import pynecone as pc

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

background = (
    "radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),"
    "radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),"
    "radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)"
)