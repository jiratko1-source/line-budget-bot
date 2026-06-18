from flask import Flask, request, jsonify
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, QuickReply, QuickReplyButton, MessageAction
import os

app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = "nQYK7aDubVwiNcJVPgLHMO82eT80Pw5j1eDkY4zwHuNj3sd9fEVXixOlIpmOwqQsJyHSesqHEzOD9zjFU1jP6ZFScv41cQaISy+BCk/wKfeTAZwCxUh+nrKXZ5EhLUCjLMzcNu23elVkHtOJxNOcdgdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "924d488f50f2ef8f86815bbbd0bf8a36"

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    if "บันทึก" in user_message or "บันทึกรายจ่าย" in user_message:
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="🍜 อาหาร", text="🍜 อาหาร")),
            QuickReplyButton(action=MessageAction(label="🚗 เดินทาง", text="🚗 เดินทาง")),
            QuickReplyButton(action=MessageAction(label="🛒 ช้อปปิ้ง", text="🛒 ช้อปปิ้ง")),
            QuickReplyButton(action=MessageAction(label="🎮 บันเทิง", text="🎮 บันเทิง")),
        ])
        line_bot_api.reply_message(
            event.reply_token,
            message=TextMessage(text="เลือกหมวดหมู่ได้เลยครับ", quick_reply=quick_reply)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=f"คุณพูดว่า: {user_message}\n\nพิมพ์ 'บันทึก' เพื่อเริ่มบันทึกรายจ่าย")
        )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
