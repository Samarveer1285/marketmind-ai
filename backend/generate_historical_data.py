from database import supabase
from datetime import datetime, timedelta
import random

products = (
    supabase
    .table("products")
    .select("*")
    .execute()
)

history_records = []

for product in products.data:

    behaviour = random.choice([
        "growing",
        "declining",
        "premium",
        "hidden_gem"
    ])

    base_price = random.randint(
        15000,
        150000
    )

    base_reviews = random.randint(
        100,
        3000
    )

    for day in range(30):

        date = (
            datetime.now()
            - timedelta(days=29-day)
        )

        if behaviour == "growing":

            reviews = (
                base_reviews
                + day * random.randint(10, 30)
            )

            rating = round(
                random.uniform(4.3, 5.0),
                1
            )

            price = (
                base_price
                + random.randint(-2000, 2000)
            )

        elif behaviour == "declining":

            reviews = max(
                50,
                base_reviews
                - day * random.randint(5, 20)
            )

            rating = round(
                random.uniform(3.5, 4.2),
                1
            )

            price = (
                base_price
                - day * random.randint(20, 100)
            )

        elif behaviour == "premium":

            reviews = (
                base_reviews
                + random.randint(-50, 50)
            )

            rating = round(
                random.uniform(4.5, 5.0),
                1
            )

            price = random.randint(
                80000,
                200000
            )

        else:

            reviews = random.randint(
                50,
                500
            )

            rating = round(
                random.uniform(4.5, 5.0),
                1
            )

            price = random.randint(
                10000,
                60000
            )

        history_records.append({

            "product_id":
                product["id"],

            "price":
                price,

            "rating":
                rating,

            "review_count":
                reviews,

            "recorded_at":
                date.isoformat()
        })

print(
    f"Generated {len(history_records)} records"
)

batch_size = 500

for i in range(
    0,
    len(history_records),
    batch_size
):

    batch = history_records[
        i:i+batch_size
    ]

    supabase.table(
        "price_history"
    ).insert(batch).execute()

    print(
        f"Inserted {i + len(batch)}"
    )

print(
    "Historical Data Loaded Successfully"
)