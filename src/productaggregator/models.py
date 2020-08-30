import datetime
import uuid
from typing import Callable

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class SerialIdModel(db.Model):
    """Abstract model with the standard id field.

    """
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)


class OffersMsRegistration(SerialIdModel):
    access_token = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def get_access_token(cls, extract_access_token: Callable[[], str]) -> str:
        """This is the only way to interact with this table.

        Acts as a single value store for the access_token. In case of first call, the `extract_access_token` function
        is called.
        :param extract_access_token:
        :return:
        """
        omr = db.session.query(cls).first()
        if omr is None:
            access_token = extract_access_token()
            omr = cls(access_token=access_token)
            db.session.add(omr)
            db.session.commit()
        return str(omr.access_token)


class OffersBatch(SerialIdModel):
    created_date = db.Column(DateTime, default=datetime.datetime.utcnow)


class Offer(SerialIdModel):
    """Represents a product offer in a particular time (OfferBatch).

    Instead of updating, a new record is created for each new retrieved offer.
    Unique index on (product, id_external, offers_batch)
    """
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    id_external = db.Column(db.Integer, nullable=False)
    offers_batch_id = db.Column(db.Integer, db.ForeignKey('offers_batch.id'), nullable=False)

    price = db.Column(db.Integer())
    items_in_stock = db.Column(db.Integer())

    __table_args__ = (
        UniqueConstraint('product_id', 'id_external', 'offers_batch_id', name='_id_external_product_batch_uc'),
    )


class Product(SerialIdModel):
    """UUID is generated for each product although serial id is used in CRUD interface.

    """
    uuid = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    name = db.Column(db.Text(), nullable=False)
    description = db.Column(db.Text())

    offers = db.relationship('Offer', backref='product', lazy=True)
