from app.services.normalizer import normalize_product


def fetch_mobile_data(db):
    raw = [
        {
                "id": 101,
                "name": "iPhone 14",
                "price": 70000,
                "battery_hours": 20,
                "rating": 4.6,
                "processor": "A15 Bionic",
                "ram_gb": 6
            },
            {
                "id": 102,
                "name": "Samsung Galaxy S23",
                "price": 65000,
                "battery_hours": 22,
                "rating": 4.5,
                "processor": "Snapdragon 8 Gen 2",
                "ram_gb": 8
            },
            {
                "id": 103,
                "name": "OnePlus 11",
                "price": 60000,
                "battery_hours": 24,
                "rating": 4.4,
                "processor": "Snapdragon 8 Gen 2",
                "ram_gb": 16
            }
        ]
    
    return [normalize_product(p, "mobiles") for p in raw]
    