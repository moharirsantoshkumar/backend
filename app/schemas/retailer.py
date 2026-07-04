from pydantic import BaseModel


class RetailerPrice(BaseModel):
    retailer: str
    price: float
    currency: str
    product_url: str
    in_stock: bool
    delivery_days: int | None = None
    seller: str | None = None