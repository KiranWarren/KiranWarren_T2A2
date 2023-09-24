import os


class BaseConfig(object):
    @property
    def SQLALCHEMY_DATABASE_URI(self):

        db = os.environ.get("SQLALCHEMY_DATABASE_URI")

        if db is None:
            raise ValueError("Missing environment variable value for `SQLALCHEMY_DATABASE_URI`.")

        return db
    
    @property
    def JWT_SECRET_KEY(self):

        jsk = os.environ.get("JWT_SECRET_KEY")

        if jsk is None:
            raise ValueError("Missing environment variable value for `JWT_SECRET_KEY`.")
        
        return jsk
    

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class TestingConfig(DevelopmentConfig):
    pass
    

class ProductionConfig(DevelopmentConfig):
    pass


current_env = os.environ.get("FLASK_ENV")

if current_env == "production":
    app_config = ProductionConfig()
elif current_env == "testing":
    app_config = TestingConfig()
else:
    app_config = DevelopmentConfig()
