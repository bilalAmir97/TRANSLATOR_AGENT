import asyncio

class Agent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions

import asyncio

class Runner:
    @staticmethod
    def run_sync(agent, input: str, run_config):
        # Run the async run method synchronously
        return asyncio.run(Runner.run_async(agent, input, run_config))

    @staticmethod
    async def run_async(agent, input: str, run_config):
        # Use the model to generate a translation response
        prompt = input
        # Assuming run_config.model is an instance of OpenAIChatCompletionsModel
        openai_client = run_config.model.openai_client

        # Prepare the chat messages
        messages = [
            {"role": "system", "content": agent.instructions},
            {"role": "user", "content": prompt}
        ]

        # Call the OpenAI chat completions API
        response = await openai_client.chat_completions.create(
            model=run_config.model.model,
            messages=messages
        )

        # Extract the translated text from the response
        translated_text = response['choices'][0]['message']['content']

        class Response:
            def __init__(self):
                self.final_output = translated_text

        return Response()

import httpx

class AsyncOpenAI:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.chat_completions = self.ChatCompletions(self)

    class ChatCompletions:
        def __init__(self, parent):
            self.parent = parent

        async def create(self, model: str, messages: list):
            url = f"{self.parent.base_url}chat/completions"
            headers = {
                "Authorization": f"Bearer {self.parent.api_key}",
                "Content-Type": "application/json"
            }
            json_data = {
                "model": model,
                "messages": messages
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=json_data)
                response.raise_for_status()
                return response.json()

class OpenAIChatCompletionsModel:
    def __init__(self, model: str, openai_client: AsyncOpenAI):
        self.model = model
        self.openai_client = openai_client

class RunConfig:
    def __init__(self, model, model_provider, tracing_disabled: bool):
        self.model = model
        self.model_provider = model_provider
        self.tracing_disabled = tracing_disabled
