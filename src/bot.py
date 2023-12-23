from collections import defaultdict

from Constants import keys
import telebot
from emoji import demojize, emojize
from loguru import logger
from telebot import types
from Engines import Avalon_Engine
from random import shuffle

TOKEN = "6468920953:AAHXzkA9iOrVwThJ6pk6kZ06AE7DSOnJVsI"

class Bot():

    def __init__(self):

        self.admin_id = None
        self.temp_admin_id = None
        self.game_admin_id = None
        self.super_admin_id  = 224775397
        self.current_committee = list()

        self.names = ["Amir_1","Amir_2", "Amir_3", "Amir_4",
                        "Amir_5", "Amir_6", "Amir_7", "Amir_8"]
        self.curren_users_id = []
        self.name_to_id = {name: 224775397 for name in self.names}
        self.optional_characters = []
        self.commander_order = []
        
        self.shuffle_commander_order = False
        self.game_state = False
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
            
            if self.game_state == False:

                #### TEXT ####
                text =("""Hello and Welcome to this bot. \n\n"""
                        """You are currently the admin. Let's start a new game""")
                                        
                #### KEYBOARD ####
                buttons_text= [keys.new_game]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

            elif self.game_state == "joining":

                #### TEXT ####
                text =("""Hello and Welcome to this bot. \n\n"""
                       """A game already exist and you can join it.""")
                                        
                #### KEYBOARD ####
                buttons_text= [keys.join_game]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

            elif self.game_state == "ongoing":

                #### TEXT ####
                text =("""Hello and Welcome to this bot. \n\n"""
                        """A game is ongoing. Check again later.""")
                                     
                #### KEYBOARD ####
                buttons_text= [keys.bot_status]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        ######################### I Am Admin Button #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.i_am_admin)
        def i_am_admin_button(message):
            
            if self.game_state == False:

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

            elif self.game_state == "joining":

                #### TEXT ####
                text =("""Hello and Welcome to this bot. \n\n"""
                       """A game already exist and you can join it.""")
                                        
                #### KEYBOARD ####
                buttons_text= [keys.join_game]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

            elif self.game_state == "ongoing":

                #### TEXT ####
                text =("""Hello and Welcome to this bot. \n\n"""
                        """A game is ongoing. Check again later.""")
                                     
                #### KEYBOARD ####
                buttons_text= [keys.bot_status]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        ######################### Fake Admin Button #########################
        @self.bot.message_handler(regexp=keys.i_am_admin)
        def fake_admin_button(message):

            #### TEXT ####
            text =(emojize(" :slightly_smiling_face: Nope, you are not"))
                                     
            #### KEYBOARD ####
            buttons_text= [keys.bot_status, keys.i_am_admin]
            buttons = map(types.KeyboardButton, buttons_text)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(*buttons)
            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        ######################### Start Command #########################
        @self.bot.message_handler(commands=["start"])
        def start_command(message):

            #### TEXT ####
            text =("""Hello and Welcome to this bot. \n\n"""
                    """Let's see the bot status""")

            #### KEYBOARD ####

            buttons_text= [keys.bot_status, keys.i_am_admin]
            buttons = map(types.KeyboardButton, buttons_text)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(*buttons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        ######################### Status Button #########################
        @self.bot.message_handler(regexp=keys.bot_status)
        def status_button(message):
            
            if self.game_state == False:

                #### TEXT ####
                text =("""No game exist. wait for the admin to create a game.""")
                                     
                #### KEYBOARD ####
                buttons_text= [keys.bot_status, keys.i_am_admin]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
                
            elif self.game_state == "ongoing":

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

            elif self.game_state == "joining":

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
        
        ######################### Creat Game #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.new_game)
        def creat_game(message):

            #### ACTIONS ####
            self.game_admin_id = message.chat.id
            self.game_state = "joining"

            self.players[message.chat.id]["name"] =  \
                message.chat.first_name + " " + message.chat.last_name
            self.players[message.chat.id]["user"] = message.chat.username
            self.name_to_id[self.players[message.chat.id]["name"]] = message.chat.id

            #### TEXT ####
            text =("Ok, ask your friends to join the game")

            #### KEYBOARD ####
            buttons_text= [keys.start, keys.terminate]
            buttons = map(types.KeyboardButton, buttons_text)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(*buttons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        ######################### Terminate Game #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.terminate)
        def terminate_game(message):

            #### ACTIONS ####
            self.admin_id = None
            self.temp_admin_id = None
            self.game_admin_id = None
            self.super_admin_id  = 224775397

            self.game_state = False
            self.players = defaultdict(dict)
            self.optional_characters = list()

            #### TEXT ####
            text = "The game has been terminated"

            #### KEYBOARD ####
            markup = types.ReplyKeyboardRemove()

            #### MESSAGE ####
            for player in self.players.keys():
                self.bot.send_message(player, text, reply_markup=markup)

        ######################### Start Game #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.start)
        def start_game(message):

            #### TEXT ####
            text = 'OK, choose your prefered character in game and press OK'
            keyboard = self.character_keyboard()

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

        ######################### Add_Persival_Morgana #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.full_Persival_Morgana)
        @self.bot.message_handler(func=self.is_admin, regexp=keys.Persival_Morgana)
        def Persival_Morgana_button(message):

            #### ACTIONS ####
            if "Persival and Morgana" not in self.optional_characters:
                text = "Persival and Morgana were added to the game"
                self.optional_characters.append("Persival and Morgana")

            else:
                text = "Persvial and Morgana were removed from the game"
                del self.optional_characters[self.optional_characters.index("Persival and Morgana")]

            keyboard = self.character_keyboard()
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

        ######################### Add_Mordred #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.full_Mordred)
        @self.bot.message_handler(func=self.is_admin, regexp=keys.Mordred)
        def Mordred_button(message):

            #### ACTIONS ####
            if "Mordred" not in self.optional_characters:
                text = "Mordred was added to the game"
                self.optional_characters.append("Mordred")

            else:
                text = "Mordred was removed from the game"
                del self.optional_characters[self.optional_characters.index("Mordred")]

            keyboard = self.character_keyboard()
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

        ######################### Add_King #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.full_King)
        @self.bot.message_handler(func=self.is_admin, regexp=keys.King)
        def King_button(message):

            #### ACTIONS ####
            if "King" not in self.optional_characters:
                text = "King Arthur was added to the game"
                self.optional_characters.append("King")

            else:
                text = "King Arthur was removed from the game"
                del self.optional_characters[self.optional_characters.index("King")]

            keyboard = self.character_keyboard()
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

        ######################### Add_Oberon #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.full_Oberon)
        @self.bot.message_handler(func=self.is_admin, regexp=keys.Oberon)
        def Oberon_button(message):

            #### ACTIONS ####
            if "Oberon" not in self.optional_characters:
                text = "Oberon was added to the game"
                self.optional_characters.append("Oberon")

            else:
                text = "Oberon was removed from the game"
                del self.optional_characters[self.optional_characters.index("Oberon")]

            keyboard = self.character_keyboard()
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

        ######################### Join Game #########################
        @self.bot.message_handler(regexp=keys.join_game)
        def join_game(message):
            
            #### ACTIONS ####
            self.players[message.chat.id]["name"] =  \
                message.chat.first_name + " " + message.chat.last_name
            self.players[message.chat.id]["user"] = message.chat.username
            name = self.players[message.chat.id]["name"]
            self.name_to_id[self.players[message.chat.id]["name"]] = message.chat.id
            text = f"You have join the game sucessfuly \n"\
                    f"your name in the game: {name}.\n\n"\
                    "Wait for the admin to start the game."

            text_to_admin = f"{name} has joined the game"
            markup = types.ReplyKeyboardRemove()
            self.bot.send_message(message.chat.id, text, reply_markup=markup)
            self.bot.send_message(self.game_admin_id, text_to_admin)

        ######################### Join Game #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.finished_choosing)
        def send_info(message):

            #### ACTIONS ####
            self.extract_names()

            Game = Avalon_Engine(self.names, self.optional_characters)

            for name, character in Game.assigned_character.items():

                message = character.message
                self.bot.send_message(self.name_to_id[name], message)

                if character.has_info:
                    
                    c_1 = character.name == "Minion"
                    c_2 = character.name == "Assassin"
                    c_3 = character.name == "Morgana"
                    c_4 = character.name == "Mordred"
                    
                    if c_1 or c_2 or c_3 or c_4:

                        info = "\n".join(Game.all_info["Evil_Team"])

                        self.bot.send_message(self.name_to_id[name], info)

                    else:

                        info = "\n".join(Game.all_info[character.name])
                        self.bot.send_message(self.name_to_id[name], info)


            self.commander_order = list(self.name_to_id.keys())[:]

            if self.shuffle_commander_order:

                shuffle(self.commander_order)
        
            commander_order_message_1 = "Here is the order of the commanders.\n"
            commander_order_message_2 = "\n:downwards_button:\n".join(self.commander_order)
            text = emojize(commander_order_message_1 + commander_order_message_2)

            for id in self.name_to_id.values():

                self.bot.send_message(id, text)

            self.resolve_commander()
            commander_id = self.name_to_id[self.current_commander]
            n_committee = Game.all_round[Game.round]
            commander_text = "It's your turn to choose your committee. "\
                                f"In this round, you should choose {n_committee} player."

            keyboard = self.committee_keyboard()
            self.bot.send_message(commander_id, commander_text, reply_markup = keyboard)


        ######################### committee add and remove #########################
        @self.bot.message_handler(func=self.is_commander, content_types =[])
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

        ######################### committee propose #########################
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

        ######################### committee final #########################
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

        ######################### vote inside #########################
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

        ######################### mission out #########################
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

        ######################### mission vote #########################
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
            
            keyboard = self.committee_keyboard()
            self.bot.send_message(message.chat.id, demojize(message.text), reply_markup=keyboard)

    ######################### Auxilary Functions #########################
    def is_super_admin(self, message):
        return self.super_admin_id == message.chat.id

    def is_admin(self, message):
        return ((self.super_admin_id == message.chat.id) or
                (self.admin_id == message.chat.id))

    def character_keyboard(self):

        condition_1 = "Persival and Morgana" in self.optional_characters
        condition_2 = "Mordred" in self.optional_characters
        condition_3 = "Oberon" in self.optional_characters
        condition_4 = "King" in self.optional_characters
        current_presival_Morgana = (keys.full_Persival_Morgana if condition_1 else keys.Persival_Morgana)
        current_king = keys.full_Mordred if condition_2 else keys.Mordred
        current_mordred = keys.full_Oberon if condition_3 else keys.Oberon
        current_oberon = keys.full_King if condition_4 else keys.King

        buttons_text_1 = [current_presival_Morgana, current_king]
        buttons_text_2 = [current_oberon, current_mordred]
        buttons_text_3 = [keys.finished_choosing, keys.terminate]

        first_row_buttons = map(types.KeyboardButton, buttons_text_1)
        second_row_buttons = map(types.KeyboardButton, buttons_text_2)
        third_row_buttons = map(types.KeyboardButton, buttons_text_3)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        keyboard.add(*first_row_buttons)
        keyboard.add(*second_row_buttons)
        keyboard.add(*third_row_buttons)

        return keyboard

    def first_commander_keyboard(self):

        buttons_str = [keys.finished_choosing, keys.terminate]
        buttons = map(types.KeyboardButton, buttons_str)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(*buttons)

        return keyboard

    def committee_keyboard(self):
        
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        for name in self.names:

            if name in self.current_committee:

                temp_str = ":check_box_with_check:"

            else:

                temp_str = ""

            button = types.KeyboardButton(emojize(f"{temp_str}{name}"))
            keyboard.row(button)

        buttons_str = [keys.propose, keys.final_decision]
        buttons = map(types.KeyboardButton, buttons_str)
        keyboard.row(*buttons)

        return keyboard


    def mission_keyboard(self):

        buttons_str = [keys.success, keys.fail]
        buttons = map(types.KeyboardButton, buttons_str)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(*buttons)
        return keyboard

    def extract_names(self):

        for player_info in self.players.values():

            self.names.append(player_info["name"])

    def resolve_commander(self):
        
        self.current_commander = self.commander_order[0]
        self.commander_order.append(self.commander_order[0])
        del self.commander_order [0]

    def is_commander(self, message):

        return(self.name_to_id[self.current_commander] == message.chat.id)

if __name__ == "__main__":

    my_bot = Bot()
