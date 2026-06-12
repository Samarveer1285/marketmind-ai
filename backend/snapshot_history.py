import os
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SNAPSHOT_DIR = os.path.join(
    BASE_DIR,
    "pipelines",
    "snapshots"
)


def load_snapshot_history():

    all_data = []

    if not os.path.exists(SNAPSHOT_DIR):
        return pd.DataFrame()

    for file in os.listdir(SNAPSHOT_DIR):

        if not file.endswith(".csv"):
            continue

        try:
            path = os.path.join(SNAPSHOT_DIR, file)

            df = pd.read_csv(path)

            snapshot_date = file.split("_")[0]

            df["snapshot_date"] = snapshot_date

            all_data.append(df)

        except:
            pass

    if len(all_data) == 0:
        return pd.DataFrame()

    return pd.concat(
        all_data,
        ignore_index=True
    )