from extensions import db
import datetime
from sqlalchemy import Column,DateTime,String,func
from sqlalchemy.orm import relationship
from database import Base

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True) #設定他為主鍵

    line_id = db.Column(db.String(50), unique= True) #unique = True 代表是不可以重複的
    display_name = db.Column(db.String(255)) #用戶的line名稱
    picture_url = db.Column(db.String(255)) #用戶大頭貼的url

    created_on = db.Column(db.DateTime, default= datetime.datetime.now())

    def __init__(self, line_id,display_name,picture_url):
        self.line_id = line_id
        self.display_name = display_name
        self.picture_url = picture_url

class Users(Base):
    __tablename__ ='users'

    id = Column(String,primary_key = True) #line用戶id
    nick_name = Column(String) #line用戶name
    image_url = Column(String(length=256)) #line用戶頭貼
    created_time = Column(DateTime,default=func.now()) #line用戶被建立

    orders = relationship('Orders', backref='user') #加上這行建立訂單關聯性

    # user.orders 未來只要用這個指令就可以知道user所有的訂單
    # [<Order1> , <Order 2>]

    # order.user 透過訂單就可以知道是哪個user的
    # <User 1>