import logging
import config

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import KeyboardButton, ReplyKeyboardMarkup


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


habits = ["chill", "guitar"]


async def button1_function(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("You pressed Button 1!")
    await show_buttons(update)


async def button2_function(update, context):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("You pressed Button 2!")
    await show_buttons(update)


# Place to select completed habbits
async def show_buttons(update):
    keyboard = [
        [InlineKeyboardButton("habbit 1", callback_data='button1')],
        [InlineKeyboardButton("habbit 2", callback_data='button2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        await update.callback_query.message.reply_text("Habits for today", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Habits for today", reply_markup=reply_markup)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="I'm a bot, please talk to me!")
    await show_buttons(update)


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
    application.add_handler(CallbackQueryHandler(button1_function, pattern='button1'))
    application.add_handler(CallbackQueryHandler(button2_function, pattern='button2'))

    
    application.run_polling()
