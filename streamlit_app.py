import nest_asyncio
nest_asyncio.apply()

# Import necessary libraries for UI, HTTP requests, environment variables, and regex
import streamlit as st
from streamlit_lottie import st_lottie
import requests
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import os
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Get the Gemini API key from environment variables
gemini_api_key = os.getenv("GEMINI_API")

# If API key is not found, show error and stop execution
if not gemini_api_key:
    st.error("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
    st.stop()

# Setup the external client for Gemini API using AsyncOpenAI
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Setup the OpenAI chat completions model with the external client
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configure the run settings for the agent
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Function to load Lottie animation from a URL
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load a 3D Lottie animation for UI enhancement
lottie_3d_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_3rwasyjy.json")

# Display the main title and subtitle of the app
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'>Translator Agent UI</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #306998;'>Translate text into multiple languages easily</h3>", unsafe_allow_html=True)

# Display the creator's credit below the title
st.markdown("<p style='text-align: center; font-size: 14px; color: gray; margin-bottom: 20px;'>Built by Muhammad Bilal Amir</p>", unsafe_allow_html=True)

# Render the Lottie animation in the UI
st_lottie(lottie_3d_animation, speed=1, height=200, key="3d_animation")

# Define the Translator Agent with instructions
translator = Agent(
    name='Translating Agent',
    instructions='''You are a Translator Agent. Translate any Paragraph, phrase, or clause into 
    language as per instructions. If not given, convert it into roman urdu.'''
)

# Input area for user to enter text to translate
st.markdown("### Enter text to translate:")
input_text = st.text_area("", height=150, max_chars=1000, placeholder="Type or paste text here...")

# List of common languages for translation with Roman Urdu as default option
languages = [
    "Roman Urdu",  # Added explicit roman urdu option
    "English",
    "Urdu",
    "French",
    "Spanish",
    "German",
    "Chinese",
    "Japanese",
    "Arabic",
    "Russian",
    "Hindi",
    "Italian",
    "Portuguese",
    "Bengali",
    "Korean",
    "Turkish",
    "Vietnamese",
    "Polish",
    "Dutch",
    "Romanian"
]

# Dropdown for selecting target language (optional)
target_language = st.selectbox("Select target language (optional):", languages)

# Layout buttons side by side: Translate and Clear
col1, col2 = st.columns([1, 3])

with col1:
    translate_button = st.button("Translate")
with col2:
    clear_button = st.button("Clear")

# Clear input and prompt user to enter new text when Clear button is clicked
if clear_button:
    input_text = ""
    st.write("Input cleared. Please enter new text.")

# When Translate button is clicked, process the input text
if translate_button:
    if not input_text.strip():
        st.warning("Please enter some text to translate.")
    else:
        with st.spinner("Translating..."):
            # Prepare prompt with target language if specified
            if target_language.strip():
                prompt = f"Translate the following text into {target_language}:\n{input_text}"
            else:
                prompt = input_text

            # Run the translation agent synchronously
            response = Runner.run_sync(
                translator,
                input=prompt,
                run_config=config
            )
            # Remove any HTML tags from the output for clean display
            clean_output = re.sub(r'<[^>]+>', '', response.final_output)

            # Display the translated output with styled markdown
            st.markdown("### Translated Output:")
            st.markdown(
                f"""
                <div style="
                    background-color:#282c34; 
                    color:#61dafb; 
                    padding:20px; 
                    border-radius:10px; 
                    font-size:18px; 
                    animation: fadeIn 1s ease-in-out;
                    white-space: pre-wrap;
                ">
                {clean_output}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Import Streamlit components for embedding custom HTML/JS
            import streamlit.components.v1 as components

            # Embed a hidden textarea and a copy button with JavaScript to copy translated text
            components.html(f"""
                <textarea id="copyTextArea" style="opacity:0; height:0; position:absolute;">{clean_output}</textarea>
                <button onclick="
                    var copyText = document.getElementById('copyTextArea');
                    copyText.select();
                    copyText.setSelectionRange(0, 99999);
                    navigator.clipboard.writeText(copyText.value);
                    alert('Translated text copied to clipboard!');
                ">
                    Copy Translated Text
                </button>
                <script>
                const btn = document.querySelector('button');
                btn.style.padding = '8px 16px';
                btn.style.fontSize = '16px';
                btn.style.backgroundColor = '#61dafb';
                btn.style.color = '#282c34';
                btn.style.border = 'none';
                btn.style.borderRadius = '5px';
                btn.style.cursor = 'pointer';
                btn.onmouseover = () => btn.style.backgroundColor = '#21a1f1';
                btn.onmouseout = () => btn.style.backgroundColor = '#61dafb';
                </script>
            """, height=60)
