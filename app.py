#openai_api_key = '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'

import os
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['vX/WSxOjIY7lTRKr59SH+UyxU4rncf7E6aKvg6IAg+kq7tdHwKo+JEgH6OZrULJrgDiVRkvjDJsRJyt8Wk+FMyu4QfjaEITDPn+nspP+ArYPxwOe6V1AnAXIPOJWdQKSKEvx7J8J0N3XW2i0fGYv8gdB04t89/1O/w1cDnyilFU='])
handler = WebhookHandler(os.environ['08ad1d8a8864f3aaaa3d003440ed609c'])

openai.api_key = os.environ['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']

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return 'Invalid signature'
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    response = openai.Completion.create(
        engine='davinci',
        prompt=text,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    answer = response.choices[0].text.strip()
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=answer)
    )

if __name__ == "__main__":
    app.run()