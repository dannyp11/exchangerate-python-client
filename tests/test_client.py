import pytest
from exchangerate.client import ExchangerateClient

def assert_currency_exist(result):
    for currency in ["USD", "CAD", "AUD"]:
        assert currency in result

def test_get_symbols():
    client = ExchangerateClient()
    all_symbols = client.symbols()
    assert_currency_exist(all_symbols)

def test_get_latest_rate():
    client = ExchangerateClient()
    assert_currency_exist(client.latest())
    assert_currency_exist(client.latest(amount=5))

    selected_rates = client.latest(symbols=["JPY", "CHF"], amount=5)
    assert "JPY" in selected_rates
    assert "CHF" in selected_rates
