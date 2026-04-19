import requests
import time

TOKEN = "783424163:t9SUXQA5ytFbrUKDa4SiURhjc2Lob8NvF18"
URL = f"https://tapi.bale.ai/bot{TOKEN}/"

ADMIN_ID = 783424163 # آیدی عددی خودت

users = {}
orders = []


# ===== ارسال پیام =====
def send_message(chat_id, text, keyboard=None):
    data = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = keyboard

    requests.post(URL + "sendMessage", json=data)


# ===== منوی اصلی =====
def main_menu(chat_id):
    keyboard = {
        "inline_keyboard": [
            [{"text": "🛍 فروشگاه", "callback_data": "shop"}],
            [{"text": "📦 سفارشات من", "callback_data": "my_orders"}],
            [{"text": "💳 پرداخت", "callback_data": "pay"}],
            [{"text": "📞 پشتیبانی", "callback_data": "support"}],
        ]
    }

    send_message(chat_id, "✨ به SellBot خوش اومدی ✨", keyboard)


# ===== دریافت آپدیت =====
def get_updates(offset):
    res = requests.get(URL + "getUpdates", params={"offset": offset})
    return res.json().get("result", [])


# ===== مدیریت پیام =====
def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        main_menu(chat_id)

    elif users.get(chat_id) == "waiting_order":
        orders.append({"user": chat_id, "text": text})
        users[chat_id] = None

        send_message(chat_id, "✅ سفارشت ثبت شد")

        # ارسال برای ادمین
        send_message(ADMIN_ID, f"📥 سفارش جدید:\n{text}")


# ===== مدیریت دکمه‌ها =====
def handle_callback(callback):
    chat_id = callback["message"]["chat"]["id"]
    data = callback["data"]

    # ===== فروشگاه =====
    if data == "shop":
        keyboard = {
            "inline_keyboard": [
                [{"text": "📱 اکانت ویژه - 50 تومن", "callback_data": "buy1"}],
                [{"text": "💎 اشتراک VIP - 100 تومن", "callback_data": "buy2"}],
                [{"text": "🔙 بازگشت", "callback_data": "back"}]
            ]
        }
        send_message(chat_id, "🛍 محصولات:", keyboard)

    # ===== خرید =====
    elif data == "buy1" or data == "buy2":
        users[chat_id] = "waiting_order"
        send_message(chat_id, "✍️ مشخصات سفارش رو بنویس:")

    # ===== سفارشات من =====
    elif data == "my_orders":
        user_orders = [o["text"] for o in orders if o["user"] == chat_id]

        if not user_orders:
            send_message(chat_id, "❌ سفارشی نداری")
        else:
            text = "\n\n".join(user_orders)
            send_message(chat_id, f"📦 سفارشات تو:\n\n{text}")

    # ===== پرداخت (نمونه) =====
    elif data == "pay":
        send_message(chat_id, "💳 برای پرداخت به پشتیبانی پیام بده")

    # ===== پشتیبانی (وصل به آیدی خودت) =====
    elif data == "support":
        keyboard = {
            "inline_keyboard": [
                [
                    {
                        "text": "📞 ارتباط با پشتیبانی",
                        "url": "https://ble.ir/Ali_Alfred"
                    }
                ]
            ]
        }

        send_message(chat_id,
"""📞 پشتیبانی SellBot

⏰ پاسخگویی: 24 ساعته  
⚡ سریع‌ترین پاسخ  

روی دکمه زیر بزن 👇
""", keyboard)

    # ===== بازگشت =====
    elif data == "back":
        main_menu(chat_id)


# ===== اجرای ربات =====
offset = 0

while True:
    updates = get_updates(offset)

    for update in updates:
        offset = update["update_id"] + 1

        if "message" in update:
            handle_message(update["message"])

        elif "callback_query" in update:
            handle_callback(update["callback_query"])

    time.sleep(1)

