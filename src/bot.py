import os
from types import SimpleNamespace

from collections import defaultdict
import telebot
from loguru import logger
from telebot import types
from emoji import emojize, demojize
from utils.io import write_json

TOKEN = "6468920953:AAHXzkA9iOrVwThJ6pk6kZ06AE7DSOnJVsI"

class Bot():

    def __init__(self):
        
        self.game_exist = False
        self.players = defaultdict(list)
        self.bot = telebot.TeleBot(TOKEN)

        logger.info("Defining the handlers ...")
        self.handlers()

        logger.info("Starting the bots ...")
        self.bot.infinity_polling()

    def handlers(self):

        ######################################     START COMMAND HANDLER     ######################################
        @self.bot.message_handler(commands=["start"])
        def start_command(message):

            ################## TEXT ##################
            start_game_text =("""Hello and Welcome to this bot. \n\n"""
                            """Let see the bot status using the "Bot Status" button""")
            after_start_str= [emojize(':plus: Start a new Game')]
            ################## KEYBOARD ##################
            start_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            after_start_str= [emojize(':white_exclamation_mark:Bot Status:white_exclamation_mark:')]
            buttons = map(types.KeyboardButton, after_start_str)
            start_keyboard.add(*buttons)
            ################## MESSAGE ##################
            self.bot.send_message(message.chat.id, text=start_game_text,
                                 reply_markup=start_keyboard)
        ######################################      STATUS BOTTON HANDLER     ######################################
        @self.bot.message_handler(regexp=emojize(':white_exclamation_mark:Bot Status:white_exclamation_mark:'))
        def status_button(message):

            status_keyboard = \
                types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            
            if not self.game_exist:
                after_start_command
                self.game_exist = True
                after_start_str= [emojize(':plus: Start a new Game')]
                buttons = map(types.KeyboardButton, after_start_str)
                after_start_keyboard.add(*buttons)
                self.bot.send_message(message.chat.id, text=start_command_text,
                                 reply_markup=after_start_keyboard)

            elif self.game_exist == "joining":

                after_start_str= "Join a Game"
                buttons = map(types.KeyboardButton, after_start_str)
                after_start_keyboard.add(*buttons)
                self.bot.send_message(message.chat.id, text=start_command_text,
                                 reply_markup=after_start_keyboard)

            elif self.game_exist == "ongoing":
                start_command_text = "A game is already being played by the players. you have to wait ..."
                self.bot.send_message(message.chat.id, text=start_command_text)
        
        ######################################     NEW GAME HANDLER     ######################################
        @self.bot.message_handler(regexp=emojize(':plus: Start a new Game'))
        def Start_a_new_game(message):

            self.game_exist = True
            self.admin_id = message.chat.id
            nick_name_text = 'OK, please choose an "ENGLISH" nickname.\n'
            self.bot.send_message(message.chat.id, nick_name_text)

        ######################################     JOIN GAME HANDLER     ######################################
        @self.bot.message_handler(regexp="Join a Game")
        def join_a_game(message):

            nick_name_text = 'OK, please choose an "ENGLISH" nickname.\n'
            self.bot.send_message(message.chat.id, nick_name_text)

        @self.bot.message_handler()
        def nickname(message):
            
            self.bot.send_message(message.chat.id, message.text)
            print(demojize(message.text))

    def is_admin(self, id):

        return self.admin_id == id




        # @self.bot.message_handler()

if __name__ == "__main__":

    my_bot = Bot()
