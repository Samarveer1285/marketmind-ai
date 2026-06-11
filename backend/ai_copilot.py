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


def answer_question(question):

    try:

        data = get_latest_market_data()

        if data.empty:

            return (
                "No live market data is currently available."
            )

        alerts = generate_market_alerts()

        total_products = len(data)

        total_categories = (
            data["category"]
            .nunique()
        )

        total_brands = (
            data["brand"]
            .nunique()
        )

        avg_price = round(
            data["price"].mean(),
            2
        )

        avg_rating = round(
            data["rating"].mean(),
            2
        )

        top_reviewed = (
            data.nlargest(
                3,
                "review_count"
            )
            [
                [
                    "title",
                    "brand",
                    "review_count"
                ]
            ]
            .to_dict(
                orient="records"
            )
        )

        hidden_gems = data[
            (data["rating"] >= 4.4)
            &
            (data["review_count"] < 500)
            &
            (data["discount_percent"] >= 20)
        ]

        hidden_gems = (
            hidden_gems[
                [
                    "title",
                    "brand",
                    "rating"
                ]
            ]
            .head(3)
            .to_dict(
                orient="records"
            )
        )

        alert_summary = (
            alerts["Type"]
            .value_counts()
            .to_dict()
        )

        prompt = f"""
You are MarketMind AI.

You are an executive market intelligence analyst.

Your job is to answer questions using ONLY the live market intelligence provided below.

LIVE MARKET SUMMARY

Total Products:
{total_products}

Categories Tracked:
{total_categories}

Brands Tracked:
{total_brands}

Average Price:
₹{avg_price}

Average Rating:
{avg_rating}

TOP REVIEWED PRODUCTS

{json.dumps(top_reviewed, indent=2)}

HIDDEN GEMS

{json.dumps(hidden_gems, indent=2)}

MARKET ALERT SUMMARY

{json.dumps(alert_summary, indent=2)}

USER QUESTION

{question}

Instructions:

- Answer like a senior business analyst.
- Use the provided market data.
- Give actionable recommendations.
- Mention specific products or brands when relevant.
- Keep responses concise but insightful.
- Never invent facts that are not present in the provided data.
"""

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return (
            f"Unable to generate response.\n\n{str(e)}"
        )