"""
Source https://github.com/pynecone-io/pynecone-examples/blob/main/dalle/dalle/dalle.py
"""
import pynecone as pc
import openai

from ailment.components import navbar, background
from ailment.state import State


class GPTState(State):

    prompt = ""
    reply = ""

    def get_response(self):
        """Get the image from the prompt."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": (
                        "You are a helpful, faithful assistant, "
                        " willing to show code examples and exercise creativity "
                        "when prompted."
                    )},
                    {"role": "user", "content": self.prompt},
                ],
            )
            self.reply = response.choices[0].message.content
        except Exception as e:
            return pc.window_alert(f"Error with OpenAI Execution: {e}")


def gpt():
    return pc.box(
        pc.vstack(
            navbar(),
            pc.box(
                pc.heading("ChatGPT", font_size="1.5em"),
                pc.text_area(
                    placeholder="Enter a prompt...",
                    size="lg",
                    on_blur=GPTState.set_prompt,
                ),
                pc.button(
                    "Talk to the beast",
                    on_click=GPTState.get_response,
                    width="100%",
                ),
                pc.divider(),
                pc.text_area(
                    default_value=GPTState.reply,
                    placeholder="GPT Result",
                    width="100%",
                ),
                bg="white",
                padding="10",
                shadow="lg",
                border_radius="lg",
            ),
        ),
        width="100%",
        height="100vh",
        background=background,
    )
