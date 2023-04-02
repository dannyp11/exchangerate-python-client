import requests
from collections import namedtuple
from urllib.parse import urlencode, urlunparse

from .config import Region
from .exceptions import *

class ExchangerateClient:
    """
    Primary client class
    """
    def __init__(self, base_currency="USD", region=Region.AMERICA):
        self.base_currency = base_currency
        self.region = region
        self.session = requests.Session()

    # -------------------------------------------------------------------
    # Public methods
    # -------------------------------------------------------------------

    def symbols(self):
        url = self._build_url(path="symbols")
        resp_json = self._validate_and_get_json(url)
        return resp_json.get("rates")

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
                netloc=self.region.value,
                query=urlencode(params),
                path=path,
                url="/",
                fragment=""
            )
        )
