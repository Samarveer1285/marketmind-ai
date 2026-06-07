from database import supabase
import random

products = supabase.table("products").select("*").execute()

for product in products.data:

    price_data = {
        "product_id": product["id"],
        "price": random.randint(40000, 120000),
        "rating": round(random.uniform(3.5, 5.0), 1),
        "review_count": random.randint(100, 5000)
    }

    supabase.table("price_history").insert(price_data).execute()

print("Price History Generated Successfully")