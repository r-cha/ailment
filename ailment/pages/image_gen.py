import openai
import pynecone as pc
import replicate

from ailment import styles
from ailment.components import card, container, navbar
from ailment.state import State


model_options = ["Dall-E", "Stable Diffusion", "Midjourney"]


class ImageGenState(State):
    """The app state."""

    prompt = ""
    image_url = ""
    image_processing = False
    image_made = False
    model: str = ""

    @staticmethod
    def _do_dalle(prompt: str) -> str:
        response = openai.Image.create(prompt=prompt, n=1, size="512x512")
        return response["data"][0]["url"]

    @staticmethod
    def _do_stability(prompt: str) -> str:
        model = replicate.models.get("stability-ai/stable-diffusion")
        version = model.versions.get(
            "27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478"
        )
        return version.predict(prompt=prompt, width=512, height=512)

    @staticmethod
    def _do_midjourney(prompt: str) -> str:
        model = replicate.models.get("tstramer/midjourney-diffusion")
        version = model.versions.get(
            "436b051ebd8f68d23e83d22de5e198e0995357afef113768c20f0b6fcef23c8b"
        )
        return version.predict(prompt=prompt, width=512, height=512)


    _model_map = {
        "Dall-E": _do_dalle,
        "Stable Diffusion": _do_stability,
        "Midjourney": _do_midjourney
    }

    def process_image(self):
        """
        Set the image processing flag to true
        and indicate that the image has not been made yet.
        """
        self.image_made = False
        self.image_processing = True

    def get_image(self):
        """Get the image from the prompt."""
        try:
            self.image_url = self._model_map[self.model](self.prompt)
            self.image_processing = False
            self.image_made = True
        except Exception as e:
            self.image_processing = False
            return pc.window_alert(f"Error with execution: {e}")


def images_card():
    return card(
        pc.text(
            "Generate an image.",
            font_size=styles.H3_FONT_SIZE,
            font_weight=styles.BOLD_WEIGHT,
        ),
        pc.vstack(
            pc.vstack(
                pc.select(
                    model_options,
                    placeholder="Select a model.",
                    on_change=ImageGenState.set_model,
                ),
                pc.text(
                    "Enter a prompt.",
                    color="#676767",
                    margin_bottom="1em",
                ),
                pc.text_area(
                    size="lg",
                    on_blur=ImageGenState.set_prompt
                ),
                pc.button(
                    "Generate Image",
                    on_click=[ImageGenState.process_image, ImageGenState.get_image],
                    width="100%",
                ),
                align_items="start",
                width="100%",
            ),
            pc.divider(),
            pc.cond(
                ImageGenState.image_processing,
                pc.circular_progress(is_indeterminate=True),
                pc.cond(
                    ImageGenState.image_made,
                    pc.image(
                        src=ImageGenState.image_url,
                        height="25em",
                        width="25em",
                    ),
                ),
            ),
            align_items="start",
        ),
        height="100%",
        margin_bottom="1em",
        background="white",
    )

def images():
    return pc.box(
        navbar(),
        pc.flex(
            container(images_card(), margin_top="72px"),
        ),
        width="100%",
        height="100vh",
        background=styles.background
    )
