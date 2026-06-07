from database import supabase

products = [
    {"name": "iPhone 16", "brand": "Apple", "category": "Smartphone"},
    {"name": "Galaxy S25", "brand": "Samsung", "category": "Smartphone"},
    {"name": "Pixel 10", "brand": "Google", "category": "Smartphone"},
    {"name": "OnePlus 14", "brand": "OnePlus", "category": "Smartphone"},
    {"name": "Xiaomi 15", "brand": "Xiaomi", "category": "Smartphone"}
]

response = supabase.table("products").insert(products).execute()

print("Products Inserted Successfully")
print(response)