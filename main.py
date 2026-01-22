import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a welcome message when the command /start is issued."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hi! I'm a simple echo bot. Send me a message and I'll repeat it."
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echoes the user message."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=update.message.text
    )

def main():
    """Starts the bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN environment variable not set.")
        print("Please create a .env file based on .env.example and add your token.")
        return

    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()