from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

from load_products import get_latest_market_data
from market_alerts import generate_market_alerts

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


from langchain_agent import ask_agent

def answer_question(question):
    try:
        return ask_agent(question)
    except Exception as e:
        return f"Unable to generate response.\n\n{str(e)}"

    except Exception as e:

        return (
            f"Unable to generate response.\n\n{str(e)}"
        )