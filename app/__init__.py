from flask_api import FlaskAPI,status,exceptions
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from config import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name):
    app = FlaskAPI(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    jwt.init_app(app)

    from .tujuanex.controllers import main as main_blueprint
    from .auth.controllers import auth as auth_blueprint
    from .home.controllers import home as home_blueprint

    app.register_blueprint(main_blueprint,url_prefix="/api/v1")
    app.register_blueprint(home_blueprint,url_prefix="/")
    app.register_blueprint(auth_blueprint,url_prefix="/api/v1/auth/")

    return app
