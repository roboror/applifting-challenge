import pytest

from models import Product


class TestProductListResource:
    url = '/products/'

    def test_get_list_empty(self, client):
        r = client.get(self.url)
        assert (r.status_code == 200)
        assert (r.json == [])

    @pytest.mark.parametrize('n', [0, 1, 2, 5, 10])
    def test_get_list_non_empty(self, db, client, create_and_commit, n):
        for i in range(n):
            create_and_commit(Product, name='test')
        r = client.get(self.url)
        response_data = r.json
        assert (r.status_code == 200)
        assert (len(response_data) == n)
        for p in response_data:
            assert (p['name'] == 'test')
            assert (p['description'] is None)
            assert (p['id'] is not None)

    @pytest.mark.parametrize(
        'data, expected_code', [
            ('', 400),
            ({}, 400),

            ({"name": "real"}, 201),
            ({"name": "the realest", "description": "so real"}, 201),
            ({"name": "big!@#!#!@#157____  1231  3123 1" * 4096}, 201),

            ({'name': None}, 422),
            ({'description': 'so real'}, 422),
            ({'nono': 'bono'}, 422),
            ({'name': 9}, 422),
            ({'name': 'nice', 'description': 123}, 422),
        ]

    )
    def test_create_single(self, db, client, data, expected_code, mocked_offers_ms):
        r = client.post(self.url, json=data)
        assert (r.status_code == expected_code)
        if r.status_code == 201:
            response_data = r.json
            assert ('id' in response_data)
            for k, v in data.items():
                assert (response_data[k] == v)


class TestProductResource:
    def get_url(self, product: Product):
        return f'/products/{str(product.id)}/'

    def test_get_single(self, db, client, create_and_commit):
        p = create_and_commit(Product, name='test')
        url = self.get_url(p)
        r = client.get(url)
        assert (r.status_code == 200)
        p_data = r.json
        for attr in ['id', 'name', 'description']:
            assert p_data[attr] == getattr(p, attr)

    @pytest.mark.parametrize('patch_data', [
        {'name': '7'},
        {'name': '7', 'description': 'new one'},
        {'name': '7', 'description': None},
        {'description': 'new one'},
    ])
    def test_update_delete_404(self, db, client, create_and_commit, patch_data):
        p = create_and_commit(Product, name='test')
        url = self.get_url(p)
        r = client.patch(url, json=patch_data)
        assert (r.status_code == 200 and 'id' in r.json)
        r = client.delete(url)
        assert (r.status_code == 204)
        r = client.get(url)
        assert (r.status_code == 404)
