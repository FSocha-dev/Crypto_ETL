import requests


def get_crypto_prices(
    ids: str = "bitcoin,ethereum,solana",
    vs_currencies: str = "usd",  
) -> dict:
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ids,
        "vs_currencies": vs_currencies,
        "include_market_cap": "true",
        "include_24hr_vol": "true",
        "include_24hr_change": "true",
        "include_last_updated_at": "true",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()
