import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SECRET_KEY = "thisisverysecret"
    ADMIN_EMAIL = "nathan@tujuanex.com"
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    MAIL_SERVER = "smtp.google.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    SQLALCHEMY_DATABASE_URI="sqlite:////" + os.path.join(base_dir,"data-dev.sqlite")

class TestingConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + os.path.join(base_dir,'data-test.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:////" + os.path.join(base_dir,'data-prod.sqlite')


config = {
        "default":DevelopmentConfig,
        "development":DevelopmentConfig,
        "testing":TestingConfig,
        "production":ProductionConfig
    }
