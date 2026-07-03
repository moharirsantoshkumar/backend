from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DECIMAL, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime

from app.archive.database import Base


# ------------------------
# Brand Table
# ------------------------
class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    laptops = relationship("Laptop", back_populates="brand")


# ------------------------
# Laptop Table
# ------------------------
class Laptop(Base):
    __tablename__ = "laptops"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.id"))
    model_number = Column(String(100))
    average_rating = Column(Float)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="laptops")
    specs = relationship("LaptopSpecs", back_populates="laptop", uselist=False)
    listings = relationship("ProductListing", back_populates="laptop")


# ------------------------
# Laptop Specs Table
# ------------------------
class LaptopSpecs(Base):
    __tablename__ = "laptop_specs"

    id = Column(Integer, primary_key=True, index=True)
    laptop_id = Column(Integer, ForeignKey("laptops.id"))

    processor = Column(String(100))
    ram_gb = Column(Integer)
    storage_gb = Column(Integer)
    storage_type = Column(String(50))

    battery_hours = Column(Float)
    weight_kg = Column(Float)

    screen_size_inches = Column(Float)
    resolution = Column(String(50))

    gpu = Column(String(100))
    os = Column(String(50))

    laptop = relationship("Laptop", back_populates="specs")


# ------------------------
# Product Listings Table
# ------------------------
class ProductListing(Base):
    __tablename__ = "product_listings"

    id = Column(Integer, primary_key=True, index=True)
    laptop_id = Column(Integer, ForeignKey("laptops.id"))

    retailer = Column(String(100))
    price = Column(DECIMAL(10, 2))
    currency = Column(String(10))

    product_url = Column(String)
    in_stock = Column(Boolean, default=True)

    last_updated = Column(TIMESTAMP, default=datetime.utcnow)

    laptop = relationship("Laptop", back_populates="listings")