from database import supabase
import pandas as pd
import numpy as np

# -----------------------------
# Load Data
# -----------------------------

products = supabase.table("products").select("*").execute()
price_history = supabase.table("price_history").select("*").execute()

products_df = pd.DataFrame(products.data)
prices_df = pd.DataFrame(price_history.data)

merged = prices_df.merge(
    products_df,
    left_on="product_id",
    right_on="id"
)

print("\n==============================")
print("DATA LOADED SUCCESSFULLY")
print("==============================")

# -----------------------------
# CUSTOMER TRUST SCORE
# -----------------------------

merged["trust_score"] = (
    merged["rating"] *
    np.log1p(merged["review_count"])
)

trust_ranking = (
    merged[
        ["name", "trust_score"]
    ]
    .sort_values(
        by="trust_score",
        ascending=False
    )
)

print("\nTOP TRUSTED PRODUCTS")
print(trust_ranking.head(10))

# -----------------------------
# PRICE VOLATILITY
# -----------------------------

volatility = (
    merged
    .groupby("name")["price"]
    .std()
    .reset_index()
)

volatility.columns = [
    "name",
    "price_volatility"
]

volatility = volatility.sort_values(
    by="price_volatility",
    ascending=False
)

print("\nMOST VOLATILE PRODUCTS")
print(volatility)

# -----------------------------
# HIDDEN GEMS
# -----------------------------

avg_reviews = merged["review_count"].mean()

hidden_gems = merged[
    (merged["rating"] >= 4.5)
    &
    (merged["review_count"] < avg_reviews)
]

print("\nHIDDEN GEMS")
print(
    hidden_gems[
        [
            "name",
            "rating",
            "review_count"
        ]
    ]
)

# -----------------------------
# OVERPRICED PRODUCTS
# -----------------------------

avg_price = merged["price"].mean()

overpriced = merged[
    merged["price"] > avg_price * 1.15
]

print("\nOVERPRICED PRODUCTS")
print(
    overpriced[
        [
            "name",
            "price"
        ]
    ]
)

# -----------------------------
# BRAND HEALTH INDEX
# -----------------------------

brand_health = (
    merged
    .groupby("brand")
    .agg({
        "rating": "mean",
        "review_count": "mean",
        "price": "mean"
    })
    .reset_index()
)

brand_health["brand_health_score"] = (
    brand_health["rating"] * 20
    +
    np.log1p(
        brand_health["review_count"]
    ) * 5
)

brand_health = (
    brand_health
    .sort_values(
        by="brand_health_score",
        ascending=False
    )
)

print("\nBRAND HEALTH INDEX")
print(
    brand_health[
        [
            "brand",
            "brand_health_score"
        ]
    ]
)
latest_prices = (
    merged
    .sort_values("recorded_at")
    .groupby("name")
    .tail(1)
)

latest_prices["value_score"] = (
    latest_prices["rating"]
    /
    (latest_prices["price"] / 10000)
)

undervalued = (
    latest_prices[
        [
            "name",
            "price",
            "rating",
            "value_score"
        ]
    ]
    .sort_values(
        by="value_score",
        ascending=False
    )
)

print("\nUNDERVALUED PRODUCTS")
print(undervalued)

price_trend = (
    merged
    .sort_values("recorded_at")
    .groupby("name")
    .agg(
        first_price=("price", "first"),
        last_price=("price", "last")
    )
    .reset_index()
)

price_trend["price_change_pct"] = (
    (
        price_trend["last_price"]
        -
        price_trend["first_price"]
    )
    /
    price_trend["first_price"]
) * 100

print("\nBIGGEST PRICE DROPS")
print(
    price_trend.sort_values(
        by="price_change_pct"
    )
)
leaderboard = (
    merged
    .groupby("name")
    .agg({
        "rating":"mean",
        "review_count":"mean"
    })
    .reset_index()
)

leaderboard["market_score"] = (
    leaderboard["rating"] * 10
    +
    np.log1p(
        leaderboard["review_count"]
    ) * 5
)

leaderboard = (
    leaderboard
    .sort_values(
        by="market_score",
        ascending=False
    )
)

print("\nMARKET LEADERBOARD")
print(
    leaderboard[
        [
            "name",
            "rating",
            "review_count",
            "market_score"
        ]
    ]
)
avg_rating = merged["rating"].mean()
avg_reviews = merged["review_count"].mean()

matrix = (
    merged
    .groupby("name")
    .agg({
        "rating":"mean",
        "review_count":"mean"
    })
    .reset_index()
)

def classify(row):

    if (
        row["rating"] >= avg_rating
        and
        row["review_count"] >= avg_reviews
    ):
        return "Star"

    elif (
        row["rating"] >= avg_rating
        and
        row["review_count"] < avg_reviews
    ):
        return "Hidden Gem"

    elif (
        row["rating"] < avg_rating
        and
        row["review_count"] >= avg_reviews
    ):
        return "Needs Attention"

    else:
        return "Poor Performer"

matrix["category"] = (
    matrix.apply(
        classify,
        axis=1
    )
)

print("\nOPPORTUNITY MATRIX")
print(matrix)