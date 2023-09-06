import os

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    LINE_PAY_ID = '2000604811'
    LINE_PAY_SECRET = '85c2256b73ef51f3adfcd8bc189172f5'

    STORE_IMAGE_URL = 'https://i.imgur.com/0KinQXT.jpg'

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://integratelinebot:ryZcECKSVuEl80HwA9VLUhmi55KFenyT@dpg-cjrr8vojbais73fe0g5g-a.singapore-postgres.render.com/integratelinebot'

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

