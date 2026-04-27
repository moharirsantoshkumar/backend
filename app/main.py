from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends
from app.database import Base, engine
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.product_service import fetch_laptop_data
from app.services.scoring import calculate_scores

from app.services.ai_service import generate_explanation

app = FastAPI()
Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.database import SessionLocal
from app.models import Brand, Laptop, LaptopSpecs, ProductListing

def seed_data():
    db = SessionLocal()

    if db.query(Laptop).first():
        db.close()
        return  # already has data

    brand1 = Brand(name="Asus")
    brand2 = Brand(name="HP")
    brand3 = Brand(name="Lenovo")

    db.add_all([brand1, brand2, brand3])
    db.commit()

    laptop1 = Laptop(name="Asus Vivobook 15", brand_id=brand1.id, average_rating=4.1)
    laptop2 = Laptop(name="HP Pavilion 14", brand_id=brand2.id, average_rating=4.2)
    laptop3 = Laptop(name="Lenovo ThinkPad E14", brand_id=brand3.id, average_rating=4.6)

    db.add_all([laptop1, laptop2, laptop3])
    db.commit()

    specs1 = LaptopSpecs(laptop_id=laptop1.id, processor="Intel i5 12th Gen", ram_gb=16, battery_hours=7)
    specs2 = LaptopSpecs(laptop_id=laptop2.id, processor="Intel i5 12th Gen", ram_gb=8, battery_hours=8)
    specs3 = LaptopSpecs(laptop_id=laptop3.id, processor="Intel i7 12th Gen", ram_gb=16, battery_hours=10)

    db.add_all([specs1, specs2, specs3])
    db.commit()

    listing1 = ProductListing(laptop_id=laptop1.id, retailer="Amazon", price=55000)
    listing2 = ProductListing(laptop_id=laptop2.id, retailer="Flipkart", price=60000)
    listing3 = ProductListing(laptop_id=laptop3.id, retailer="Amazon", price=78000)

    db.add_all([listing1, listing2, listing3])
    db.commit()

    db.close()

seed_data()




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