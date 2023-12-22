from collections import defaultdict

import telebot
from emoji import emojize
from loguru import logger
from telebot import types

TOKEN = "6468920953:AAHXzkA9iOrVwThJ6pk6kZ06AE7DSOnJVsI"

class Bot():

    def __init__(self):

        self.admin_id = None
        self.temp_admin_id = None
        self.super_admin_id  = 224775397

        self.game_exist = False
        self.players = defaultdict(list)
        self.bot = telebot.TeleBot(TOKEN)

        #### Initializing the bot ####
        logger.info("Defining the handlers ...")
        self.handlers()

        #### Running the bot ####
        logger.info("Starting the bots ...")
        self.bot.infinity_polling()

    def handlers(self):

        ######################### admin start command #########################
        @self.bot.message_handler(func=self.is_admin, commands=["start"])
        def admin_start_command(message):

            #### ACTIONS ####

            #### TEXT ####
            admin_start_command_text =("""Hello and Welcome to this bot. \n\n"""
                                       """You are currently the admin. Let's start a new game""")
                                     
            #### KEYBOARD ####
            admin_start_command_bottons_text= [emojize(':plus: Start a new Game')]
            admin_start_command_bottons = map(types.KeyboardButton, admin_start_command_bottons_text)
            admin_start_command_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            admin_start_command_keyboard.add(*admin_start_command_bottons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=admin_start_command_text,
                                  reply_markup=admin_start_command_keyboard)

        ######################### start command #########################
        @self.bot.message_handler(commands=["start"])
        def start_command(message):

            #### ACTIONS ####

            #### TEXT ####
            start_command_text =("""Hello and Welcome to this bot. \n\n"""
                                 """Let's see the bot status""")

            #### KEYBOARD ####
            start_command_buttons_text= [emojize(':white_exclamation_mark:Bot Status:white_exclamation_mark:')]
            start_command_buttons = map(types.KeyboardButton, start_command_buttons_text)
            start_command_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            start_command_keyboard.add(*start_command_buttons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=start_command_text,
                                 reply_markup=start_command_keyboard)

        ######################### Status Button #########################
        @self.bot.message_handler(regexp=emojize(':white_exclamation_mark:Bot Status:white_exclamation_mark:'))
        def status_button(message):

            if self.game_exist == False:

                #### ACTIONS ####

                #### TEXT ####
                status_button_text =("""No game exist. wait for the admin to create a game.""")
                                     
                #### KEYBOARD ####
                status_botton_bottons_text= [emojize(':white_exclamation_mark:Bot Status:white_exclamation_mark:')]
                status_botton_bottons = map(types.KeyboardButton, status_botton_bottons_text)
                status_botton_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                status_botton_keyboard.add(*status_botton_bottons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=status_button_text,
                                 reply_markup=status_botton_keyboard)
                
            elif self.game_exist == "ongoing":

                #### ACTIONS ####

                #### TEXT ####
                status_button_text =("""A game is ongoing. Check again later.""")
                                     
                #### KEYBOARD ####
                status_botton_bottons_text= [emojize(':white_exclamation_mark:Bot Status:white_exclamation_mark:')]
                status_botton_bottons = map(types.KeyboardButton, status_botton_bottons_text)
                status_botton_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                status_botton_keyboard.add(*status_botton_bottons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=status_button_text,
                                 reply_markup=status_botton_keyboard)

            elif self.game_exist == "joining":
                
                #### ACTIONS ####

                #### TEXT ####
                status_button_text =("""A game already exist and you can join it.""")
                                     
                #### KEYBOARD ####
                status_botton_bottons_text= [emojize(':plus: Joing the game')]
                status_botton_bottons = map(types.KeyboardButton, status_botton_bottons_text)
                status_botton_keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                status_botton_keyboard.add(*status_botton_bottons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=status_button_text,
                                 reply_markup=status_botton_keyboard)
        
        ######################### Admin Request #########################
        @self.bot.message_handler(regexp="Join a Game")
        def join_a_game(message):

            nick_name_text = 'OK, please choose an "ENGLISH" nickname.\n'
            self.bot.send_message(message.chat.id, nick_name_text)

        ######################### Admin Request #########################
        @self.bot.message_handler(commands=["adminrequest"])
        def admin_request(message):
            
            request = f"{message.chat.first_name} {message.chat.last_name} " \
                        f"with usrname {message.chat.username} "\
                            "Requeste for an admin promotion"
            
            self.temp_admin_id = message.chat.id
            message_to_user= "you request has been sent to the super admin."
            self.bot.send_message(self.super_admin_id, request)
            self.bot.send_message(self.super_admin_id, self.temp_admin_id)
            self.bot.send_message(message.chat.id, message_to_user)
        
        ######################### Accept Request #########################
        @self.bot.message_handler(func = self.is_super_admin,
                                    commands=["acceptadmin"])
        def accept_request(message):

            self.admin_id = self.temp_admin_id
            answer = f"you are now an admin"
            admin_answer = f"{self.temp_admin_id} is now an admin"
            self.bot.send_message(self.temp_admin_id, answer)
            self.bot.send_message(message.chat.id, admin_answer)
    ######################### Auxilary Functions #########################
    def is_super_admin(self, message):
        return self.super_admin_id == message.chat.id

    def is_admin(self, message):
        return ((self.super_admin_id == message.chat.id) or
                (self.admin_id == message.chat.id))

if __name__ == "__main__":

    my_bot = Bot()
