from typing import Dict
from app.services.retailer_service import get_retailer_prices
from app.schemas.recommendation import Pricing
from datetime import datetime

def enrich_with_pricing(product: dict):

    retailer_prices = get_retailer_prices(product)

    cheapest = min(retailer_prices, key=lambda x: x["price"])

    market_average = round(
        sum(x["price"] for x in retailer_prices) / len(retailer_prices),
        2,
    )

    difference_percent = (
        (market_average - cheapest["price"]) / market_average
    ) * 100

    if difference_percent >= 10:
        status = "Excellent Deal"
    elif difference_percent >= 5:
        status = "Good Deal"
    elif difference_percent >= 2:
        status = "Fair Price"
    else:
        status = "Market Price"

    pricing = Pricing(
        source="Retail Intelligence",
        currency="USD",
        best_store=cheapest["retailer"],
        best_price=cheapest["price"],
        market_average=market_average,
        potential_savings=round(
            market_average - cheapest["price"],
            2,
        ),
        buy_recommendation="Good time to buy",
        confidence="High",
        price_last_updated=datetime.utcnow().isoformat(),
        price_status=status,
    )

    product["pricing"] = pricing
    product["retailers"] = retailer_prices

    return product