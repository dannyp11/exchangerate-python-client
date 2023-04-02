from exchangerate.client import ExchangerateClient

def test_get_symbols():
    client = ExchangerateClient()
    all_symbols = client.symbols()

    assert "USD" in all_symbols
    assert "CAD" in all_symbols
    assert "AUD" in all_symbols
