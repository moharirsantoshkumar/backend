from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.product_service import fetch_laptop_data
from app.services.scoring import calculate_scores

from app.services.ai_service import generate_explanation

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

# -------------------------
# DB Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# Health Check
# -------------------------
@app.get("/")
def root():
    return {"message": "ClariCart API running"}


# -------------------------
# Recommendation API
# -------------------------
@app.post("/recommendations")
def get_recommendations(preferences: dict, db: Session = Depends(get_db)):

    # Fetch products
    products = fetch_laptop_data(db)

    # Default weights
    weights = preferences.get("weights", {
        "price": 0.4,
        "performance": 0.3,
        "battery": 0.2,
        "rating": 0.1
    })

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

        if score_gap > 0.1:
            best["confidence"] = "High"
        elif score_gap > 0.05:
            best["confidence"] = "Medium"
        else:
            best["confidence"] = "Low"

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
    return {
        "top_recommendation": best,
        "alternatives": alternatives
    }