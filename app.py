from flask import Flask,request,abort
from linebot.models import *
from events.service import *
from line_bot_api import *
from events.basic import *
from events.admin import *
from extensions import db, migrate
from models.user import User    
from database import db_session, init_db
from models.product import Products
from models.cart import Cart
import os

app = Flask(__name__)
#admin: !QAZ2wsx資料庫的帳號和密碼
#讓程式自己去判斷如果是測試端就會使用APP_SETTINGS
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevConfig'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://integratelinebot:ryZcECKSVuEl80HwA9VLUhmi55KFenyT@dpg-cjrr8vojbais73fe0g5g-a.singapore-postgres.render.com/integratelinebot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)


#callback

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()
    user = User.query.filter(User.line_id == event.source.user_id).first()#取得user的第一筆資料
    #如果沒有user資料時，才會透過api去取得
    if not user:

        profile = line_bot_api.get_profile(event.source.user_id)#Line API 中說明get_profile可以取得的資料
        print(profile.display_name)
        print(profile.user_id)#相同的好以會因為不同的profile 而有不同的user_id

        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()

    print(user.id)
    print(user.line_id)
    print(user.display_name)

    cart = Cart(user_id=event.source.user_id)

    if message_text == '@關於我們':
        about_us_event(event)
    elif message_text =='@預約服務':
        service_category_event(event)

    elif message_text.startswith('*'):
        if event.source.user_id not in ['U135d0047f682b28ef4001bcb47d0d21f']:
            return
        if message_text in ['*data', '*d']:
            list_reservation_event(event)

    elif message_text == '@醫師群':
        pass

    elif message_text in ['@優惠商品','再去逛逛']:
        message=Products.list_all(event)

    elif "請輸入購買數量" in message_text:
        message = cart.ordering(event)
    
    elif message_text in ['@購物車','my cart', 'cart', "查看購物車"]:#當出現'my cart', 'cart', "that's it"時

        if cart.bucket():#當購物車裡面有東西時
            message = cart.display()#就會使用 display()顯示購物車內容
        else:
            message = TextSendMessage(text='您的購物並沒有任何商品！')
    elif message_text == '清空購物車':

        cart.reset()

        message = TextSendMessage(text='您的購物車已清空.')
    

    if message:
        line_bot_api.reply_message(
        event.reply_token,
        message) 

        


#接收postback的訊息
#parse_qsl解析data中的資料
@handler.add(PostbackEvent)
def handle_postback(event):
    #把傳進來的event儲存在postback.data中再利用parse_qsl解析data中的資料然漚轉換成dict
    data = dict(parse_qsl(event.postback.data))
    #建立好def service_event(event) function後要來這裡加上判斷式
    #直接呼叫service_event(event)

    if data.get('action') == 'service':
        service_event(event)
    elif data.get('action') == 'select_date':
        service_select_date_event(event)
    elif data.get('action') == 'select_time':
        service_select_time_event(event)
    elif data.get('action') == 'confirm':
        service_confirm_event(event)
    elif data.get('action') == 'confirmed':
        service_confirmed_event(event)
    elif data.get('action') == 'cancel':
        service_cancel_event(event)

    #用get()來取得data中的資料，好處是如果備有data時會顯示None，而不會出線錯物
    

################## 解除封鎖 ####################
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg="""Hello! 您好，歡迎您成為 Aesthetc_Medicine 的好友！

我是 Aesthetc_Medicine 小幫手！

-歡迎預約門診

-諮詢費每30分鐘200元喔！
    
-醫美/整型外科/隆乳/隆鼻/美麗計畫"""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg)
    )

################## 顯示封鎖 ####################
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)



#初始化產品資訊
@app.before_first_request
def init_products():
    # init db
    result = init_db()#先判斷資料庫有沒有建立，如果還沒建立就會進行下面的動作初始化產品
    if result:
        init_data = [Products(name='白松露修護冰霜 50ml',
                              product_image_url='https://shoplineimg.com/5eccc85266c9d60040e84861/61860ca65f4d580035c481f1/800x.webp?source_format=png',
                              price=150,
                              description='富含多種植物精華、無動物性成分、修護肌膚、快速吸收，無添加人工香精、酒精、色素'),
                     Products(name='Tea',
                              product_image_url='https://i.imgur.com/PRTxyhq.jpg',
                              price=120,
                              description='adipiscing elit. Aenean commodo ligula eget dolor'),
                     Products(name='Cake',
                              price=180,
                              product_image_url='https://i.imgur.com/PRm22i8.jpg',
                              description='Aenean massa. Cum sociis natoque penatibus')]
        db_session.bulk_save_objects(init_data)#透過這個方法一次儲存list中的產品
        db_session.commit()#最後commit()才會存進資料庫
        #記得要from models.product import Products在app.py
        



if __name__ == '__main__':
    init_products()
    app.run()