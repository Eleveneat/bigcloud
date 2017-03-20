# -*- encoding: utf-8 -*-
# Copyright 2016 Vinzor Co.,Ltd.
#
# 2016/12/22 Chen Weijian : Init

import os
import logging
from config import config
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, ALL, patch_request_class

if __name__.find('.') > 0:
    flask_name = __name__.split('.')[0]
else:
    flask_name = __name__


class HackedSQLAlchemy(SQLAlchemy):
    """A simple hack to support isolation level"""

    def apply_driver_hacks(self, app, info, options):
        if app.config.get('SQLALCHEMY_ISOLATION_LEVEL'):
            options['isolation_level'] = app.config['SQLALCHEMY_ISOLATION_LEVEL']
        elif info.drivername.startswith('mysql'):
            options['isolation_level'] = 'READ COMMITTED'
        elif info.drivername == 'sqlite':
            options['isolation_level'] = 'READ UNCOMMITTED'
        super(HackedSQLAlchemy, self).apply_driver_hacks(app, info, options)


app = Flask(flask_name)
db = HackedSQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = ''

patch_request_class(app, 1024 * 1024 * 1024)
upload = UploadSet('upload', ALL)

logger = app.logger


def create_app(config_name):
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.config['UPLOADED_UPLOAD_DEST'] = os.path.abspath('upload_files')
    configure_uploads(app, upload)

    login_manager.init_app(app)

    db.init_app(app)

    handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

    # register blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .connect import connect as connect_blueprint
    app.register_blueprint(connect_blueprint, url_prefix='/connect')

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint, url_prefix='/home')

    from .monitor import monitor as monitor_blueprint
    app.register_blueprint(monitor_blueprint, url_prefix='/monitor')

    from .push import push as push_blueprint
    app.register_blueprint(push_blueprint, url_prefix='/push')

    from .file import file as file_blueprint
    app.register_blueprint(file_blueprint, url_prefix='/file')

    from .remote import remote as remote_blueprint
    app.register_blueprint(remote_blueprint, url_prefix='/remote')

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app


app = create_app(os.environ.get('FLASK_CONFIG') or 'default')
