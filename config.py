class Config(object):
    """
    Base configuration class. Default to Production settings.
    """
    DEBUGGING = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CLIENT_URL = "https://linkshorty.in"
    # REDIRECT_URL = "https://linkshorty.in"
    CLIENT_URL = "linkshorty.in"
    API_URL = "https://linkshorty.in/api"
    REDIRECT_URL = "linkshorty.in"
    # deleted https:// from the URLs to look shorter when displayed on web

class DevelopmentConfig(Config):
    """
    Development configuration class.
    """
    DEBUGGING = True

    CLIENT_URL = "localhost:5000"
    API_URL = "http://localhost:5000/api"
    REDIRECT_URL = "localhost:5000"

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
    


    
