from collections import defaultdict

from constants import keys
import telebot
from emoji import demojize, emojize
from loguru import logger
from telebot import types

TOKEN = "6468920953:AAHXzkA9iOrVwThJ6pk6kZ06AE7DSOnJVsI"

class Bot():

    def __init__(self):

        self.admin_id = None
        self.temp_admin_id = None
        self.super_admin_id  = 224775397
        self.game_admin_id = None

        self.game_exist = False
        self.players = defaultdict(dict)
        self.bot = telebot.TeleBot(TOKEN)

        #### Initializing the bot ####
        logger.info("Defining the handlers ...")
        self.handlers()

        #### Running the bot ####
        logger.info("Starting the bots ...")
        self.bot.infinity_polling()

    def handlers(self):

        ######################### Admin Start Command #########################
        @self.bot.message_handler(func=self.is_admin, commands=["start"])
        def admin_start_command(message):

            #### ACTIONS ####

            #### TEXT ####
            text =("""Hello and Welcome to this bot. \n\n"""
                    """You are currently the admin. Let's start a new game""")
                                     
            #### KEYBOARD ####
            buttons_text= [keys.new_game, keys.bot_status]
            buttons = map(types.KeyboardButton, buttons_text)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(*buttons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        ######################### I Am Admin Button #########################
        @self.bot.message_handler( func=self.is_admin, regexp=keys.is_admin)
        def i_am_admin_button(message):

            #### ACTIONS ####
            #### TEXT ####
            text =("""Hello and Welcome to this bot. \n\n"""
                    """You are currently the admin. Let's start a new game.""")
                                     
            #### KEYBOARD ####
            buttons_text= [keys.new_game]
            buttons = map(types.KeyboardButton, buttons_text)
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            keyboard.add(*buttons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        ######################### Fake Admin Button #########################
        @self.bot.message_handler(regexp=keys.is_admin)
        def fake_admin_button(message):

            #### ACTIONS ####
            #### TEXT ####
            text =(emojize(" :slightly_smiling_face: Nope, you are not"))
                                     
            #### KEYBOARD ####
            buttons_text= [keys.bot_status, keys.is_admin]
            buttons = map(types.KeyboardButton, buttons_text)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(*buttons)
            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        ######################### Start Command #########################
        @self.bot.message_handler(commands=["start"])
        def start_command(message):

            #### ACTIONS ####

            #### TEXT ####
            text =("""Hello and Welcome to this bot. \n\n"""
                    """Let's see the bot status""")

            #### KEYBOARD ####

            buttons_text= [keys.bot_status, keys.is_admin]
            buttons = map(types.KeyboardButton, buttons_text)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(*buttons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        ######################### Status Button #########################
        @self.bot.message_handler(regexp=keys.bot_status)
        def status_button(message):
            
            if self.game_exist == False:

                #### ACTIONS ####

                #### TEXT ####
                text =("""No game exist. wait for the admin to create a game.""")
                                     
                #### KEYBOARD ####
                buttons_text= [keys.bot_status, keys.is_admin]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
                
            elif self.game_exist == "ongoing":

                #### ACTIONS ####

                #### TEXT ####
                text =("""A game is ongoing. Check again later.""")
                                     
                #### KEYBOARD ####
                buttons_text= [keys.bot_status]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

            elif self.game_exist == "joining":

                #### ACTIONS ####

                #### TEXT ####
                text =("""A game already exist and you can join it.""")
                                     
                #### KEYBOARD ####
                buttons_text= [keys.join_game]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
        
        ######################### Print Input #########################
        @self.bot.message_handler(regexp=keys.new_game)
        def new_game(message):

            #### ACTIONS ####
            self.game_admin_id = message.chat.id
            self.game_exist = "joining"
            #### TEXT ####

            text =("Ok, ask your friends to join the game")

            #### KEYBOARD ####

            buttons_text= [keys.start, keys.terminate]
            buttons = map(types.KeyboardButton, buttons_text)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(*buttons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        @self.bot.message_handler(regexp=keys.start)
        def start_game(message):

            #### ACTIONS ####

            #### TEXT ####
            text = 'OK, choose your prefered character in game and press OK'

            #### KEYBOARD ####
            buttons_text_1= [keys.Persival_Morgana, keys.King]
            buttons_text_2= [keys.Oberon, keys.Mordred]
            buttons_text_3= [keys.OK]

            first_row_buttons = map(types.KeyboardButton, buttons_text_1)
            second_row_buttons =map(types.KeyboardButton, buttons_text_2)
            third_row_buttons =map(types.KeyboardButton, buttons_text_3)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

            keyboard.add(*first_row_buttons)
            keyboard.add(*second_row_buttons)
            keyboard.add(*third_row_buttons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
        
        @self.bot.message_handler(regexp=keys.start)
        def start_game(message):

            #### ACTIONS ####

            #### TEXT ####
            text = 'OK, choose your prefered character in game and press OK'

            #### KEYBOARD ####
            buttons_text_1= [keys.Persival_Morgana, keys.King]
            buttons_text_2= [keys.Oberon, keys.Mordred]
            buttons_text_3= [keys.OK]

            first_row_buttons = map(types.KeyboardButton, buttons_text_1)
            second_row_buttons =map(types.KeyboardButton, buttons_text_2)
            third_row_buttons =map(types.KeyboardButton, buttons_text_3)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            
            keyboard.add(*first_row_buttons)
            keyboard.add(*second_row_buttons)
            keyboard.add(*third_row_buttons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
        ######################### Hoin Game #########################
        @self.bot.message_handler(regexp=keys.join_game)
        def join_game(message):
            
            #### ACTIONS ####
            self.players[message.chat.id]["name"] =  \
                message.chat.first_name + " " + message.chat.last_name
            self.players[message.chat.id]["user"] = message.chat.username
            name = self.players[message.chat.id]["name"]

            text = f"You have join the game sucessfuly \n"\
                    f"your name in the game: {name}.\n\n"\
                    "Wait for the admin to start the game."

            text_to_admin = f"{name} has joing the game"
            markup = types.ReplyKeyboardRemove()
            self.bot.send_message(message.chat.id, text, reply_markup=markup)
            self.bot.send_message(self.game_admin_id, text_to_admin)

        ######################### Admin Request #########################
        @self.bot.message_handler(regexp=keys.join_game)
        def choose_character(message):
            pass

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

        ######################### Print Input #########################
        @self.bot.message_handler()
        def print_function(message):

            print(demojize(message.text))

    ######################### Auxilary Functions #########################
    def is_super_admin(self, message):
        return self.super_admin_id == message.chat.id

    def is_admin(self, message):
        return ((self.super_admin_id == message.chat.id) or
                (self.admin_id == message.chat.id))

if __name__ == "__main__":

    my_bot = Bot()
