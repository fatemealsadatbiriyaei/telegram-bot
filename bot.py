import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توکن از متغیر محیطی خوانده می‌شود (در Render اضافه‌اش می‌کنیم)
BOT_TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 خوش اومدی به ربات صفر فروش‌ها!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("ربات فعال شد ✅")
app.run_polling()
