from database import supabase

data = {
    "name": "iPhone 16",
    "brand": "Apple",
    "category": "Smartphone"
}

response = supabase.table("products").insert(data).execute()

print("Inserted Successfully!")
print(response)