def normalize_product(item, category):
    return {
        "id": item.get("id"),
        "name": item.get("name"),
        "image": item.get("image", ""),
        "brand": item.get("brand", ""),
        "price": item.get("price", 0),
        "rating": item.get("rating", 0),
        "battery_hours": item.get("battery_hours", 0),
        "processor": item.get("processor", ""),
        "ram_gb": item.get("ram_gb", 0),
    }