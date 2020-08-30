from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_restful_swagger import swagger

from models import db
from resources import ProductListResource, ProductResource


def handle_not_found(e):
    """Return json instead of html

    """
    return {'message': 'Not found.'}, 404


def handle_bad_request(e):
    return {'message': 'Bad request.'}, 400


def handle_internal_error(e):
    db.session.rollback()
    return {'message': 'Internal server error.'}, 500


def create_app(config_cls: str = 'ProductionConfig'):
    app = Flask(__name__)
    app.config.from_object(f'config.{config_cls}')

    app.register_error_handler(400, handle_bad_request)
    app.register_error_handler(404, handle_not_found)
    app.register_error_handler(500, handle_internal_error)

    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app, db)

    api = Api(app)
    api = swagger.docs(api, apiVersion='0.1')
    api.add_resource(ProductListResource, '/products/')
    api.add_resource(ProductResource, '/products/<int:product_id>/')

    return app
