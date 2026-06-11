from database import supabase
import random

brands = [
    "Apple","Samsung","Google","OnePlus","Xiaomi",
    "Sony","LG","Dell","HP","Lenovo",
    "Asus","Acer","Boat","JBL","Nothing",
    "Realme","Oppo","Vivo","MSI","BenQ"
]

categories = [
    "Smartphone",
    "Laptop",
    "Tablet",
    "Smartwatch",
    "Headphones",
    "TV",
    "Camera",
    "Speaker",
    "Monitor",
    "Gaming Console"
]

products = []

for i in range(500):

    brand = random.choice(brands)
    category = random.choice(categories)

    products.append({
        "name": f"{brand} {category} {i+1}",
        "brand": brand,
        "category": category
    })

supabase.table(
    "products"
).insert(products).execute()

print("500 Products Inserted")