from line_bot_api import *
from urllib.parse import parse_qsl
import datetime


from extensions import db
from models.user import User
from models.reservation import Reservation #資料寫入資料庫中
#預約相關功能都會寫在這邊
#增加多個服務項目
services = {
    1:{
        'category':'醫美',
        'img_url':'https://i.imgur.com/y3S5t51.jpg',
        'title':'塑身纖體',
        'duration':'諮詢30min',
        'description' : '冷凍溶脂/EMBODY核心美麗/So纖筆/Liposonix/CM Slim偵腹肌',
        'price':200,
        'post_url':'https://google.com'
    },
    2: {
        'category':'醫美',
        'img_url':'https://i.imgur.com/dm4SFcH.jpg',
        'title':'雷射光療',
        'duration':'諮詢30min',
        'description' : '全像超皮秒雷射/皮冷極光雷射/淨白煥膚',
        'price':200,
        'post_url':'https://google.com'
    },
    3: {
        'category':'醫美',
        'img_url':'https://i.imgur.com/Fvk5zdu.jpg',
        'title':'抗老拉提',
        'duration':'諮詢30min',
        'description' : '電波拉提/Ulthra音波拉提/線雕',
        'price':200,
        'post_url':'https://google.com'
    },
    4: {
        'category':'醫美',
        'img_url':'https://i.imgur.com/3zAkzog.jpg',
        'title':'微整形',
        'duration':'諮詢30min',
        'description' : '凹陷填補/複合式微整/保濕計畫/除皺/瘦小臉/立體塑型',
        'price':200,
        'post_url':'https://google.com'
    },

    #整型外科
    5: {
        'category':'整型外科',
        'img_url':'https://i.imgur.com/Go1Hoq2.jpg',
        'title':'Motiva魔滴隆乳',
        'duration':'諮詢30min',
        'description' : '渾然美胸VIVI/自然美胸/告別小胸/柔軟仿真觸感',
        'price':200,
        'post_url':'https://google.com'
    },
    6: {
        'category':'整型外科',
        'img_url':'https://i.imgur.com/XIF4iAA.png',
        'title':'抽脂補脂',
        'duration':'諮詢30min',
        'description' : '自體脂肪移植隆乳豐胸/自己脂肪豐頰補臉',
        'price':200,
        'post_url':'https://google.com'
    },
    7: {
        'category':'整型外科',
        'img_url':'https://i.imgur.com/LAb26E4.jpg',
        'title':'胸部',
        'duration':'諮詢30min',
        'description' : 'Mentor Xtra 女王波/隱痕水滴型隆乳/果凍矽膠隆乳',
        'price':200,
        'post_url':'https://google.com'
    },
    8: {
        'category':'整型外科',
        'img_url':'https://i.imgur.com/KYYWgHl.jpg',
        'title':'眼睛',
        'duration':'諮詢30min',
        'description' : '隱痕眼袋明眸術/除眼袋/割眼袋/雙凍超毫米隱痕提眼臉/隱痕明眸上額拉提術/雙眼皮/開眼皮，縫雙眼皮',
        'price':200,
        'post_url':'https://google.com'
    },
    9: {
        'category':'整型外科',
        'img_url':'https://i.imgur.com/P8VXLwM.jpg',
        'title':'抽脂雕塑',
        'duration':'諮詢30min',
        'description' : 'VaserLipo威塑體雕/大腿環狀抽脂',
        'price':200,
        'post_url':'https://google.com'
    },
    10: {
        'category':'整型外科',
        'img_url':'https://i.imgur.com/JnJiIuR.png',
        'title':'臉部輪廓',
        'duration':'諮詢30min',
        'description' : '隆鼻+雙眼皮/臉部自體補脂/黃金比例美顏術',
        'price':200,
        'post_url':'https://google.com'
    },
    11: {
        'category':'整型外科',
        'img_url':'https://i.imgur.com/jJXxN52.jpg',
        'title':'鼻子',
        'duration':'諮詢30min',
        'description' : '三段式隆鼻/眼鼻精雕術/隆鼻/自然系混血感客製化隆鼻手術',
        'price':200,
        'post_url':'https://google.com'
    }

    }

def service_category_event(event):
     image_carousel_template_message = TemplateSendMessage(
          alt_text = '請選擇想服務類別',
          template = ImageCarouselTemplate(
            columns = [
                 ImageCarouselColumn(
                    image_url = 'https://i.imgur.com/YwIvYjP.jpg',
                    action = PostbackAction(
                        label = '醫美',
                        display_text = '想了解醫美',
                        data = 'action=service&category=醫美'
                    )
                 ),
                 ImageCarouselColumn(
                    image_url = 'https://i.imgur.com/1eud8vr.jpg',
                    action = PostbackAction(
                        label = '整形手術',
                        display_text = '想了解整形',
                        data = 'action=service&category=整型外科'
                    )
                 )
            ]
          )
     )
     line_bot_api.reply_message(
          event.reply_token,
          [image_carousel_template_message]
     )



def service_event(event):
    #底下三個要等上面的service建立後才寫，主要是要跑service的服務
    #data = dict(parse_qsl(event.postback.data))
    #bubbles=[]
    #for service_id in services:

    data = dict(parse_qsl(event.postback.data))
    bubbles = []

    for service_id in services:
            if services[service_id]['category'] == data['category']:
                service = services[service_id]
                bubble = {
                "type": "bubble",
                "hero": {
                    "type": "image",
                    "size": "full",
                    "aspectRatio": "20:13",
                    "aspectMode": "cover",
                    "url": service['img_url']
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "text",
                        "text": service['title'],
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl"
                    },
                    {
                        "type": "text",
                        "text": service['duration'],
                        "size": "md",
                        "weight": "bold"
                    },
                    {
                        "type": "text",
                        "text": service['description'],
                        "margin": "lg",
                        "wrap": True
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "contents": [
                        {
                            "type": "text",
                            "text": f"NT$ {service['price']}",
                            "wrap": True,
                            "weight": "bold",
                            "size": "xl",
                            "flex": 0
                        }
                        ],
                        "margin": "xl"
                    }
                    ]
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "button",
                        "style": "primary",
                        "action": {
                        "type": "postback",
                        "label": "預約",
                        "data": f"action=select_date&service_id={service_id}",
                        "displayText": f"我想預約【{service['title']} {service['duration']}】"
                        },
                        "color": "#b28530"
                    },
                    {
                        "type": "button",
                        "action": {
                        "type": "uri",
                        "label": "了解詳情",
                        "uri": service['post_url']
                        }
                    }
                    ]
                }
                }

                bubbles.append(bubble)

    flex_message = FlexSendMessage(
         alt_text = '請選擇預約項目',
         contents={
              "type":"carousel",
              "contents":bubbles
         }
    )

    line_bot_api.reply_message(
         event.reply_token,
         [flex_message]
    )


def service_select_date_event(event):
    data = dict(parse_qsl(event.postback.data))

    weekdat_string={
          0:'一',
          1:'二',
          2:'三',
          3:'四',
          4:'五',
          5:'六',
          6:'日',
     }#休息日就拿掉

    business_day = [1,2,3,4,5,6]#休息日就拿掉

    quick_reply_buttons = []

    today = datetime.datetime.today().date()#取得當天日期
    #weekday()取得星期幾?0是星期一
    for x in range(1,11):
        day = today + datetime.timedelta(days=x)#透過datetime.timedelta()可以取得隔天的日期
        

        if day != 0 and (day.weekday() in business_day):
            quick_reply_button = QuickReplyButton(
                action = PostbackAction(label=f'{day}({weekdat_string[day.weekday()]})',
                                        text=f'我要預約{day}({weekdat_string[day.weekday()]})這天',
                                        data= f'action=select_time&service_id={data["service_id"]}&date={day}'))
            quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text="請問要預約哪一天？",
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    line_bot_api.reply_message(
         event.reply_token,
         [text_message]
    )




#選擇時間功能
def service_select_time_event(event):
    data = dict(parse_qsl(event.postback.data))

    available_time=['11:00', '14:00' ,'17:00', '20:00'] #可以自己更改時間段

    quick_reply_buttons = []

    for time in available_time:
         quick_reply_button = QuickReplyButton(action= PostbackAction(label=time,
                                                                       text=f'{time}這個時段',
                                                                       data=f'action=confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'))
         quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪個時段？',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    line_bot_api.reply_message(
         event.reply_token,
         [text_message]
    )

#
def service_confirm_event(event):
     
    data = dict(parse_qsl(event.postback.data))
    booking_service = services[int(data['service_id'])] #取得要預約的服務項目資料，會出現1234對應到上面的service

    confirm_template_message = TemplateSendMessage(
        alt_text='請確認預約項目',
        template = ConfirmTemplate(
            text=f'您即將預約\n\n{booking_service["title"]} {booking_service["duration"]}\n預約時段: {data["date"]} {data["time"]}\n\n確認沒問題請按【確定】',
            actions=[
                 PostbackAction(
                        label='確定',
                        display_text='確定沒問題！',
                        data=f'action=confirmed&service_id={data["service_id"]}&date={data["date"]}&time={data["time"]}'
                 ),
                 MessageAction(
                        label='重新預約',
                        text='@預約服務'
                 )
            ]
        )
    )
    line_bot_api.reply_message(
         event.reply_token,
         [confirm_template_message]
    )


def is_booked(event, user):
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_canceled.is_(False),#代表沒有被取消
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
                                           #需要大於當下的時間.first()是會回傳第一筆資料
    if reservation:#text顯示預約項目名稱和服務時段
        buttons_template_message = TemplateSendMessage(
            alt_text='您已經有預約了，是否需要取消?',
            template=ButtonsTemplate(
                title='您已經有預約了',
                text=f'{reservation.booking_service}\n預約時段: {reservation.booking_datetime}',
                actions=[
                    PostbackAction(
                        label='我想取消預約',
                        display_text='我想取消預約',
                        data='action=cancel'
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            [buttons_template_message])

        return True
    else:
        return False



# def service_confirmed_event(event):
#      data = dict(parse_qsl(event.postback.data))

#      booking_service = services[int(data['service_id'])]
#      booking_datetime = datetime.datetime.strptime(f'{data["date"]}{data["time"]}', '%Y-%m-%d %H:%M')

#      user = User.query.filter(User.line_id == event.source.user_id).first()
#      if is_booked(event,user):
#           return
#      reservation = Reservation(
#           user_id= user.id,
#           booking_service_category=f'{booking_service["category"]}',
#           booking_service = f'{booking_service["title"]}{booking_service["duration"]}',
#           booking_datetime = booking_datetime 
#      )

#      db.session.add(reservation)
#      db.session.commit()

#      line_bot_api.reply_message(
#           event.reply_token,
#           [TextSendMessage(text='沒問題！感謝您的預約，我已經幫你預約成功了喔，到時候見！')]
#      )
def service_confirmed_event(event):
    data = dict(parse_qsl(event.postback.data))

    booking_service = services[int(data['service_id'])]
    booking_datetime = datetime.datetime.strptime(f'{data["date"]} {data["time"]}', '%Y-%m-%d %H:%M')

    user = User.query.filter(User.line_id == event.source.user_id).first()
    if is_booked(event, user):
        return

    reservation = Reservation(
        user_id=user.id,
        booking_service_category=f'{booking_service["category"]}',
        booking_service=f'{booking_service["title"]} {booking_service["duration"]}',
        booking_datetime=booking_datetime)

    db.session.add(reservation)
    db.session.commit()

    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text='沒問題! 感謝您的預約，我已經幫你預約成功了喔，到時候見!')])
    
#取消預約 資料庫欄位不會drop,是 is_cacnceled欄位會變成true

def service_cancel_event(event):

    user = User.query.filter(User.line_id == event.source.user_id).first()
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_canceled.is_(False),
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
    if reservation:
        reservation.is_canceled = True

        db.session.add(reservation)
        db.session.commit()

        # line_bot_api.reply_message(
        #     event.reply_token,
        #     [TextSendMessage(text='您的預約已經幫你取消了')])
        buttons_cancel_message = TemplateSendMessage(
            alt_text='您的預約已幫你取消了！',
            template=ConfirmTemplate(
                text='您的預約已幫你取消了！',
                actions=[                     
                    MessageAction(
                        label='重新預約',
                        text='@預約服務'
                    ),
                    MessageAction(
                        label ='取消',
                        text='取消'
                    )
                ]
            )
        )
        line_bot_api.reply_message(
            event.reply_token,
            [buttons_cancel_message])
    else:
        buttons_cancel_message = TemplateSendMessage(
            alt_text='您的預約已幫你取消了！',
            template=ConfirmTemplate(
                text='您目前沒有預約喔！',
                actions=[                     
                    MessageAction(
                        label='我要預約',
                        text='@預約服務'
                    ),
                    MessageAction(
                        label ='取消',
                        text='取消'
                    )
                ]
            )
        )


        line_bot_api.reply_message(
            event.reply_token,
            [buttons_cancel_message])