from typing import Final

from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          MessageHandler, filters)

from src.Data import DATA_DIR

TOKEN: Final = '6468920953:AAHXzkA9iOrVwThJ6pk6kZ06AE7DSOnJVsI'
BOT_USERNAME: Final = "@Our_Avalon_Bot"


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_game = "start a new game"
    not_a_new_game = "starting from scratch"
    buttons = [[KeyboardButton(new_game)], [KeyboardButton(not_a_new_game)]]
    await update.message.reply_text("OK Let's play.\nStart by choosing a name for yourself.")
    reply_markup = ReplyKeyboardMarkup(buttons)


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


# async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print(f"Update {update} cause error{context.error}")

    # Errors
    # app.add_error_handler(error)
    # print(f"User {update.message.chat.id} in {message_type}: {text}")
    #
    # if BOT_USERNAME in text:
    #
    #     new_text: str = text.replace(BOT_USERNAME, '').strip()
    #     response: str = handle_response(new_text)
    #
    # else:
    #
    #     return

    # message_type: str = update.message.chat.type
    #
    # text: str = update.message.text
