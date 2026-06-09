from analytics_function import *
import pandas as pd


def generate_market_alerts():

    alerts = []

    growth = get_demand_momentum()

    for _, row in growth.iterrows():

        if row["momentum_pct"] > 15:

            alerts.append({
                "type": "Opportunity",
                "product": row["name"],
                "message": f"Demand surged by {round(row['momentum_pct'],2)}%"
            })

        elif row["momentum_pct"] < -15:

            alerts.append({
                "type": "Risk",
                "product": row["name"],
                "message": f"Demand dropped by {round(abs(row['momentum_pct']),2)}%"
            })

    risk = get_risk_products()

    for _, row in risk.head(5).iterrows():

        alerts.append({
            "type": "High Risk",
            "product": row["name"],
            "message": f"Risk Score = {round(row['risk_score'],2)}"
        })

    return pd.DataFrame(alerts)