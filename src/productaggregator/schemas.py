from flask import abort
from marshmallow import Schema, ValidationError, fields


class OfferSchemaExternal(Schema):
    id = fields.Int()
    price = fields.Int()
    items_in_stock = fields.Int()


offers_schema_external = OfferSchemaExternal()


class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    # TODO add nested offers read-only


product_schema = ProductSchema()
product_schema_partial = ProductSchema(partial=('name',))
product_schema_list = ProductSchema(many=True)


class ProductSchemaExternal(ProductSchema):
    """Uses uuid instead of serial pk.

    """
    id = fields.Function(lambda obj: str(obj.uuid))


product_schema_external = ProductSchemaExternal()


def validate_data(raw_data: dict, schema: Schema) -> dict:
    """Helper to load and validate raw_data using schema.

    Uses flask.abort to throw http errors 400 or 422 with appropriate messages.

    :param raw_data: dict of raw data from request body
    :param schema: marshmallow.Schema
    :return: validated data
    """
    if not raw_data:
        return abort(400, {'message': 'No input data provided'})
    try:
        return schema.load(raw_data)
    except ValidationError as e:
        return abort(422, {'message': e.messages})
