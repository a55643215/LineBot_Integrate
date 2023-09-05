import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://integratelinebot:ryZcECKSVuEl80HwA9VLUhmi55KFenyT@dpg-cjrr8vojbais73fe0g5g-a.singapore-postgres.render.com/integratelinebot'

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')