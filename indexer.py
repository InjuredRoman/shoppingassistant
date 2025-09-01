import os
from dotenv import load_dotenv

# loads api keys present in `.env` file
load_dotenv()

apiKeys = [
    "GEMINI_API_KEY",
]

keys = {}
for apiKey in apiKeys:
    try:
        keys[apiKey] = os.getenv(apiKey)
    except:
        print(f"Can't find {apiKey} in environment variables. Double check it's defined in local `.env` file")
