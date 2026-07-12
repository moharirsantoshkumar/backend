from app.services.pricing_service import enrich_with_pricing
from app.services.confidence_service import calculate_confidence
from app.services.advisor_service import generate_buying_advice
from app.services.consensus_service import generate_consensus


def enrich_product(product: dict) -> dict:

    enrich_with_pricing(product)

    product["confidence"] = calculate_confidence(product)
    product["advisor"] = generate_buying_advice(product)
    product["consensus"] = generate_consensus(product)

    return product