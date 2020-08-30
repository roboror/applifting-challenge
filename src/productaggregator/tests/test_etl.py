import json
from datetime import datetime

import pytest

from etl import retrieve_new_offers
from models import Product, OffersBatch, Offer
from offers_ms_client import OFFERS_URLS


class TestRetrieveNewOffers:
    @pytest.mark.parametrize('offers_data', [
        [],
        [{'id': 7871, 'price': 546, 'items_in_stock': 0}, {'id': 9376, 'price': 763, 'items_in_stock': 6},
         {'id': 9788, 'price': 916, 'items_in_stock': 0}, {'id': 8011, 'price': 1096, 'items_in_stock': 0},
         {'id': 7874, 'price': 1109, 'items_in_stock': 0}, {'id': 9359, 'price': 1176, 'items_in_stock': 0},
         {'id': 25819, 'price': 1184, 'items_in_stock': 0}, {'id': 9377, 'price': 1219, 'items_in_stock': 0},
         {'id': 9858, 'price': 1267, 'items_in_stock': 0}, {'id': 9699, 'price': 1277, 'items_in_stock': 0},
         {'id': 9214, 'price': 1320, 'items_in_stock': 9}, {'id': 7870, 'price': 1442, 'items_in_stock': 6},
         {'id': 9212, 'price': 1444, 'items_in_stock': 15}, {'id': 8304, 'price': 1536, 'items_in_stock': 0},
         {'id': 8045, 'price': 1568, 'items_in_stock': 0}, {'id': 25838, 'price': 1593, 'items_in_stock': 58},
         {'id': 8316, 'price': 1647, 'items_in_stock': 0}, {'id': 25817, 'price': 1649, 'items_in_stock': 58},
         {'id': 25774, 'price': 1767, 'items_in_stock': 17}, {'id': 8358, 'price': 2029, 'items_in_stock': 9},
         {'id': 9732, 'price': 3666, 'items_in_stock': 0}],
        [{}, {'bad': 'bas'}, {'price': 50}, {'id': 'a'}, {'id': 123, 'price': 'devet'}],
    ])
    def test_basic(self, db, create_and_commit, mocked_offers_ms, offers_data):
        products = [create_and_commit(Product, name='test'), create_and_commit(Product, name='test2')]
        for p in products:
            url = OFFERS_URLS['get_offers'](p)
            mocked_offers_ms.register_uri('GET', url, status_code=200, text=json.dumps(offers_data))

        retrieve_new_offers()

        assert (OffersBatch.query.count() == 1)
        ob = OffersBatch.query.first()
        assert (isinstance(ob.created_date, datetime))

        for o in Offer.query.all():
            assert (o.product_id in set([p.id for p in products]))
            assert (o.offers_batch_id is not None)
