import math

def normalize(value, min_val, max_val):
    if max_val == min_val:
        return 1
    return (value - min_val) / (max_val - min_val)


def inverse_normalize(value, min_val, max_val):
    if max_val == min_val:
        return 1
    return (max_val - value) / (max_val - min_val)


def cpu_score(processor):
    processor = processor.lower()

    if "i7" in processor or "m1" in processor:
        return 0.9
    elif "i5" in processor:
        return 0.7
    elif "i3" in processor:
        return 0.5
    else:
        return 0.6


def calculate_scores(products, weights):

    prices = [p["price"] for p in products]
    batteries = [p["battery_hours"] for p in products]
    ratings = [p["rating"] for p in products]

    min_price, max_price = min(prices), max(prices)
    min_battery, max_battery = min(batteries), max(batteries)
    min_rating, max_rating = min(ratings), max(ratings)

    scored_products = []

    for p in products:
        price_s = inverse_normalize(p["price"], min_price, max_price)
        battery_s = normalize(p["battery_hours"], min_battery, max_battery)
        rating_s = normalize(p["rating"], min_rating, max_rating)

        cpu_s = cpu_score(p["processor"])
        ram_s = min(p["ram_gb"] / 32, 1)

        performance_s = (cpu_s + ram_s) / 2
        eco_s = 1

        final_score = (
            weights.get("price", 0) * price_s +
            weights.get("performance", 0) * performance_s +
            weights.get("battery", 0) * battery_s +
            weights.get("rating", 0) * rating_s +
            weights.get("eco", 0) * eco_s   # if you compute eco_s
        )

        p["score"] = round(final_score, 4)

        scored_products.append(p)

    scored_products.sort(key=lambda x: x["score"], reverse=True)

    return scored_products