from app.schemas.retailer_intelligence import (
    RetailerIntelligence,
    RetailerScore,
)


def analyze_retailers(product: dict) -> RetailerIntelligence:

    retailers = product.get("retailers", [])

    scores = []

    for retailer in retailers:

        # Trust Score (40)
        seller = retailer.get("seller", "")

        if seller == "Amazon":
            trust = 40
        elif seller == "Retail Partner":
            trust = 32
        else:
            trust = 25

        # Delivery Score (30)
        if retailer.get("in_stock"):

            days = retailer.get("delivery_days") or 7

            if days <= 1:
                delivery = 30
            elif days <= 2:
                delivery = 25
            elif days <= 3:
                delivery = 20
            else:
                delivery = 10
        else:
            delivery = 0

        # Value Score (30)
        prices = [
            r["price"]
            for r in retailers
            if r.get("in_stock")
        ]

        lowest = min(prices)

        difference = retailer["price"] - lowest

        if difference <= 0:
            value = 30
        elif difference <= 5:
            value = 25
        elif difference <= 10:
            value = 20
        else:
            value = 10

        total = trust + delivery + value

        if total >= 90:
            badge = "Best Overall"
        elif value == 30:
            badge = "Cheapest"
        elif delivery >= 25:
            badge = "Fast Delivery"
        else:
            badge = "Trusted Seller"

        scores.append(

            RetailerScore(
                retailer=retailer["retailer"],
                score=total,
                badge=badge,
                trust_score=trust,
                delivery_score=delivery,
                value_score=value,
            )

        )

    scores.sort(
        key=lambda x: x.score,
        reverse=True,
    )

    best = scores[0]

    return RetailerIntelligence(
        best_retailer=best.retailer,
        summary=f"{best.retailer} offers the best overall buying experience.",
        retailers=scores,
    )