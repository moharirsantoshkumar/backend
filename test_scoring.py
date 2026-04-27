import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app.services.scoring import calculate_scores

products = [
    {
        "name": "Dell XPS 13",
        "price": 85000,
        "battery_hours": 12,
        "rating": 4.5,
        "processor": "Intel i7",
        "ram_gb": 16
    },
    {
        "name": "HP Pavilion",
        "price": 60000,
        "battery_hours": 8,
        "rating": 4.2,
        "processor": "Intel i5",
        "ram_gb": 8
    }
]

weights = {
    "price": 0.4,
    "performance": 0.3,
    "battery": 0.2,
    "rating": 0.1
}

result = calculate_scores(products, weights)

for r in result:
    print(r["name"], r["score"])