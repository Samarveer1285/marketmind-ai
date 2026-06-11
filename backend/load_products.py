import pandas as pd
import os
import glob


SNAPSHOT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "pipelines",
    "snapshots"
)


def get_latest_market_data():

    csv_files = glob.glob(
        os.path.join(SNAPSHOT_DIR, "*.csv")
    )

    if not csv_files:
        return pd.DataFrame()

    latest_files = {}

    for file in csv_files:

        filename = os.path.basename(file)

        parts = filename.replace(".csv", "").split("_")

        keyword = "_".join(parts[3:])

        latest_files[keyword] = file

    frames = []

    for file in latest_files.values():

        try:
            df = pd.read_csv(file)

            frames.append(df)

        except Exception:
            pass

    if not frames:
        return pd.DataFrame()

    return pd.concat(
        frames,
        ignore_index=True
    )