from sqlalchemy.orm import Session
from app import models
from app.services.normalizer import normalize_product

def fetch_laptop_data(db: Session):
    """
    Joins laptops, specs, and listings into a flat structure
    suitable for scoring engine
    """

    results = (
        db.query(
            models.Laptop.id,
            models.Laptop.name,
            models.Laptop.average_rating,
            models.LaptopSpecs.processor,
            models.LaptopSpecs.ram_gb,
            models.LaptopSpecs.battery_hours,
            models.ProductListing.price
        )
        .join(models.LaptopSpecs, models.Laptop.id == models.LaptopSpecs.laptop_id)
        .join(models.ProductListing, models.Laptop.id == models.ProductListing.laptop_id)
        .all()
    )

    products = []

    for r in results:
        products.append(
            normalize_product({
                "id": r.id,
                "name": r.name,
                "price": int(r.price) if r.price else 0,
                "battery_hours": r.battery_hours or 0,
                "rating": r.average_rating or 0,
                "processor": r.processor or "",
                "ram_gb": r.ram_gb or 0
            }, "laptops")
        )

    return products