import requests
from app.services.normalizer import normalize_product


def fetch_external_products(category):

    if category == "mobiles":
        url = "https://dummyjson.com/products/category/smartphones"
    elif category == "laptops":
        url = "https://dummyjson.com/products/category/laptops"
    else:
        url = "https://dummyjson.com/products"

    response = requests.get(url)

    data = response.json()

    products = []

    for item in data["products"][:10]:

        normalized = normalize_product({
            "id": item.get("id"),
            "name": item.get("title"),
            "image": item.get("thumbnail"),
            "brand": item.get("brand", ""),
            "price": item.get("price", 0),
            "rating": item.get("rating", 0),
            "battery_hours": 12,
            "processor": item.get("brand", ""),
            "ram_gb": 8
        }, category)

        products.append(normalized)

    return products