import pandas as pd

from market_monitor import get_latest_market_data


def get_customer_segments():

    data = get_latest_market_data()

    if data.empty:
        return pd.DataFrame(
            columns=[
                "customer",
                "price",
                "rating",
                "review_count",
                "segment_name"
            ]
        )

    customer_data = data.copy()

    # Treat each product as a customer persona
    customer_data["customer"] = (
        customer_data["product_name"]
    )

    median_price = (
        customer_data["price"]
        .median()
    )

    median_reviews = (
        customer_data["review_count"]
        .median()
    )

    customer_data["segment_name"] = "Value Seekers"

    customer_data.loc[
        (
            (customer_data["price"] >= median_price)
            &
            (customer_data["rating"] >= 4.5)
        ),
        "segment_name"
    ] = "Premium Buyers"

    customer_data.loc[
        (
            (customer_data["review_count"] >= median_reviews)
            &
            (customer_data["rating"] >= 4.3)
        ),
        "segment_name"
    ] = "Loyal Advocates"

    customer_data.loc[
        customer_data["rating"] < 4,
        "segment_name"
    ] = "Low Satisfaction"

    return customer_data[
        [
            "customer",
            "price",
            "rating",
            "review_count",
            "segment_name"
        ]
    ]