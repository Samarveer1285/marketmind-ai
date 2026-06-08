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
# -----------------------------
# DEMAND MOMENTUM SCORE
# -----------------------------

momentum = (
    merged
    .sort_values("recorded_at")
    .groupby("name")
    .agg(
        start_reviews=("review_count", "first"),
        end_reviews=("review_count", "last")
    )
    .reset_index()
)

momentum["momentum_pct"] = (
    (
        momentum["end_reviews"]
        -
        momentum["start_reviews"]
    )
    /
    momentum["start_reviews"]
) * 100

print("\nDEMAND MOMENTUM")
print(
    momentum.sort_values(
        by="momentum_pct",
        ascending=False
    )
)
# -----------------------------
# REVIEW GROWTH %
# -----------------------------

review_growth = (
    merged
    .sort_values("recorded_at")
    .groupby("name")
    .agg(
        start_reviews=("review_count", "first"),
        end_reviews=("review_count", "last")
    )
    .reset_index()
)

review_growth["review_growth_pct"] = (
    (
        review_growth["end_reviews"]
        -
        review_growth["start_reviews"]
    )
    /
    review_growth["start_reviews"]
) * 100

print("\nREVIEW GROWTH %")
print(
    review_growth.sort_values(
        by="review_growth_pct",
        ascending=False
    )
)
# -----------------------------
# RISK PRODUCTS
# -----------------------------

risk_products = (
    merged
    .sort_values("recorded_at")
    .groupby("name")
    .agg(
        avg_rating=("rating", "mean"),
        avg_reviews=("review_count", "mean"),
        avg_price=("price", "mean")
    )
    .reset_index()
)

risk_products["risk_score"] = (
    (5 - risk_products["avg_rating"]) * 10
)

risk_products = risk_products.sort_values(
    by="risk_score",
    ascending=False
)

print("\nRISK PRODUCTS")
print(
    risk_products[
        [
            "name",
            "avg_rating",
            "risk_score"
        ]
    ]
)
# -----------------------------
# BRAND GROWTH SCORE
# -----------------------------

brand_growth = (
    merged
    .sort_values("recorded_at")
    .groupby("brand")
    .agg(
        start_reviews=("review_count", "first"),
        end_reviews=("review_count", "last"),
        avg_rating=("rating", "mean")
    )
    .reset_index()
)

brand_growth["growth_pct"] = (
    (
        brand_growth["end_reviews"]
        -
        brand_growth["start_reviews"]
    )
    /
    brand_growth["start_reviews"]
) * 100

brand_growth["brand_growth_score"] = (
    brand_growth["growth_pct"] * 0.7
    +
    brand_growth["avg_rating"] * 10 * 0.3
)

brand_growth = brand_growth.sort_values(
    by="brand_growth_score",
    ascending=False
)

print("\nBRAND GROWTH SCORE")
print(
    brand_growth[
        [
            "brand",
            "growth_pct",
            "avg_rating",
            "brand_growth_score"
        ]
    ]
)
# -----------------------------
# REVENUE OPPORTUNITY SCORE
# -----------------------------

latest_products = (
    merged
    .sort_values("recorded_at")
    .groupby("name")
    .tail(1)
)

latest_products["opportunity_score"] = (
    latest_products["rating"] * 20
    -
    np.log1p(
        latest_products["review_count"]
    ) * 5
)

opportunity = (
    latest_products[
        [
            "name",
            "price",
            "rating",
            "review_count",
            "opportunity_score"
        ]
    ]
    .sort_values(
        by="opportunity_score",
        ascending=False
    )
)

print("\nREVENUE OPPORTUNITY SCORE")
print(opportunity)