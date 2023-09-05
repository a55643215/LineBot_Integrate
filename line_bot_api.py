
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent, 
    StickerSendMessage, ImageSendMessage, LocationSendMessage,FlexSendMessage,
    TemplateSendMessage,ImageCarouselTemplate,ImageCarouselColumn,PostbackAction,
    PostbackEvent,QuickReply,QuickReplyButton,ConfirmTemplate,MessageAction,ButtonsTemplate
)

line_bot_api = LineBotApi('FGv8iZ1Ma5XCwmCqSFL9sKKd+VbCYJYhgFy5sthR8LaidOMMqeo0a1C/MOrDu2SzXXEnvjN6Nhfej6cXumQ3I8yp9w7QP6bYyqVQdOb54G5vCJdied6vfVNLBleiSf2UuY8zzAAMPZwa3++hf1862QdB04t89/1O/w1cDnyilFU=')
# Channel access token
handler = WebhookHandler('f1fa75e1b63d5245714ecf28668307f8') 
#Channel secret