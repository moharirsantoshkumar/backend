from app.services.providers.provider_registry import fetch_prices


def get_retailer_prices(product):
    return fetch_prices(product)