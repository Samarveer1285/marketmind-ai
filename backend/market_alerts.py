import pandas as pd

from load_products import get_latest_market_data


def generate_market_alerts():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame()

    alerts = []

    median_reviews = data["review_count"].median()

    # ==========================
    # Demand Opportunities
    # ==========================

    opportunities = data[
        (data["rating"] >= 4.3)
        &
        (data["review_count"] >= median_reviews)
        &
        (data["discount_percent"] >= 30)
    ]

    for _, row in opportunities.iterrows():

        alerts.append({
            "Type": "🟢 Opportunity",
            "Product": row["title"],
            "Category": row["category"],
            "Message":
                f"{row['rating']}★ rating, "
                f"{int(row['discount_percent'])}% discount "
                f"and strong engagement."
        })

    # ==========================
    # Quality Risks
    # ==========================

    risks = data[
        (data["rating"] < 3.8)
        &
        (data["review_count"] >= median_reviews)
    ]

    for _, row in risks.iterrows():

        alerts.append({
            "Type": "🔴 Risk",
            "Product": row["title"],
            "Category": row["category"],
            "Message":
                f"Low rating ({row['rating']}★) "
                f"despite significant market visibility."
        })

    # ==========================
    # Hidden Gems
    # ==========================

    hidden_gems = data[
        (data["rating"] >= 4.4)
        &
        (data["review_count"] < 500)
        &
        (data["discount_percent"] >= 20)
    ]

    for _, row in hidden_gems.iterrows():

        alerts.append({
            "Type": "💎 Hidden Gem",
            "Product": row["title"],
            "Category": row["category"],
            "Message":
                f"{row['rating']}★ rated product "
                f"with only {int(row['review_count'])} reviews."
        })

    # ==========================
    # Market Leaders
    # ==========================

    leaders = data.nlargest(
        5,
        "review_count"
    )

    for _, row in leaders.iterrows():

        alerts.append({
            "Type": "⚡ Leader",
            "Product": row["title"],
            "Category": row["category"],
            "Message":
                f"Market leader with "
                f"{int(row['review_count'])} reviews."
        })

    return pd.DataFrame(alerts)