import os
import openai


class Assistant:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def respond(self, prompt, model="text-davinci-003", temperature=0.5, max_tokens=64, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
        if prompt == '':
            return
        response = openai.Completion.create(
            model=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )

        return response
