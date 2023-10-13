import requests
from urllib.parse import urlencode

from .exceptions import *

class ExchangerateClient:
    """
    Primary client class
    @param api_key: the api key from https://apilayer.com/marketplace/fixer-api#documentation-tab
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    # -------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------
    def symbols(self):
        """
        Get list of supported symbols
        """
        url = self._build_url(path="symbols")
        resp_json = self._validate_and_get_json(url)
        return resp_json.get("symbols").keys()

    def latest(self, base_currency="USD", symbols=None, amount=1):
        """
        Get latest rate

        @param base_currency:   the base currency
        @param symbols:         list of currencies, None if including all
        @param amount:          the currency amount
        """
        params = {"amount": amount, "base": base_currency}
        if symbols: params["symbols"] = ",".join(symbols)

        url = self._build_url(path="latest", params=params)
        resp_json = self._validate_and_get_json(url)
        return resp_json.get("rates")

    # -------------------------------------------------------------------
    # Private methods
    # -------------------------------------------------------------------
    def _validate_and_get_json(self, url):
            headers = {"apikey": self.api_key}
            resp = self.session.get(url, headers=headers)
            if resp.status_code != 200:
                raise ResponseErrorException("Status code=%d calling url=%s" % (resp.status_code, url))

            resp_json = resp.json()
            if not resp_json.get("success", False):
                raise ResponseErrorException("No success field calling url=%s" % (url))

            return resp_json

    def _build_url(self, path="", params=None):
        url = "https://api.apilayer.com/fixer/"
        if path:
            url += path

        if params:
            url += f"?{urlencode(params)}"

        return url
