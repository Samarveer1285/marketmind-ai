from dotenv import load_dotenv
import os
import google.generativeai as genai

from analytics_function import *
from recommendation_engine import *

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def answer_question(question):

    try:

        recommendations = generate_recommendations()

        top_product = recommendations.iloc[0]

        risk_products = get_risk_products()

        top_risk = risk_products.iloc[0]

        brand_growth = get_brand_growth()

        top_brand = brand_growth.iloc[0]

        momentum = get_demand_momentum()

        fastest_product = momentum.iloc[0]

        prompt = f"""
You are a senior market intelligence analyst.

Use the market data below to answer the user's question.

MARKET DATA

Fastest Growing Product:
{fastest_product['name']}

Growth Percentage:
{round(fastest_product['momentum_pct'], 2)}

Fastest Growing Brand:
{top_brand['brand']}

Brand Growth Score:
{round(top_brand['brand_growth_score'], 2)}

Highest Opportunity Product:
{top_product['product']}

Priority Score:
{round(top_product['priority_score'], 2)}

Recommended Action:
{top_product['recommendation']}

Highest Risk Product:
{top_risk['name']}

Risk Score:
{round(top_risk['risk_score'], 2)}

USER QUESTION:
{question}

Answer like a business analyst.
Give insights and recommendations.
Keep the answer concise.
"""

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return str(e)