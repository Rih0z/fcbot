from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

import requests, bs4
import sys
import re
#import importlib
#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

app = Flask(__name__)


url = 'https://www.amazon.co.jp/s/ref=nb_sb_noss_1?url=search-alias%3Dinstant-video&field-keywords='

keyword = ""

cn = "見つかりませんでした"
tx = ""
mes = ""
#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    keyword = event.message.text
    res = requests.get(url + keyword)
    try:
        soup = bs4.BeautifulSoup(res.text, "html.parser")
    except:
        soup = bs4.BeautifulSoup(res.text, "html5lib")

    cnt =  soup.select_one("#result_0 > div > div > div > div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small > div > a > h2")
    if(type(cnt) is bs4.element.Tag):
        cn = cnt.getText()
    else: 
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="見つけられなかったよ"))
        return
    tx =  soup.select_one("#result_0 > div > div > div > div.a-fixed-left-grid-col.a-col-right > div:nth-child(2) > div.a-column.a-span7").getText()

    if (tx.find("プライム会員特典") != -1):
        mes= cn + "は"+"Amazon Prime特典だよ"
    else:
        
        mes = cn  + "は" +tx + "だよ．"
        if(tx == ""):
            mes = cn + "はAmazonでは見られないよ．"
        if(tx.find("￥ 0エピソード レンタル") != -1):
            mes = mes + "2話以降は有料かも"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = mes))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
