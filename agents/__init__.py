import asyncio

class Agent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions

class Runner:
    @staticmethod
    def run_sync(agent, input: str, run_config):
        # Dummy synchronous run method
        class Response:
            def __init__(self):
                self.final_output = f"Translated text for input: {input}"
        return Response()

class AsyncOpenAI:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

class OpenAIChatCompletionsModel:
    def __init__(self, model: str, openai_client: AsyncOpenAI):
        self.model = model
        self.openai_client = openai_client

class RunConfig:
    def __init__(self, model, model_provider, tracing_disabled: bool):
        self.model = model
        self.model_provider = model_provider
        self.tracing_disabled = tracing_disabled
