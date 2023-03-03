import openai
import pynecone as pc

from ailment import styles
from ailment.components import card
from ailment.state import State

model_options = [
    model["id"]
    for model
    in openai.Model.list()["data"]
    if model["id"].startswith("text-")
    or "gpt" in model["id"]
]


class TextState(State):

    prompt = ""
    reply = ""
    model: str = "gpt-3.5-turbo"

    _chat_options = ["gpt-3.5-turbo", "gpt-3.5-turbo-0301"]

    @staticmethod
    def _do_chat(model: str, prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": (
                    "You are a helpful, faithful assistant, "
                    "willing to show code examples and exercise creativity "
                    "when prompted."
                )},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    @staticmethod
    def _do_completion(model: str, prompt: str) -> str:
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
        )
        return response.choices[0].text

    def get_response(self):
        """Get the image from the prompt."""
        try:
            model = (
                self._do_chat
                if self.model in self._chat_options else
                self._do_completion
            )
            self.reply = model(self.model, self.prompt)
        except Exception as e:
            return pc.window_alert(f"Error with execution: {e}")


def text_card():
    return card(
        pc.text(
            "Complete some text.",
            font_size=styles.H3_FONT_SIZE,
            font_weight=styles.BOLD_WEIGHT,
        ),
        pc.vstack(
            pc.vstack(
                pc.select(
                    model_options,
                    placeholder="Select a model.",
                    on_change=TextState.set_model,
                ),
                pc.text(
                    "Enter a prompt.",
                    color="#676767",
                    margin_bottom="1em",
                ),
                pc.input(
                    size="lg",
                    on_blur=TextState.set_prompt
                ),
                pc.button(
                    "Generate Text",
                    on_click=TextState.get_response,
                    width="100%",
                ),
                align_items="start",
                width="100%",
            ),
            pc.divider(),
            pc.text_area(
                default_value=TextState.reply,
                placeholder="Results...",
                width="100%",
            ),
            align_items="start",
        ),
        height="100%",
        margin_bottom="1em",
        background="white",
    )
