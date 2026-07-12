from app.schemas.confidence import Confidence


def calculate_confidence(product: dict) -> Confidence:

    score = 0
    factors = []

    pricing = product.get("pricing")

    # Product Rating (35)
    rating = product.get("rating", 0)

    if rating >= 4.5:
        score += 35
        factors.append("Excellent product rating")
    elif rating >= 4.2:
        score += 30
        factors.append("Good product rating")
    elif rating >= 4.0:
        score += 25
        factors.append("Above average product rating")
    elif rating >= 3.5:
        score += 18
        factors.append("Average product rating")
    else:
        score += 10
        factors.append("Below average product rating")

    # Price Competitiveness (25)
    if pricing:

        savings = pricing.potential_savings

        if savings >= 20:
            score += 25
            factors.append("Excellent market price")
        elif savings >= 10:
            score += 22
            factors.append("Below market average")
        elif savings >= 5:
            score += 18
            factors.append("Competitive pricing")
        else:
            score += 15
            factors.append("Fair market pricing")

    # Retailer Availability (15)
    retailers = product.get("retailers", [])

    retailer_count = len([r for r in retailers if r["in_stock"]])

    if retailer_count >= 3:
        score += 15
        factors.append("Available across multiple retailers")
    elif retailer_count == 2:
        score += 12
        factors.append("Available across two retailers")
    elif retailer_count == 1:
        score += 8
        factors.append("Limited retailer availability")

    # Price Trend (10)
    trend = pricing.price_trend if pricing else "Stable"

    if trend == "Stable":
        score += 10
        factors.append("Stable pricing")
    elif trend == "Falling":
        score += 8
        factors.append("Price trend favors waiting")
    else:
        score += 5
        factors.append("Price trending upward")

    # AI Recommendation Score (15)
    recommendation_score = product.get("score", 0)

    ai_score = round(recommendation_score * 18)
    score += ai_score

    if recommendation_score >= 0.90:
        factors.append("Very strong AI recommendation")
    elif recommendation_score >= 0.80:
        factors.append("Strong AI recommendation")
    elif recommendation_score >= 0.70:
        factors.append("Moderate AI recommendation")

    score = min(score, 100)

    if score >= 80:
        level = "High"
    elif score >= 65:
        level = "Medium"
    else:
        level = "Low"

    if level == "High":
        summary = "High confidence recommendation based on product quality, pricing and retailer availability."
    elif level == "Medium":
        summary = "Reasonably confident recommendation with a few trade-offs."
    else:
        summary = "Recommendation has notable trade-offs. Consider reviewing alternatives."

    return Confidence(
        score=score,
        level=level,
        summary=summary,
        factors=factors,
    )