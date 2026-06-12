import os
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SNAPSHOT_DIR = os.path.join(
    BASE_DIR,
    "pipelines",
    "snapshots"
)


def get_latest_market_data():

    if not os.path.exists(SNAPSHOT_DIR):
        return pd.DataFrame()

    files = [
        f
        for f in os.listdir(SNAPSHOT_DIR)
        if f.endswith(".csv")
    ]

    if len(files) == 0:
        return pd.DataFrame()

    latest_data = []

    for file in files:

        path = os.path.join(
            SNAPSHOT_DIR,
            file
        )

        try:

            df = pd.read_csv(path)

            latest_data.append(df)

        except:
            pass

    if len(latest_data) == 0:
        return pd.DataFrame()

    data = pd.concat(
        latest_data,
        ignore_index=True
    )

    if "title" in data.columns:
        data["product_name"] = data["title"]

    if "analytics_category" in data.columns:
        data["keyword"] = data["analytics_category"]

    elif "category" in data.columns:
        data["keyword"] = data["category"]

    return data
def get_market_summary():

    data = get_latest_market_data()

    if data.empty:

        return {
            "products": 0,
            "categories": 0,
            "avg_rating": 0,
            "avg_price": 0
        }

    return {

        "products":
            len(data),

        "categories":
            data["keyword"].nunique(),

        "avg_rating":
            round(
                data["rating"].mean(),
                2
            ),

        "avg_price":
            round(
                data["price"].mean(),
                0
            )
    }