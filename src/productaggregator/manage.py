from flask_script import Manager

import etl
from app import create_app

app_ = create_app('ProductionConfig')
manager = Manager(app_)


# manager = Manager(create_app)
# manager.add_option('-c', '--config_cls', dest='config_cls', required=False, default='ProductionConfig')


@manager.command
def retrieve_new_offers():
    return etl.retrieve_new_offers()


if __name__ == '__main__':
    manager.run()
