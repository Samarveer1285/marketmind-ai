from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from langchain.agents import (
    initialize_agent,
    AgentType
)

from langchain_tools import tools

load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


agent = initialize_agent(

    tools,

    llm,

    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,

    verbose=False
)


def ask_agent(question):

    response = agent.run(
        question
    )

    return response