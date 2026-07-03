from typing import List, Dict

def get_prices(product: Dict) -> List[Dict]:
    """
    Temporary implementation.

    Next step will call real APIs.
    """

    base = float(product["price"])

    return [
        {
            "store": "Amazon",
            "price": round(base * 0.98, 2),
            "url": "#"
        },
        {
            "store": "Flipkart",
            "price": round(base * 1.01, 2),
            "url": "#"
        },
        {
            "store": "Croma",
            "price": round(base * 1.03, 2),
            "url": "#"
        }
    ]