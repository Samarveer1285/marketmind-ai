from market_monitor import get_latest_market_data

def generate_live_market_alerts():

    data = get_latest_market_data()

    alerts = []

    if data.empty:
        return alerts

    # Low Ratings
    low_rated = data[
        data["rating"] < 4.0
    ]

    for _, row in low_rated.iterrows():

        alerts.append({
            "type": "Low Rating",
            "product": row["product_name"],
            "message": (
                f"{row['product_name']} "
                f"has a low rating of "
                f"{row['rating']}."
            )
        })

    # High Engagement
    high_reviews = data[
        data["review_count"]
        >
        data["review_count"].quantile(0.90)
    ]

    for _, row in high_reviews.iterrows():

        alerts.append({
            "type": "High Engagement",
            "product": row["product_name"],
            "message": (
                f"{row['product_name']} "
                f"is experiencing unusually "
                f"high engagement."
            )
        })

    # Premium Pricing
    expensive = data[
        data["price"]
        >
        data["price"].quantile(0.90)
    ]

    for _, row in expensive.iterrows():

        alerts.append({
            "type": "Premium Pricing",
            "product": row["product_name"],
            "message": (
                f"{row['product_name']} "
                f"is priced significantly "
                f"above the market average."
            )
        })

    return alerts