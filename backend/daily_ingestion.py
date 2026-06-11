import requests
import pandas as pd
import os
from datetime import datetime


from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
ACTOR_ID = os.getenv("ACTOR_ID")

MAX_PRODUCTS = 50


CATEGORY_URLS = {
    "smartphones":
        "https://www.flipkart.com/search?q=smartphones",

    "gaming_laptops":
        "https://www.flipkart.com/search?q=gaming+laptops",

    "tablets":
        "https://www.flipkart.com/search?q=tablets",

    "bluetooth_speakers":
        "https://www.flipkart.com/search?q=bluetooth+speakers",

    "computer_monitors":
        "https://www.flipkart.com/search?q=computer+monitors",

    "headphones":
        "https://www.flipkart.com/search?q=headphones",

    "smartwatches":
        "https://www.flipkart.com/search?q=smartwatches",

    "televisions":
        "https://www.flipkart.com/search?q=televisions",

    "cameras":
        "https://www.flipkart.com/search?q=cameras",

    "power_banks":
        "https://www.flipkart.com/search?q=power+banks"
}


SNAPSHOT_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "pipelines",
    "snapshots"
)

os.makedirs(
    SNAPSHOT_DIR,
    exist_ok=True
)


def scrape_category(category_url):

    payload = {
        "proxyConfiguration": {
            "useApifyProxy": False
        },
        "results_wanted": MAX_PRODUCTS,
        "startUrl": category_url
    }

    response = requests.post(
        f"https://api.apify.com/v2/actors/{ACTOR_ID}/run-sync-get-dataset-items",
        params={
            "token": APIFY_TOKEN
        },
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    return pd.DataFrame(data)


def save_snapshot(df, category):

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    filepath = os.path.join(
        SNAPSHOT_DIR,
        f"{today}_{category}.csv"
    )

    df.to_csv(
        filepath,
        index=False
    )

    print(
        f"Saved snapshot: {filepath}"
    )


def run_ingestion():

    for category, url in CATEGORY_URLS.items():

        print(
            f"\nFetching: {category}"
        )

        try:

            df = scrape_category(url)

            if df.empty:

                print(
                    f"No data returned for {category}"
                )

                continue

            print(
                f"Fetched {len(df)} products"
            )

            save_snapshot(
                df,
                category
            )

        except Exception as e:

            print(
                f"Failed for {category}: {e}"
            )

    print(
        "\nIngestion completed."
    )


if __name__ == "__main__":

    run_ingestion()