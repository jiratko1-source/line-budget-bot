from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature")
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400
    
    return "OK", 200

@handler.add
def handle_message(event):
    if event.type != "message" or event.message.type != "text":
        return
    
    quick_reply = QuickReply(items=[
        QuickReplyButton(action=MessageAction(label="💸 บันทึกรายจ่าย", text="บันทึกรายจ่าย")),
        QuickReplyButton(action=MessageAction(label="💰 บันทึกรายรับ", text="บันทึกรายรับ")),
        QuickReplyButton(action=MessageAction(label="📊 ดูสรุป", text="ดูสรุป")),
    ])
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="สวัสดีครับ! มีอะไรที่ช่วยได้ไหมครับ", quick_reply=quick_reply)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
