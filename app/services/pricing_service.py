from typing import Dict
from app.services.retailer_service import get_retailer_prices
from app.schemas.recommendation import Pricing

def enrich_with_pricing(product: dict):

    retailer_prices = get_retailer_prices(product)

    cheapest = min(retailer_prices, key=lambda x: x["price"])

    market_average = round(
        sum(x["price"] for x in retailer_prices) / len(retailer_prices),
        2,
    )

    pricing = Pricing(
        source="Retail Intelligence",
        currency="USD",
        best_store=cheapest["store"],
        best_price=cheapest["price"],
        market_average=market_average,
        potential_savings=round(
            market_average - cheapest["price"],
            2,
        ),
        buy_recommendation="Good time to buy",
    )

    product["pricing"] = pricing
    product["retailers"] = retailer_prices

    return product