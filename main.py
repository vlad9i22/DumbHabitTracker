import logging
import config

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def add_habbit(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Habbit {" ".join(context.args)} was added")


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
    
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    start_handler = CommandHandler('start', start)
    add_habbit_handler = CommandHandler('add', add_habbit)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(add_habbit_handler)

    
    application.run_polling()
