import requests
from collections import namedtuple
from urllib.parse import urlencode, urlunparse

from .config import Region
from .exceptions import *

class ExchangerateClient:
    """
    Primary client class
    """
    def __init__(self, server_region=Region.AMERICA):
        self.server_region = server_region
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
        return resp_json.get("rates")

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
            resp = self.session.get(url)
            if resp.status_code != 200:
                raise ResponseErrorException("Status code=%d calling url=%s" % (resp.status_code, url))

            resp_json = resp.json()
            if not resp_json.get("success", False):
                raise ResponseErrorException("No success field calling url=%s" % (url))

            return resp_json

    def _build_url(self, path="", params=None):
        Components = namedtuple(
            typename='Components',
            field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
        )

        if not params:
            params = {}

        return urlunparse(
            Components(
                scheme='https',
                netloc=self.server_region.value,
                query=urlencode(params),
                path=path,
                url="/",
                fragment=""
            )
        )
