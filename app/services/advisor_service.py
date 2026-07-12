from app.schemas.advisor import BuyingAdvisor


def generate_buying_advice(product: dict) -> BuyingAdvisor:

    pricing = product.get("pricing")

    if not pricing:

        return BuyingAdvisor(
            decision="Insufficient Data",
            deal_score=50,
            potential_savings=0,
            wait_days=0,
            price_risk="Unknown",
            next_sale_probability="Unknown",
            summary="Not enough pricing information to generate buying advice."
        )

    score = 50

    # Price Trend
    if pricing.price_trend == "Stable":
        score += 15
    elif pricing.price_trend == "Falling":
        score -= 10
    elif pricing.price_trend == "Rising":
        score += 10

    # Potential Savings
    savings = pricing.potential_savings

    if savings >= 20:
        score += 15
    elif savings >= 10:
        score += 10
    elif savings >= 5:
        score += 5

    # Recommendation Confidence
    confidence = product.get("confidence")

    if confidence:

        if confidence.score >= 90:
            score += 15
        elif confidence.score >= 80:
            score += 10
        elif confidence.score >= 70:
            score += 5

    score = max(0, min(score, 100))

    # Decision
    if score >= 85:
        decision = "Buy Now"
        wait_days = 0
        risk = "High"
        sale_probability = "Low"

    elif score >= 70:
        decision = "Good Time to Buy"
        wait_days = 3
        risk = "Medium"
        sale_probability = "Medium"

    else:
        decision = "Wait"
        wait_days = 7
        risk = "Low"
        sale_probability = "High"

    summary = (
        f"{decision}. "
        f"Estimated savings by waiting: ${pricing.estimated_wait_savings}."
    )

    return BuyingAdvisor(
        decision=decision,
        deal_score=score,
        potential_savings=pricing.estimated_wait_savings,
        wait_days=wait_days,
        price_risk=risk,
        next_sale_probability=sale_probability,
        summary=summary,
    )