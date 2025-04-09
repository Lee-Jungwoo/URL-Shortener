class Config(object):
    """
    Base configuration class. Default to Production settings.
    """
    DEBUGGING = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://admin:0225@localhost/urlshortener"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CLIENT_URL = "https://linkshorty.in"
    API_URL = "https://linkshorty.in/api"
    REDIRECT_URL = "https://linkshorty.in"

class DevelopmentConfig(Config):
    """
    Development configuration class.
    """
    DEBUGGING = True

    CLIENT_URL = "http://localhost:5500"
    API_URL = "http://localhost:5000/api"
    REDIRECT_URL = "http://localhost:5000"

class ProductionConfig(Config):
    """
    Production configuration class.
    """
    DEBUGGING = False
    TESTING = False

class TestingConfig(Config):
    """
    Testing configuration class.
    """
    TESTING = True
    DEBUGGING = False
    


    