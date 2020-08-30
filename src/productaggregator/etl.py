from flask import current_app
from marshmallow import ValidationError

from models import OffersBatch, db, Product, Offer
from offers_ms_client import OffersMsClient
from schemas import offers_schema_external


def retrieve_new_offers() -> None:
    """Extract and store offers from the Offers MS for each product.

    First creates OffersBatch record to which all created offers are tied.
    Ignores offers not matching the schema or empty responses
    :return:
    """
    oms = OffersMsClient()

    ob = OffersBatch()
    db.session.add(ob)

    for p in Product.query.all():
        for offer_data_raw in oms.extract_offers(p):
            try:
                offer_data = offers_schema_external.load(offer_data_raw)
                offer_data['id_external'] = offer_data.pop('id')
            except (ValidationError, KeyError) as e:
                current_app.logger.warning(
                    f'offer validation failed with {getattr(e, "messages", str(e))} {offer_data_raw=}')
                continue

            o = Offer(product_id=p.id, offers_batch_id=ob.id, **offer_data)
            db.session.add(o)

    db.session.commit()
