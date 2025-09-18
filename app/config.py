class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI  = 'mysql+mysqlconnector://root:Hillzz%4069@localhost/library_db'
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    pass



