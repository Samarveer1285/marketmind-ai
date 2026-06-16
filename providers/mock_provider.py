import pandas as pd
import random
from datetime import datetime

from providers.provider_interface import DataProvider


class MockProvider(DataProvider):

    """
    Simulates a live e-commerce data provider.

    Used for:
    - Pipeline development
    - Forecasting
    - Alerts
    - Gemini integration
    - n8n workflows

    Can later be replaced by FlipkartProvider
    without changing the rest of MarketMind.
    """

    MOCK_PRODUCTS = {
        "wireless earbuds": [
            "boAt Airdopes 141",
            "Noise Buds VS104",
            "OnePlus Nord Buds 3",
            "Realme Buds T110",
            "Boult Audio Z40"
        ],

        "protein powder": [
            "Optimum Nutrition Whey",
            "MuscleBlaze Biozyme",
            "AS-IT-IS Whey",
            "Avvatar Whey",
            "Bigmuscles Nutrition"
        ],

        "running shoes": [
            "Nike Revolution 7",
            "Adidas Duramo",
            "Puma Flyer Runner",
            "ASICS Jolt",
            "Skechers Go Run"
        ]
    }

    def fetch_products(
        self,
        keyword: str,
        limit: int = 20
    ) -> pd.DataFrame:

        keyword_lower = keyword.lower()

        products = self.MOCK_PRODUCTS.get(
            keyword_lower,
            [
                f"{keyword.title()} Product {i}"
                for i in range(1, limit + 1)
            ]
        )

        rows = []

        for product in products[:limit]:

            price = random.randint(
                500,
                5000
            )

            rating = round(
                random.uniform(3.5, 4.8),
                1
            )

            review_count = random.randint(
                100,
                50000
            )

            rows.append({
                "keyword": keyword,
                "product_name": product,
                "price": price,
                "rating": rating,
                "review_count": review_count,
                "timestamp": datetime.now()
            })

        return pd.DataFrame(rows)