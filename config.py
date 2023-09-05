import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://medicine_offer:Vt6RqxnBcXH45JzKvz8wUqVJZi6Vq4Ny@dpg-cjg2jec1ja0c739odo7g-a.singapore-postgres.render.com/medicine_offer'

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')