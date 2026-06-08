from database import supabase
from datetime import datetime, timedelta
import random

products = supabase.table("products").select("*").execute()

for product in products.data:

    base_price = random.randint(50000, 100000)

    for day in range(30):

        date = datetime.now() - timedelta(days=29-day)

        price = base_price + random.randint(-5000, 5000)

        record = {
            "product_id": product["id"],
            "price": price,
            "rating": round(random.uniform(3.8, 5.0), 1),
            "review_count": random.randint(100, 5000),
            "recorded_at": date.isoformat()
        }

        supabase.table("price_history").insert(record).execute()

print("30 days history generated")