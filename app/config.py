from distutils.debug import DEBUG

class Config:
    SECRET_KEY = "28cd865235dc750028fc3b28"
class DevelopmentConfig(Config):
    DEBUG = True
    #DB
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "123456"
    MYSQL_DB = "test"
config = {
    "development": DevelopmentConfig
}