# bot.py
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is not set")

# داده‌ها از جدول شما
CAR_DATA = {
    "آریسان": {"ارتقا یافته": ["1403", "1404"]},
    "اطلس": {"G دنده ای": ["1403", "1404"], "GL دنده ای": ["1404"], "اتوماتیک E پلاس": ["1404"]},
    "پراید": {"151 GX": ["1404"], "151 SE": ["1403", "1404"]},
    "پژو": {
        "207 TU3": ["1403", "1404"],
        "207 اتوماتیک TU5P": ["1403", "1404"],
        "207 پانوراما اتوماتیک TU5P": ["1403", "1404"],
        "207 پانوراما دنده ای TU5": ["1403", "1404"],
        "207 دنده ای TU5": ["1403", "1404"],
        "207 دنده ای TU5P": ["1404"],
        "پارس ELX-XU7P": ["1403"],
        "پارس XU7P": ["1403"]
    },
    "تارا": {"اتوماتیک V2": ["1403"], "اتوماتیک V4 LX": ["1403", "1404"], "دنده ای V1 پلاس 6 سرعته": ["1403", "1404"]},
    "دنا": {
        "پلاس EF7 5 دنده ساده": ["1403", "1404"],
        "پلاس EF7 6 دنده توربو": ["1403"],
        "پلاس EF7 اتوماتیک توربو آپشنال": ["1403", "1404"],
        "پلاس EF7 اتوماتیک توربو ساده": ["1403"],
        "پلاس EF7P 6 دنده": ["1403", "1404"]
    },
    # بقیه خودروها را می‌توانید به همین شکل اضافه کنید
}

user_data = {}

# شروع ربات
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(car, callback_data=f"car_{car}")] for car in CAR_DATA]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام 👋 خوش اومدی! ماشین خود را انتخاب کنید:", reply_markup=reply_markup)

# هندلر دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data.startswith("car_"):
        car = query.data.split("_")[1]
        user_data[user_id] = {"car": car}
        models = CAR_DATA[car].keys()
        keyboard = [[InlineKeyboardButton(model, callback_data=f"model_{model}")] for model in models]
        await query.edit_message_text(f"مدل/تیپ {car} را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("model_"):
        model = query.data.split("_")[1]
        user_data[user_id]["model"] = model
        car = user_data[user_id]["car"]
        years = CAR_DATA[car][model]
        keyboard = [[InlineKeyboardButton(year, callback_data=f"year_{year}")] for year in years]
        await query.edit_message_text(f"سال تولید {car} {model} را انتخاب کنید:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("year_"):
        year = query.data.split("_")[1]
        user_data[user_id]["year"] = year
        info = user_data[user_id]
        await query.edit_message_text(
            f"✅ آگهی شما با موفقیت ثبت شد!\n\n"
            f"🚗 خودرو: {info['car']}\n"
            f"📦 مدل/تیپ: {info['model']}\n"
            f"📅 سال: {info['year']}"
        )
        user_data.pop(user_id, None)  # پاک کردن داده کاربر بعد از ثبت آگهی

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("ربات فعال شد ✅")
    app.run_polling()
