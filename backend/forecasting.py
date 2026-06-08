from analytics_function import load_data
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


def forecast_reviews():

    merged = load_data()

    forecasts = []

    for product in merged["name"].unique():

        temp = (
            merged[
                merged["name"] == product
            ]
            .sort_values("recorded_at")
        )

        temp = temp.reset_index(drop=True)

        X = np.arange(len(temp)).reshape(-1, 1)

        y = temp["review_count"]

        model = LinearRegression()
        model.fit(X, y)

        next_day = [[len(temp)]]

        prediction = model.predict(
            next_day
        )[0]

        forecasts.append({
            "product": product,
            "current_reviews":
                y.iloc[-1],
            "forecast_reviews":
                round(prediction)
        })

    return pd.DataFrame(
        forecasts
    )

def forecast_price():

    merged = load_data()

    forecasts = []

    for product in merged["name"].unique():

        temp = (
            merged[
                merged["name"] == product
            ]
            .sort_values("recorded_at")
        )

        temp = temp.reset_index(drop=True)

        X = np.arange(
            len(temp)
        ).reshape(-1, 1)

        y = temp["price"]

        model = LinearRegression()
        model.fit(X, y)

        next_day = [[len(temp)]]

        prediction = model.predict(
            next_day
        )[0]

        forecasts.append({
            "product": product,
            "current_price":
                y.iloc[-1],
            "forecast_price":
                round(prediction, 2)
        })

    return pd.DataFrame(
        forecasts
    )