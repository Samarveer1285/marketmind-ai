import os
from functools import lru_cache

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_tools import (
    demand_tool,
    brand_tool,
    recommendation_tool,
    risk_tool,
    category_tool
)

load_dotenv()


@lru_cache(maxsize=1)
def get_llm():
    """
    Lazy, cached Gemini client -- built on first actual use inside
    ask_agent()'s try/except, not at import time. Previously this was built
    at module level, so a missing/invalid GEMINI_API_KEY would crash on
    import (taking down the AI Copilot and Executive Command Center pages
    with a raw traceback) before ask_agent() ever got a chance to catch it.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )

def route_question(question):

    q = question.lower()

    if any(
        word in q
        for word in [
            "risk",
            "danger",
            "weak",
            "declining"
        ]
    ):
        return risk_tool()

    elif any(
        word in q
        for word in [
            "opportunity",
            "recommend",
            "invest",
            "investment"
        ]
    ):
        return recommendation_tool()

    elif any(
        word in q
        for word in [
            "brand",
            "health"
        ]
    ):
        return brand_tool()

    elif any(
        word in q
        for word in [
            "category"
        ]
    ):
        return category_tool()

    elif any(
        word in q
        for word in [
            "growth",
            "momentum",
            "fastest"
        ]
    ):
        return demand_tool()

    return (
        "No matching market intelligence "
        "tool found for this question."
    )


def ask_agent(question):

    try:

        tool_output = route_question(question)

    except Exception as e:

        error_text = str(e)

        if (
            "429" in error_text
            or "quota" in error_text.lower()
            or "rate limit" in error_text.lower()
            or "exceeded" in error_text.lower()
        ):

            return (
                "⚠️ Gemini free quota exhausted.\n\n"
                "The AI Copilot logic is functioning correctly, "
                "but Gemini cannot process further requests right now.\n\n"
                "Please retry later when quota resets."
            )

        return (
            "Unable to execute agent.\n\n"
            f"{error_text}"
        )

    executive_prompt = f"""
You are an executive market intelligence analyst.

User Question:
{question}

Market Intelligence:
{tool_output}

Generate a concise executive briefing with:

1. Executive Insight
2. Strategic Implications
3. Recommended Actions
4. Confidence Level

Use professional business language.
Do not invent facts.
Base your response only on the market intelligence provided.
"""

    try:

        llm = get_llm()

        return llm.invoke(executive_prompt).content

    except Exception as e:

        error_text = str(e)

        if (
            "429" in error_text
            or "quota" in error_text.lower()
            or "rate limit" in error_text.lower()
            or "exceeded" in error_text.lower()
        ):

            return (
                "⚠️ Executive briefing unavailable because Gemini quota "
                "has been exhausted.\n\n"
                "Showing underlying market intelligence instead:\n\n"
                f"{tool_output}"
            )

        return (
            "Unable to generate executive briefing.\n\n"
            f"{error_text}"
        )