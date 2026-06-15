import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.agents import (
    initialize_agent,
    AgentType
)

from langchain_tools import tools



load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)


agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


def ask_agent(question):

    return agent.run(question)