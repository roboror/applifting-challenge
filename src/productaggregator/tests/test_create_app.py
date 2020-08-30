class TestConfig:
    def test_production(self):
        from ..app import create_app
        app = create_app('ProductionConfig')
        assert (not app.config.get('DEBUG'))
        assert (not app.config.get('TESTING'))

    def test_develop_and_testing(self):
        from ..app import create_app
        app_development = create_app('DevelopmentConfig')
        assert app_development.config.get('DEBUG')

        app_testing = create_app('TestingConfig')
        assert app_testing.config.get('TESTING')

        assert (app_development.config.get('SQLALCHEMY_DATABASE_URI') != app_testing.config.get(
            'SQLALCHEMY_DATABASE_URI'))
