"""Inspired mostly by http://boussejra.com/2018/08/01/testing-with-flask.html

Using scope=function to have fresh isolated db for each test.

"""
import uuid

import pytest

from models import db as db_


@pytest.fixture(scope='function')
def app():
    """Yield your app with its context set up and ready"""
    from ..app import create_app
    app_ = create_app('DevelopmentConfig')
    with app_.app_context():
        yield app_


@pytest.fixture(scope='function')
def db(app):
    db_.drop_all()
    db_.create_all()  # couldn't manage to get flask_migrate.upgrade() to work correctly
    return db_


@pytest.fixture(scope='function')
def client(app):
    """Get a test client for your Flask app"""
    with app.test_client() as client_:
        yield client_


@pytest.fixture(scope='function')
def create_and_commit(db):
    def _create_and_commit(model, **data):
        inst = model(**data)
        assert (inst.id is None)
        db.session.add(inst)
        db.session.commit()
        return inst

    return _create_and_commit


@pytest.fixture(scope='function')
def mocked_offers_ms(requests_mock):
    from offers_ms_client import OFFERS_URLS

    uuid_str = str(uuid.uuid4())

    requests_mock.register_uri('POST', OFFERS_URLS['auth'], status_code=200, text='{"access_token":"' + uuid_str + '"}')
    requests_mock.register_uri('POST', OFFERS_URLS['register_product'], status_code=200, text='{}')

    return requests_mock
