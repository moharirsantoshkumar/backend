from typing import List, Dict

def get_prices(product: Dict) -> List[Dict]:
    """
    Temporary implementation.

    Next step will call real APIs.
    """

    base = float(product["price"])

    return [
        {
            "retailer": "Amazon",
            "price": round(base * 0.98, 2),
            "currency": "USD",
            "product_url": "#",
            "in_stock": True,
            "delivery_days": 2,
            "seller": "Amazon"
        },
        {
            "retailer": "Flipkart",
            "price": round(base * 1.01, 2),
            "currency": "USD",
            "product_url": "#",
            "in_stock": True,
            "delivery_days": 3,
            "seller": "Retail Partner"
        },
        {
            "retailer": "Croma",
            "price": round(base * 1.03, 2),
            "currency": "USD",
            "product_url": "#",
            "in_stock": False,
            "delivery_days": None,
            "seller": "Croma"
        }
    ]