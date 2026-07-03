from app.services.providers.dummyjson_provider import get_prices as dummyjson_provider

from app.services.providers.search_provider import get_prices as search_provider

PROVIDERS = [
    dummyjson_provider,
    search_provider,
]


def fetch_prices(product):
    prices = []

    for provider in PROVIDERS:
        try:
            prices.extend(provider(product))
        except Exception as ex:
            from app.logger import logger
            logger.exception(
                "Provider %s failed",
                provider.__name__,
            )

    return prices