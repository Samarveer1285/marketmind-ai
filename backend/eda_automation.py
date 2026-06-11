import matplotlib.pyplot as plt
import pandas as pd
import json
import os
from datetime import datetime

from load_products import get_latest_market_data


REPORT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "analytics",
    "reports"
)

CHART_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "analytics",
    "charts"
)

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)


def generate_daily_eda_report():

    data = get_latest_market_data()

    if data.empty:
        print("No market data found.")
        return None

    today = datetime.now().strftime("%Y-%m-%d")

    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_products": int(len(data)),
        "categories": int(data["category"].nunique()),
        "brands": int(data["brand"].nunique()),
        "avg_price": round(float(data["price"].mean()), 2),
        "avg_rating": round(float(data["rating"].mean()), 2),
        "avg_reviews": round(float(data["review_count"].mean()), 2),
    }

    with open(
        os.path.join(REPORT_DIR, f"{today}_summary.json"),
        "w"
    ) as f:
        json.dump(summary, f, indent=4)

    top_products = (
        data.sort_values(
            "review_count",
            ascending=False
        )
        [
            [
                "title",
                "brand",
                "category",
                "price",
                "rating",
                "review_count"
            ]
        ]
        .head(10)
    )

    top_products.to_csv(
        os.path.join(
            REPORT_DIR,
            f"{today}_top_products.csv"
        ),
        index=False
    )

    hidden_gems = data[
        (data["rating"] >= 4.3)
        &
        (data["review_count"] < 500)
    ]

    hidden_gems[
        [
            "title",
            "brand",
            "category",
            "rating",
            "review_count"
        ]
    ].to_csv(
        os.path.join(
            REPORT_DIR,
            f"{today}_hidden_gems.csv"
        ),
        index=False
    )

    data[
        [
            "price",
            "rating",
            "review_count"
        ]
    ].describe().to_csv(
        os.path.join(
            REPORT_DIR,
            f"{today}_data_quality.csv"
        )
    )

    plt.figure(figsize=(10, 5))

    (
        data["category"]
        .value_counts()
        .plot(kind="bar")
    )

    plt.title("Category Distribution")
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIR,
            f"{today}_category_distribution.png"
        )
    )

    plt.close()

    plt.figure(figsize=(10, 5))

    data["rating"].hist(
        bins=10
    )

    plt.title("Rating Distribution")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIR,
            f"{today}_rating_distribution.png"
        )
    )

    plt.close()

    plt.figure(figsize=(10, 5))

    data["review_count"].hist(
        bins=20
    )

    plt.title("Review Distribution")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            CHART_DIR,
            f"{today}_review_distribution.png"
        )
    )

    plt.close()

    print("EDA completed successfully.")

    return summary


if __name__ == "__main__":
    print(generate_daily_eda_report())