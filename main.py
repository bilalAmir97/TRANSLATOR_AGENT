from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel,RunConfig
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


translator = Agent(
    name= 'Translating Agent',
    instructions= '''You are a Translator Agent. Translate any Paragraph, phrase, or clause into 
    language as per instructions. If not given, convert it into roman urdu.'''
)

response= Runner.run_sync(
    translator,
    input= input('Enter the text to be translated: '),
    run_config= config
)
print(response.final_output)