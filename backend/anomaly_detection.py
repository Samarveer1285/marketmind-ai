import pandas as pd

from snapshot_history import load_snapshot_history


def detect_price_anomalies():

    data = load_snapshot_history()

    if data.empty:
        return pd.DataFrame()

    anomalies = []

    for product in data["title"].dropna().unique():

        temp = (
            data[data["title"] == product]
            .sort_values("snapshot_date")
        )

        if len(temp) < 2:
            continue

        latest = temp.iloc[-1]["price"]

        historical_avg = temp.iloc[:-1]["price"].mean()

        if historical_avg == 0:
            continue

        deviation = (
            (latest - historical_avg)
            / historical_avg
        ) * 100

        if abs(deviation) >= 10:

            anomalies.append({
                "product": product,
                "latest_price": latest,
                "average_price": round(historical_avg, 2),
                "deviation_pct": round(deviation, 2)
            })

    return pd.DataFrame(anomalies)
def detect_rating_anomalies():

    data = load_snapshot_history()

    if data.empty:
        return pd.DataFrame()

    anomalies = []

    for product in data["title"].dropna().unique():

        temp = (
            data[data["title"] == product]
            .sort_values("snapshot_date")
        )

        if len(temp) < 2:
            continue

        latest = temp.iloc[-1]["rating"]

        historical_avg = temp.iloc[:-1]["rating"].mean()

        if historical_avg == 0:
            continue

        deviation = (
            (latest - historical_avg)
            / historical_avg
        ) * 100

        if abs(deviation) >= 8:

            anomalies.append({
                "product": product,
                "latest_rating": latest,
                "average_rating": round(historical_avg, 2),
                "deviation_pct": round(deviation, 2)
            })

    return pd.DataFrame(anomalies)