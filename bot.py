# bot.py
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# گرفتن توکن از متغیر محیطی
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

# داده‌های خودروها
CARS = {
    "207": {"name": "پژو 207", "models": {"manual": "207 دستی", "auto": "207 اتوماتیک", "panorama": "207 پانوراما"}},
    "samand": {"name": "سمند", "models": {"normal": "سمند معمولی", "soren": "سمند سورن", "lx": "سمند LX"}},
    "pride": {"name": "پراید", "models": {"111": "پراید 111", "131": "پراید 131", "132": "پراید 132"}},
    "dana": {"name": "دنا", "models": {"normal": "دنا معمولی", "plus": "دنا پلاس", "turbo": "دنا پلاس توربو"}},
    "tiba": {"name": "تیبا", "models": {"sedan": "تیبا صندوق‌دار", "hatch": "تیبا 2"}}
}

# داده‌های محل تحویل
DELIVERIES = {"college": "کالج", "golha": "گلها", "tohid": "توحید", "valiasr": "ولیعصر"}

# ذخیره‌سازی موقت داده‌های کاربر
user_data = {}

# فرمان /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(CARS[car]["name"], callback_data=f"car_{car}")] for car in CARS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام 👋 خوش اومدی! ماشین خود را انتخاب کنید:", reply_markup=reply_markup)

# مدیریت کلیک‌های کاربر
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data.startswith("car_"):
        car_key = query.data.split("_")[1]
        user_data[user_id] = {"car_key": car_key}
        car = CARS[car_key]
        keyboard = [[InlineKeyboardButton(name, callback_data=f"model_{key}")] for key, name in car["models"].items()]
        await query.edit_message_text(f"مدل {car['name']} را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("model_"):
        model_key = query.data.split("_")[1]
        user_data[user_id]["model_key"] = model_key
        keyboard = [[InlineKeyboardButton(name, callback_data=f"delivery_{key}")] for key, name in DELIVERIES.items()]
        await query.edit_message_text("نوع تحویل را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("delivery_"):
        delivery_key = query.data.split("_")[1]
        user_data[user_id]["delivery_key"] = delivery_key
        info = user_data[user_id]
        car = CARS[info["car_key"]]
        model = car["models"][info["model_key"]]
        delivery = DELIVERIES[delivery_key]
        await query.edit_message_text(
            f"✅ آگهی شما ثبت شد!\n\n🚗 ماشین: {car['name']}\n📦 مدل: {model}\n📍 تحویل: {delivery}"
        )

# اجرای وبهوک (برای Render)
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    PORT = int(os.environ.get("PORT", 8443))
    RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
    if not RENDER_URL:
        raise RuntimeError("RENDER_EXTERNAL_URL environment variable is not set")

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=f"webhook/{BOT_TOKEN}",
        webhook_url=f"https://{RENDER_URL}/webhook/{BOT_TOKEN}"
    )
