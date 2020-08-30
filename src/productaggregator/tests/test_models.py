import uuid

from sqlalchemy.exc import IntegrityError

from models import OffersMsRegistration, Product, OffersBatch


class TestProduct:
    def test_creation(self, db, create_and_commit):
        p = create_and_commit(Product, name='test')
        assert (isinstance(p.id, int))
        p = create_and_commit(Product, name='test2', description='123')
        assert (isinstance(p.id, int))

    def test_missing_name(self, db, create_and_commit):
        try:
            create_and_commit(Product, description='123')
            assert False
        except IntegrityError as e:
            assert ('name' in str(e))

    def test_multiple(self, db, create_and_commit):
        ids = set()
        for i in range(10):
            p = create_and_commit(Product, name='test', description='123')  # name can be duplicate
            assert (p.id not in ids)
            ids.add(p.id)

    def test_uuid(self, db, create_and_commit):
        p = create_and_commit(Product, name='test')
        assert (isinstance(p.uuid, uuid.UUID))


class TestOffersMsRegistration:
    def test_get_access_token(self, db):
        new_uuid_str = str(uuid.uuid4())

        def dummy_retrieve_access_token():
            dummy_retrieve_access_token.cnt += 1
            return new_uuid_str

        dummy_retrieve_access_token.cnt = 0

        for i in range(10):
            access_token = OffersMsRegistration.get_access_token(dummy_retrieve_access_token)
            assert (access_token == new_uuid_str)

        assert (dummy_retrieve_access_token.cnt == 1)


class TestOffersBatch:
    def test_creation(self, create_and_commit):
        ob = create_and_commit(OffersBatch)
        assert (ob.id is not None)
