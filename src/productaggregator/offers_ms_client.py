import os
from functools import cached_property
from typing import Dict, List, Any

import requests
from flask import current_app, abort

from models import Product, OffersMsRegistration
from schemas import product_schema_external

DEFAULT_OFFERS_MS_BASE_URL = 'https://applifting-python-excercise-ms.herokuapp.com/api/v1'
OFFERS_MS_BASE_URL = os.environ.get('OFFERS_MS_BASE_URL', DEFAULT_OFFERS_MS_BASE_URL).rstrip('/')
OFFERS_URLS = {
    'auth': f'{OFFERS_MS_BASE_URL}/auth',
    'register_product': f'{OFFERS_MS_BASE_URL}/products/register',
    'get_offers': lambda product: f'{OFFERS_MS_BASE_URL}/products/{str(product.uuid)}/offers'
}


def abort_503():
    abort(503, {'message': 'Call to external service failed.'})


class OffersMsClient:
    """Responsible for making calls to Offers MS.

    `OFFERS_MS_BASE_URL` can be configured via env var.
    access_token is stored on instance and uses @cached_property

    >>> oms = OffersMsClient()
    >>> success = oms.register_product(product)
    >>> for offer_data_raw in oms.extract_offers(product):
    >>>     ...
    """

    def register_product(self, product: Product) -> bool:
        """Register product in Offers MS using its uuid.

        Abort with 503 if response not ok.

        :param product:
        :return: success
        """
        url = OFFERS_URLS['register_product']
        data = product_schema_external.dump(product)

        current_app.logger.info(f'Registering product with uuid={data["id"]} and headers {self._headers}')
        r = requests.post(url=url, headers=self._headers, data=data)
        if r.status_code:
            return True
        # elif r.status_code == 401:  # TODO get new access_token?
        else:
            current_app.logger.error(f'register_product({product}) failed', response=r)  # TODO retry, ...
            abort_503()

    def extract_offers(self, product: Product) -> List[Dict[str, Any]]:
        """Get raw offers_data from Offers MS.

        :param product:
        :return:
        """
        url = OFFERS_URLS['get_offers'](product)
        r = requests.get(url, headers=self._headers)
        if not r.ok:
            current_app.logger.error(f'extract_offers({product}) failed', response=r)
            return []

        return r.json()

    @staticmethod
    def _extract_access_token() -> str:  # TODO error handling
        url = OFFERS_URLS['auth']
        current_app.logger.info('Calling auth.')
        r = requests.post(url=url)
        return r.json()['access_token']

    @cached_property
    def get_access_token(self) -> str:
        return OffersMsRegistration.get_access_token(self._extract_access_token)

    @property
    def _headers(self) -> Dict[str, str]:
        return {'Bearer': self.get_access_token}
