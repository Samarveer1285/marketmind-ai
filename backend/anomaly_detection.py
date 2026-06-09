from analytics_function import *

import pandas as pd


def detect_price_anomalies():

    merged = load_data()

    anomalies = []

    for product in merged["name"].unique():

        temp = (
            merged[
                merged["name"] == product
            ]
            .sort_values(
                "recorded_at"
            )
        )

        temp = temp.reset_index(
            drop=True
        )

        latest = (
            temp.iloc[-1]["price"]
        )

        average = (
            temp["price"].mean()
        )

        deviation = (
            (latest - average)
            / average
        ) * 100

        if abs(deviation) > 10:

            anomalies.append({

                "product":
                    product,

                "latest_price":
                    latest,

                "average_price":
                    round(
                        average,
                        2
                    ),

                "deviation_pct":
                    round(
                        deviation,
                        2
                    )
            })

    return pd.DataFrame(
        anomalies
    )


def detect_rating_anomalies():

    merged = load_data()

    anomalies = []

    for product in merged["name"].unique():

        temp = (
            merged[
                merged["name"] == product
            ]
            .sort_values(
                "recorded_at"
            )
        )

        temp = temp.reset_index(
            drop=True
        )

        latest = (
            temp.iloc[-1]["rating"]
        )

        average = (
            temp["rating"].mean()
        )

        deviation = (
            (latest - average)
            / average
        ) * 100

        if abs(deviation) > 8:

            anomalies.append({

                "product":
                    product,

                "latest_rating":
                    latest,

                "average_rating":
                    round(
                        average,
                        2
                    ),

                "deviation_pct":
                    round(
                        deviation,
                        2
                    )
            })

    return pd.DataFrame(
        anomalies
    )