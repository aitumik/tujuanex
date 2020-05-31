from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .tujuanex.controllers import main as main_blueprint
    from .auth.controllers import auth as auth_blueprint
    app.register_blueprint(main_blueprint,url_prefix="/api/v1")
    app.register_blueprint(auth_blueprint,url_prefix="/api/v1/auth/")

    return app