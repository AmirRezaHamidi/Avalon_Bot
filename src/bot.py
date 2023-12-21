from typing import Final
import telebot
from telegram import Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)
import os


TOKEN = '6468920953:AAHXzkA9iOrVwThJ6pk6kZ06AE7DSOnJVsI'
BOT_USERNAME = "@Our_Avalon_Bot"

bot = telebot.TeleBot(TOKEN)
print('hello')
bot.infinity_polling()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("OK Let's play.\nStart by choosing"
                                    "a name for yourself.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here is the help function for ")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ok lets play the game")


def handle_response(text: str) -> str:

    return text


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat.id == 224775397:

        text = 'You are the admin of the game.\n'\
               'Start the game by pressing "Start the Game" button below.'
        response: str = handle_response(text)

        print("Bot: ", response)
        await update.message.reply_text(response)

    else:

        text = "Wait for the admin to start the game."
        response: str = handle_response(text)

        print("Bot: ", response)
        await update.message.reply_text(response)


if __name__ == "__main__":

    print('starting the bot ... ')

    app = Application.builder().token(TOKEN).build()

    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("Custom", custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print('start polling...')
    app.run_polling(poll_interval=1e-2)
