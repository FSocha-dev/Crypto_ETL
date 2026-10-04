from unittest.mock import Mock, patch

from get_crypto_prices import get_crypto_prices


@patch("get_crypto_prices.requests.get")
def test_get_crypto_prices_returns_api_data(mock_get: Mock) -> None:
    expected_data = {
        "bitcoin": {
            "usd": 65000,
            "usd_market_cap": 1_200_000,
        }
    }
    mock_response = Mock()
    mock_response.json.return_value = expected_data
    mock_get.return_value = mock_response

    result = get_crypto_prices(ids="bitcoin", vs_currencies="usd")

    assert result == expected_data
    mock_get.assert_called_once_with(
        "https://api.coingecko.com/api/v3/simple/price",
        params={
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
            "include_last_updated_at": "true",
        },
        timeout=10,
    )
    mock_response.raise_for_status.assert_called_once_with()
