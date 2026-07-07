from telegram import Update
from telegram.ext import ContextTypes

from services import verify_telegram


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if len(context.args) == 0:
        await update.message.reply_text(
            "👋 Welcome to REMINDR!\n\nPlease connect your account from the REMINDR website."
        )
        return

    token = context.args[0]

    response = verify_telegram(
        token=token,
        chat_id=str(update.effective_chat.id),
    )

    if response.status_code == 200:
        await update.message.reply_text(
            "✅ Telegram connected successfully!\n\nYou'll now receive REMINDR notifications here."
        )
    else:
        await update.message.reply_text(
            "❌ Invalid or expired connection link.\nPlease connect again from REMINDR."
        )