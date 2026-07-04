import random
from app.schemas.price_intelligence import (
    PriceIntelligence,
    PriceHistoryPoint,
)


def get_price_history(product: dict):

    current_price = product["price"]

    history = []

    for days_ago in range(30, 0, -1):
        variation = random.uniform(-0.08, 0.08)
        price = round(current_price * (1 + variation), 2)

        history.append(
            {
                "day": days_ago,
                "price": price,
            }
        )

    history.append(
        {
            "day": 0,
            "price": current_price,
        }
    )

    return history

def get_price_statistics(history):

    prices = [p["price"] for p in history]

    return {
        "lowest_price": round(min(prices), 2),
        "highest_price": round(max(prices), 2),
        "average_price": round(sum(prices) / len(prices), 2),
    }

def get_price_trend(history):

    first_price = history[0]["price"]
    latest_price = history[-1]["price"]

    difference = ((latest_price - first_price) / first_price) * 100

    if difference >= 3:
        return "Rising"

    if difference <= -3:
        return "Falling"

    return "Stable"

def get_buy_recommendation(current_price, stats):

    if current_price <= stats["lowest_price"] * 1.02:
        return (
            "Buy Now",
            0,
        )

    if current_price >= stats["average_price"] * 1.05:
        savings = round(
            current_price - stats["average_price"],
            2,
        )

        return (
            "Wait",
            savings,
        )

    return (
        "Good Time to Buy",
        0,
    )

def get_predicted_price(history):

    latest = history[-1]["price"]
    average = sum(x["price"] for x in history[-7:]) / min(len(history), 7)

    return round((latest + average) / 2, 2)


def get_price_confidence(history):

    prices = [x["price"] for x in history]

    volatility = ((max(prices) - min(prices)) / sum(prices)) * len(prices)

    if volatility < 0.03:
        return "High"

    if volatility < 0.06:
        return "Medium"

    return "Low"


def build_price_intelligence(product):

    history = get_price_history(product)

    stats = get_price_statistics(history)

    trend = get_price_trend(history)

    recommendation, wait_savings = get_buy_recommendation(
        product["price"],
        stats,
    )

    prediction = get_predicted_price(history)

    confidence = get_price_confidence(history)

    return PriceIntelligence(
        price_history=[
            PriceHistoryPoint(**point)
            for point in history
        ],
        price_trend=trend,
        lowest_price=stats["lowest_price"],
        highest_price=stats["highest_price"],
        average_price=stats["average_price"],
        predicted_price=prediction,
        recommended_action=recommendation,
        estimated_wait_savings=wait_savings,
        pricing_confidence=confidence,
    )