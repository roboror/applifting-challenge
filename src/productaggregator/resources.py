from flask import request
from flask_restful import Resource

from models import db, Product
from offers_ms_client import OffersMsClient
from schemas import product_schema, product_schema_list, product_schema_partial, validate_data

oms_client = OffersMsClient()


# TODO add swagger annotations
class ProductListResource(Resource):
    def get(self):
        """Retrieve array of all products.

        :return:
        """
        products = Product.query.all()
        return product_schema_list.dump(products)

    def post(self):
        """Create a new product.

        :return:
        """
        data = validate_data(request.get_json(), product_schema)
        product = Product(**data)
        db.session.add(product)
        db.session.commit()

        oms_client.register_product(product)  # TODO could use background worker
        return product_schema.dump(product), 201


class ProductResource(Resource):
    def get(self, product_id):
        """Retrieve a single product.

        :param product_id: Product.id
        :return:
        """
        product = Product.query.get_or_404(product_id)

        return product_schema.dump(product)

    def patch(self, product_id):
        """Update an existing product's fields.

        :param product_id:
        :return:
        """
        product = Product.query.get_or_404(product_id)
        data = validate_data(request.get_json(), product_schema_partial)

        for k, v in data.items():
            setattr(product, k, v)
        db.session.commit()

        return product_schema.dump(product)

    def delete(self, product_id):
        """Delete an existing product.

        :param product_id:
        :return:
        """
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return '', 204
