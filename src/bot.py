from collections import defaultdict

from Constants import keys,States
import telebot
from emoji import demojize, emojize
from loguru import logger
from telebot import types
from Engines import Avalon_Engine
from random import shuffle
# from utils.io import write_json
# write_json(message, Message.json)

TOKEN = "6468920953:AAHXzkA9iOrVwThJ6pk6kZ06AE7DSOnJVsI"

class Bot():

    def initial_condition(self):

        self.admin_id = None
        self.temp_admin_id = int()
        self.game_admin_id = int()
        self.super_admin_id  = 224775397
        self.current_committee = list()
        self.committee_voters = list()
        self.current_commander = str()
        self.committee_votes = list()
        self.mission_votes = list()

        self.names = ["Amir Hamidi", "Amir_1","Amir_2", "Amir_3", "Amir_4",
                        "Amir_5", "Amir_6", "Amir_7", "Amir_8"]
        self.choosed_names = [emojize(f"{keys.check_box}{name}")\
                               for name in self.names]
        self.names_to_ids = {name: 224775397 for name in self.names}
        # self.names = []
        # self.names_to_ids = []

        self.curren_users_id = []
        self.optional_characters = []
        self.commander_order = []
        
        self.shuffle_commander_order = False
        self.game_state = States.no_game
    def define_game(self, names, optional_characters):

        self.Game = Avalon_Engine(names, optional_characters)

    def __init__(self):

        self.initial_condition()
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
            
            if self.game_state == States.no_game:

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

            elif self.game_state == States.starting:

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

            elif self.game_state == States.ongoing:

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
            
            if self.game_state == States.no_game:

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

            elif self.game_state == States.starting:

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

            elif self.game_state == States.ongoing:

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
            text =(emojize(":slightly_smiling_face: Nope, you are not"))
                                     
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
            
            if self.game_state == States.no_game:

                #### TEXT ####
                text =("""No game exist. wait for the admin to create a game.""")
                                     
                #### KEYBOARD ####
                buttons_text= [keys.bot_status, keys.i_am_admin]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
                
            elif self.game_state == States.ongoing:

                #### TEXT ####
                text =("""A game is ongoing. Check again later.""")
                                     
                #### KEYBOARD ####
                buttons_text= [keys.bot_status]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                #### MESSAGE ####
                self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

            elif self.game_state == States.starting:

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
            self.game_state = States.starting

            name = self.grab_name(message)
            self.names_to_ids[name] = message.chat.id
            self.names.append(name)
            self.choosed_names.append(emojize(f"{keys.check_box}{name}"))

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
            self.initial_condition()

            #### TEXT ####
            text = "The game has been terminated"

            #### KEYBOARD ####
            markup = types.ReplyKeyboardRemove()

            #### MESSAGE ####
            for id in self.names_to_ids.values():
                self.bot.send_message(id, text, reply_markup=markup)

        ######################### Start Game #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.start)
        def start_game(message):

            #### TEXT ####
            text = 'OK, choose your prefered character in game and press OK'
            keyboard = self.character_keyboard()
            self.names
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
            name = self.grab_name(message)
            self.names_to_ids[name] = message.chat.id
            self.names.append(name)
            self.choosed_names.append(emojize(f"{keys.check_box}{name}"))

            text = f"You have join the game sucessfuly \n"\
                    f"your name in the game: {name}.\n\n"\
                        "Wait for the admin to start the game."
            
            text_to_admin = f"{name} has joined the game"
            markup = types.ReplyKeyboardRemove()
            self.bot.send_message(message.chat.id, text, reply_markup=markup)
            self.bot.send_message(self.game_admin_id, text_to_admin)

        ######################### Send Info #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.finished_choosing)
        def send_info(message):

            #### ACTIONS ####
            # send assasin the button
            self.define_game(self.names, self.optional_characters)

            for name, character in self.Game.assigned_character.items():

                message = character.message
                self.bot.send_message(self.names_to_ids[name], message)

                if character.has_info:
                    
                    c_1 = character.name == "Minion"
                    c_2 = character.name == "Assassin"
                    c_3 = character.name == "Morgana"
                    c_4 = character.name == "Mordred"
                    
                    if c_1 or c_2 or c_3 or c_4:

                        info = "\n".join(self.Game.all_info["Evil_Team"])

                        self.bot.send_message(self.names_to_ids[name], info)

                    else:

                        info = "\n".join(self.Game.all_info[character.name])
                        self.bot.send_message(self.names_to_ids[name], info)


            self.commander_order = list(self.names_to_ids.keys())[:]

            if self.shuffle_commander_order:

                shuffle(self.commander_order)
        
            commander_order_message_1 = "Here is the order of the commanders.\n"
            commander_order_message_2 = "\n:downwards_button:\n".join(self.commander_order)
            text = emojize(commander_order_message_1 + commander_order_message_2)

            for _, id in self.names_to_ids.values():

                self.bot.send_message(id, text)

            self.resolve_commander()
            commander_id = self.names_to_ids[self.current_commander]

            n_committee = self.Game.all_round[self.Game.round]
            commander_text = "It's your turn to choose your committee. "\
                                f"In this round, you should pick {n_committee} player."

            keyboard = self.commander_keyboard()
            self.bot.send_message(commander_id, commander_text, reply_markup = keyboard)
            self.game_state = States.committee_choose

        ######################### ccommander choosing name #########################
        @self.bot.message_handler(func=self.is_commander_choosing_name)
        def commander_choose_name(message):

            add_remove_name = self.correct_name(message.text)
            if add_remove_name in self.current_committee:
                del self.current_committee[self.current_committee.index(add_remove_name)]
                text = f"{add_remove_name} was removed from the committee"

            else:
                self.current_committee.append(message.text)
                text = f"{add_remove_name} was add to the committee"

            keyboard = self.commander_keyboard()

            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

        ######################### commander pressing_button #########################
        @self.bot.message_handler(func=self.is_commander_pressing_button)
        def commander_press_button(message):
            
            # adding the rule that the number of committee members are equal to the right number
            if message.text == keys.propose:

                committee_member_text = "\n".join(self.current_committee)
                whole_text = text + committee_member_text
                keyboard = self.remove_keyboard()

                for _, id in self.names_to_ids.items():

                    if id != message.chat.id:

                        self.bot.send_message(id, whole_text, reply_markup=keyboard)

            elif message.text == keys.final:

                text = "Final Decision:\n"
                committee_member_text = "\n".join(self.current_committee)
                whole_text = text + committee_member_text
                keyboard = self.committee_vote_keyboard()
                self.committee_voters = self.names[:]

                for _, id in self.names_to_ids.items():
                    self.bot.send_message(id, whole_text, reply_markup=keyboard)

        ######################### vote inside #########################
        @self.bot.message_handler(func=self.is_eligible_vote)
        def vote_for_committee(message):

            self.committee_voters.remove(self.grab_name(message))
            if self.committee_voters:
                
                name = self.grab_name(message)
                self.transfer_committee_vote(message)

                text = emojize(f"{name} voted: {message}")
                self.bot.send_message(message.chat.id, text)

            else:

                name = self.grab_name(message)
                self.transfer_committee_vote(message)

                text = emojize(f"{name} voted: {message}")
                self.bot.send_message(message.chat.id, text)

                self.Game.count_committee_vote(self.committee_votes)

                if self.Game.committee_accept:

                    members_text = "the proposed committee was accepted"
                    committee_text  ="Please choose between Fail and Success"

                    for _, id in self.names_to_ids.items():

                        self.bot.send_message(id, members_text)

                    for name in self.current_committee:

                        id = self.names_to_ids[name]
                        keyboard = self.mission_keyboard()
                        self.bot.send_message(id, committee_text, reply_markup=keyboard)

                elif self.Game.reject_count == 5:

                    self.Game.continues = False
                    self.Game.win_side = "Evil"

                    for _, id in self.names_to_ids.items():
                        
                        text = "Evil Won.\n Reason: 5 consecitive rejection of the committee"
                        self.bot.send_message(id, text)

                else:

                    members_text = "the proposed committee was rejected"
                    n_committee = self.Game.all_round[self.Game.round]
                    commander_text = "It's your turn to choose your committee. "\
                                f"In this round, you should pick {n_committee} player."

                    for _, id in self.names_to_ids.items():

                        self.bot.send_message(id, members_text)

                    commander_id = self.commander_order[0]
                    self.resolve_commander()
                    keyboard = self.commander_keyboard()
                    self.bot.send_message(commander_id, commander_text, reply_markup=keyboard)

        ######################### mission out #########################
        @self.bot.message_handler(func=self.is_eligible_fail_success)
        def vote_for_mission(message):
            
            self.current_committee.remove(self.grab_name(message))

            if self.current_committee:

                pass

            else:

                self.Game.mission_result(self.mission_votes)

                if self.Game.evil_wins == 3:

                    for _, id in self.names_to_ids.items():
                        
                        text = "Evil Won.\n Reason: thye won three times"
                        self.bot.send_message(id, text)

                elif self.Game.city_wins == 3:

                    text = "City won 3 rounds, it is time for assassin to shoot"
                    self.bot.send_message(id, text)
                    assassin_text = "who do you want to shoot?"
                    assassin_id = 12
                    self.bot.send_message(assassin_id, text)

                else:

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
            
            self.bot.send_message(message.chat.id, demojize(message.text))

    ######################### rule checkers #########################
    def is_super_admin(self, message):

        c_1 = self.super_admin_id == message.chat.id

        return c_1

    def is_admin(self, message):

        c_1 = self.is_super_admin(message)
        c_2 = self.admin_id == message.chat.id

        return c_1 or c_2

    def is_commander(self, message):

        c_1 = self.current_commander == self.grab_name(message)
        print(self.current_commander)
        return c_1

    def is_in_current_committee(self, message):

        c_1 = self.grab_name(message) in self.current_committee
        return c_1

    def is_commander_choosing_name(self,message):

        c_1 = self.game_state == States.committee_choose
        c_2 = self.is_commander(message)
        c_3 = message.text in self.names
        c_4 = message.text in self.choosed_names

        return c_1 and c_2 and (c_3 or c_4)

    def is_commander_pressing_button(self, message):

        c_1 = self.game_state == States.committee_choose
        c_2 = self.is_commander(message)
        c_3 = message.text in [keys.final, keys.propose]
        print(c_1, c_2, c_3)

        return c_1 and c_2 and c_3

    def is_eligible_vote(self, message):

        name = self.grab_name(message)
        c_1 = self.game_state == States.committee_voting
        c_2 = emojize(message.text) in [keys.agree, keys.disagree]
        c_3 = name in self.committee_voters

        return c_1 and c_2 and c_3

    def is_eligible_fail_success(self, message):

        c_1 = self.is_in_current_committee(message)
        c_2 = message.text in [keys.success, keys.fail]
        c_3 = self.game_state = States.mission_voting

        return c_1 and c_2 and c_3

    ######################### keyboard makers #########################
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

    def commander_keyboard(self):
        
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        for name in self.names:

            if name in self.current_committee:

                temp_str = ":check_box_with_check:"

            else:

                temp_str = ""

            button = types.KeyboardButton(emojize(f"{temp_str}{name}"))
            keyboard.row(button)

        buttons_str = [keys.propose, keys.final]
        buttons = map(types.KeyboardButton, buttons_str)
        keyboard.row(*buttons)

        return keyboard

    def committee_vote_keyboard(self):

        buttons_str = [keys.agree, keys.disagree]
        buttons = map(types.KeyboardButton, buttons_str)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(*buttons)
        return keyboard

    def mission_keyboard(self):

        buttons_str = [keys.success, keys.fail]
        buttons = map(types.KeyboardButton, buttons_str)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(*buttons)
        return keyboard

    def remove_keyboard(self):
        return types.ReplyKeyboardRemove()

    ######################### auxilary functions #########################
    def resolve_commander(self):
        
        self.current_commander = self.commander_order[0]
        self.commander_order.append(self.commander_order[0])
        del self.commander_order [0]

    def grab_name(self, message):
        
        name = str()

        if((message.chat.first_name != None) and (message.chat.last_name != None)):
            name = message.chat.first_name + " " + message.chat.last_name

        elif not (message.chat.last_name):
            name = message.chat.first_name

        elif not (message.chat.first_name):
            name = message.chat.last_name

        return name

    def correct_name(self, currupted_name):

        if currupted_name[0:len(keys.check_box)] == keys.check_box:

            return currupted_name[len(keys.check_box):]

        else:

            return currupted_name

    def transfer_committee_vote(self, message):

        if message.text == keys.agree:
            self.committee_votes.append(1)

        elif message.text == keys.disagree:
            self.committee_votes.append(0)

    def transfer_mission_vote(self, message):

        if message.text == keys.success:
            self.mission_votes.append(1)

        elif message.text == keys.fail:
            self.mission_votes.append(0)

if __name__ == "__main__":

    my_bot = Bot()
