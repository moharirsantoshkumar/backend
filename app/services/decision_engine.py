from app.services.ai_service import generate_explanation
from app.services.external_api_service import fetch_external_products
from app.services.pricing_service import enrich_with_pricing
from app.services.scoring import calculate_scores
from app.services.mobile_service import fetch_mobile_data
from app.services.response_builder import build_response
from app.services.product_enrichment_service import enrich_product

def generate_recommendations(preferences: dict):
    # Fetch products based on category
    category = preferences.get("category", "laptops")

    products = fetch_external_products(category)

    if not products:
        return {
            "message": f"No products found for category '{category}'"
        }

    incoming = preferences.get("weights", {})

    # 🔁 Map UI → backend keys
    weights = {
        "price": incoming.get("Price sensitivity", 0.4),
        "battery": incoming.get("Delivery speed", 0.2),
        "performance": incoming.get("Brand trust", 0.3),
        "rating": incoming.get("Review depth", 0.1),
        "eco": incoming.get("Sustainability", 0)
    }

    # Score products
    scored = calculate_scores(products, weights)

    top_products = scored[:3]

    if not top_products:
        return {"message": "No products found"}

    best = top_products[0]
    best["verdict"] = "Recommended"
    alternatives = top_products[1:]

    # -------------------------
    # AI Explanation
    # -------------------------
    for p in top_products:
        p["explanation"] = generate_explanation(p, weights)
    for p in top_products:
        enrich_product(p)
    
    # -------------------------
    # Comparison Logic
    # -------------------------
    if len(top_products) > 1:
        second = top_products[1]

        price_diff = int(abs(second["price"] - best["price"]))
        battery_diff = int(abs(second["battery_hours"] - best["battery_hours"]))

        best["decision_summary"] = "Best overall value based on your preferences"
        

        best["tradeoff_vs_next"] = (
            f"You save ₹{price_diff}, but get {battery_diff} hour{'s' if battery_diff != 1 else ''} less battery compared to {second['name']}."
        )

        # Confidence logic
        score_gap = best["score"] - second["score"]

        # if score_gap > 0.1:
        #     best["confidence"] = second["confidence"]
        # elif score_gap > 0.05:
        #     best["confidence"] = second["confidence"]
        # else:
        #     best["confidence"] = second["confidence"]

    # -------------------------
    # Best For Tag
    # -------------------------
    if weights["price"] >= 0.4:
        best["best_for"] = "Budget-conscious users"
    elif weights["performance"] >= 0.4:
        best["best_for"] = "Performance-focused users"
    else:
        best["best_for"] = "Balanced everyday use"

    # -------------------------
    # Final Response
    # -------------------------
    return build_response(
        category,
        best,
        alternatives,
    )