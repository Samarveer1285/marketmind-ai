from analytics_function import load_data

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)


def compare_forecasting_models():

    merged = load_data()

    results = []

    for product in (
        merged["name"]
        .unique()
    ):

        temp = (
            merged[
                merged["name"] == product
            ]
            .sort_values(
                "recorded_at"
            )
        )

        if len(temp) < 10:
            continue

        y = (
            temp["review_count"]
            .values
        )

        X = (
            np.arange(
                len(y)
            )
            .reshape(-1,1)
        )

        split = int(
            len(y) * 0.8
        )

        X_train = X[:split]
        X_test = X[split:]

        y_train = y[:split]
        y_test = y[split:]

        # Linear Regression

        lr = LinearRegression()

        lr.fit(
            X_train,
            y_train
        )

        lr_pred = lr.predict(
            X_test
        )

        lr_mae = (
            mean_absolute_error(
                y_test,
                lr_pred
            )
        )

        # Random Forest

        rf = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

        rf.fit(
            X_train,
            y_train
        )

        rf_pred = rf.predict(
            X_test
        )

        rf_mae = (
            mean_absolute_error(
                y_test,
                rf_pred
            )
        )

        next_day = [[len(y)]]

        lr_forecast = (
            lr.predict(
                next_day
            )[0]
        )

        rf_forecast = (
            rf.predict(
                next_day
            )[0]
        )

        best_model = (
            "Random Forest"
            if rf_mae < lr_mae
            else "Linear Regression"
        )

        results.append({

            "product":
                product,

            "linear_mae":
                round(
                    lr_mae,
                    2
                ),

            "rf_mae":
                round(
                    rf_mae,
                    2
                ),

            "linear_forecast":
                round(
                    lr_forecast,
                    0
                ),

            "rf_forecast":
                round(
                    rf_forecast,
                    0
                ),

            "best_model":
                best_model
        })

    return pd.DataFrame(
        results
    )