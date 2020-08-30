import os


class Config:
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # provided by Heroku
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://pa:papa@db/pa'


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://pa:papa@db_test/pa'
