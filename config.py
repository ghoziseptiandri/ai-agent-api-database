from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
MODEL_NAME = "gemini-3.5-flash-lite" # Add the model you want to use

MAX_TOOL_LOOPS = 10
MAX_MEMORY_ITEMS = 10

client = genai.Client(
    api_key=GEMINI_API_KEY
)