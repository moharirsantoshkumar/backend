from typing import Dict
from app.services.retailer_service import get_retailer_prices
from app.schemas.recommendation import Pricing
from datetime import datetime
from app.services.price_history_service import build_price_intelligence
from app.services.retailer_intelligence_service import analyze_retailers

def enrich_with_pricing(product: dict):

    retailer_prices = get_retailer_prices(product)

    cheapest = min(retailer_prices, key=lambda x: x["price"])

    fastest = min(
        [r for r in retailer_prices if r["in_stock"]],
        key=lambda x: x["delivery_days"],
        default=cheapest,
    )

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

    price_data = build_price_intelligence(product)

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
        retailer_reason=(
            f"{cheapest['retailer']} offers the lowest price "
            f"and delivery in {fastest['delivery_days']} day(s)."
        ),
        price_trend=price_data.price_trend,
        lowest_price=price_data.lowest_price,
        highest_price=price_data.highest_price,
        average_price=price_data.average_price,
        predicted_price=price_data.predicted_price,
        recommended_action=price_data.recommended_action,
        estimated_wait_savings=price_data.estimated_wait_savings,
    )

    product["pricing"] = pricing
    product["price_history"] = [
        point.model_dump()
        for point in price_data.price_history
    ]
    product["retailers"] = retailer_prices
    product["retailer_intelligence"] = analyze_retailers(product)

    return product