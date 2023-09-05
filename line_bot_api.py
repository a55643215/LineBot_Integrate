
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

line_bot_api = LineBotApi('Ihk8eFoBqjwSWAqUGPFEqpNxBY5TjdJUiLJO3hINiG3vmClr5Q2sAe6+HT9POGeU/ITi4GOmRRb4fGWMZ8buxEEOlyvB3FyOWvERxfqKKd42oPA35WXABMx6n8oK/YrVtVIuU7aMtiSOwBteLPg1OQdB04t89/1O/w1cDnyilFU=')
# Channel access token
handler = WebhookHandler('fe615012eaea781c5e2738fc6d38134e') 
#Channel secret