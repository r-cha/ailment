"""
Source https://github.com/pynecone-io/pynecone-examples/blob/main/dalle/dalle/dalle.py
"""
import pynecone as pc
import openai

from ailment.components import navbar, background
from ailment.state import State


class DalleState(State):
    """The app state."""

    prompt = ""
    image_url = ""
    image_processing = False
    image_made = False

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
            response = openai.Image.create(prompt=self.prompt, n=1, size="1024x1024")
            self.image_url = response["data"][0]["url"]
            # Set the image processing flag to false
            # and indicate that the image has been made.
            self.image_processing = False
            self.image_made = True
        except Exception as e:
            self.image_processing = False
            return pc.window_alert(f"Error with OpenAI Execution: {e}")


def dalle():
    return pc.center(
        pc.vstack(
            navbar(),
            pc.heading("DALL-E", font_size="1.5em"),
            pc.input(
                placeholder="Enter a prompt...",
                size="lg",
                on_blur=DalleState.set_prompt
            ),
            pc.button(
                "Generate Image",
                on_click=[DalleState.process_image, DalleState.get_image],
                width="100%",
            ),
            pc.divider(),
            pc.cond(
                DalleState.image_processing,
                pc.circular_progress(is_indeterminate=True),
                pc.cond(
                    DalleState.image_made,
                    pc.image(
                        src=DalleState.image_url,
                        height="25em",
                        width="25em",
                    ),
                ),
            ),
            bg="white",
            padding="2em",
            shadow="lg",
            border_radius="lg",
        ),
        width="100%",
        height="100vh",
        background=background,
    )
