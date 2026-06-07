from database import supabase
import pandas as pd

products = supabase.table("products").select("*").execute()
price_history = supabase.table("price_history").select("*").execute()

products_df = pd.DataFrame(products.data)
prices_df = pd.DataFrame(price_history.data)

merged = prices_df.merge(
    products_df,
    left_on="product_id",
    right_on="id"
)

print("\nTOP RATED PHONE")
print(
    merged.sort_values(
        by="rating",
        ascending=False
    )[["name", "rating"]].head(1)
)

print("\nMOST REVIEWED PHONE")
print(
    merged.sort_values(
        by="review_count",
        ascending=False
    )[["name", "review_count"]].head(1)
)

print("\nAVERAGE PRICE")
print(round(merged["price"].mean(), 2))