import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = f"https://telegram-bot-1-itzu.onrender.com/{BOT_TOKEN}"  # URL سرویس Render شما

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 خوش اومدی به ربات صفر فروش‌ها!")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Webhook
app.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 5000)),  # Render خودش PORT اختصاص میده
    url_path=BOT_TOKEN,
    webhook_url=WEBHOOK_URL
)
