import os
from collections import defaultdict
import re

from Constants import keys, States
import telebot
from emoji import demojize, emojize
from loguru import logger
from telebot import types
from Engines import Avalon_Engine
from random import shuffle
from utils.io import read_txt_file

current_working_directory = os.getcwd()
TOKEN = read_txt_file(f"{current_working_directory}\\src\\Data\\Bot_Token.txt")

class Bot():
        
    def print_instance_attributes(self):
    
        print("Game State:",self.game_state, sep=" --> ")
        print("Game_admin", self.game_admin_id, sep=" --> ")
        print("Names:", self.names, sep=" --> ")
        print("checked Names:", self.checked_names, sep=" --> ")
        print("Names to Ids:", self.names_to_ids, sep=" --> ")
        print("choosed characters:",self.choosed_characters, sep=" --> ")
        print("commander order:",self.commander_order, sep=" --> ")
        print("current commander:", self.current_commander, sep=" --> ")
        print("current committee:", self.mission_voters, sep=" --> ")
        print("committee voters:", self.committee_voters, sep=" --> ")
        print("committee votes:", self.committee_votes, sep=" --> ")
        print("mission votes:", self.mission_votes, sep=" --> ")
        print("king id:", self.king_id, sep=" --> ")
        print("assassin id:", self.assassin_id, sep=" --> ")

    def initial_condition(self):

        self.super_admin_id  = 224775397
        self.admin_id = None
        self.temp_admin_id = int()
        self.game_admin_id = int()

        self.game_state = States.no_game

        ############### Temp ###############
        self.names = ["Amir Hamidi", "Amir 1", "Amir 2", "amir 3"]
        self.checked_names = [emojize(f"{keys.check_box}{name}") for name in self.names]

        self.ids = [224775397, 224775397, 224775397, 224775397]

        self.names_to_ids = {name : id for name, id in zip(self.names, self.ids)}
        self.ids_to_names = {id : name for name, id in zip(self.names, self.ids)}
        ############### Temp ###############

        ############### main ###############
        # self.names = list()
        # self.checked_names = list()
        # self.ids = list()

        # self.ids_to_names = dict()
        # self.names_to_ids = dict()
        ############### main ###############

        self.choosed_characters = ["Merlin", "Assassin"]
        self.optional_characters = [keys.Persival_Morgana, keys.Mordred, keys.King, keys.Oberon]
        self.checked_optional_characters = [f"{keys.check_box}{name}" for name in self.optional_characters]
        self.Evil_team_id = list()

        self.commander_order = list()
        self.current_commander = str()
        self.shuffle_commander_order = False

        self.committee_voters = list()
        self.committee_votes = list()

        self.mission_voters = list()
        self.mission_votes = list()

        self.king_id = int()
        self.names_to_send_to_king = list()
        self.checked_names_to_send_to_king = list()
        self.kings_guess = list()
        
        self.assassin_id = int()
        self.names_to_send_to_assassin = list()
        self.checked_names_to_send_to_assassin = list()
        self.assassins_guess = str()

        self.summary_voting_text = list()

        self.someone_requested = False
        self.requested_name = None
        self.committee_summary = str()
        self.mission_summary = str()
        self.all_time_summary = str()


    def __init__(self):

        self.initial_condition()
        self.bot = telebot.TeleBot(TOKEN)

        #### Initializing the bot ####
        logger.info("Defining the handlers ...")
        self.handlers()

        #### Running the bot ####
        logger.info("Starting the bots ...")
        self.bot.infinity_polling()

    def grab_name(self, message):
        
        name = str()

        if((message.chat.first_name != None) and (message.chat.last_name != None)):
            name = message.chat.first_name + " " + message.chat.last_name

        elif not (message.chat.last_name):
            name = message.chat.first_name

        elif not (message.chat.first_name):
            name = message.chat.last_name

        return name

    def fix_name(self, currupted_name):

        if currupted_name[0:len(keys.check_box)] == keys.check_box:

            return currupted_name[len(keys.check_box):]

        else:

            return currupted_name
    
    def add_player(self, message):

        name = self.grab_name(message)
        id = message.chat.id

        if name in self.names:

            similar_name = self.names.count(name)
            name = f"{name}_{similar_name}"

            self.names.append(name)
            self.ids.append(id)

            self.checked_names.append(emojize(f"{keys.check_box}{name}"))

            self.names_to_ids[name] = id
            self.ids_to_names[id] = name

        else:

            self.names.append(name)
            self.ids.append(id)

            self.checked_names.append(emojize(f"{keys.check_box}{name}"))

            self.names_to_ids[name] = id
            self.ids_to_names[id] = name

    def define_game(self):
        
        name_for_game = self.names[:]
        character_fo_game = self.choosed_characters[:]

        self.Game = Avalon_Engine(name_for_game, character_fo_game)
    
    def handlers(self):

        ######################### Admin Start Command #########################
        @self.bot.message_handler(func=self.is_admin, commands=["start"])
        def admin_start_command(message):
            print("admin_start_command")

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
         
        ######################### Start Command #########################
        @self.bot.message_handler(commands=["start"])
        def start_command(message):
            print("start_command")

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

        ######################### I Am Admin Button #########################
        @self.bot.message_handler(func=self.is_admin, regexp=keys.i_am_admin)
        def i_am_admin_button(message):
            print("start_command")
            
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
            print("fake_admin_button")

            #### TEXT ####
            text =(emojize(":slightly_smiling_face: Nope, you are not"))
                                     
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
            print("status_button")
            
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
            print("create_game")

            #### ACTIONS ####
            self.game_admin_id = message.chat.id
            self.game_state = States.starting
            self.add_player(message)
            
            #### TEXT ####
            text =("Ok, ask your friends to join the game")

            #### KEYBOARD ####
            buttons_text= [keys.choose_character]
            buttons = map(types.KeyboardButton, buttons_text)
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            keyboard.add(*buttons)

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

        ######################### Terminate Game #########################
        @self.bot.message_handler(func=self.is_game_admin, commands=["terminate"])
        def terminate_game(message):
            print("terminate_game")

            #### ACTIONS ####
            self.initial_condition()

            #### TEXT ####
            text = "The game has been terminated"

            #### KEYBOARD ####
            markup = types.ReplyKeyboardRemove()

            #### MESSAGE ####
            for id in self.ids:
                self.bot.send_message(id, text, reply_markup=markup)

            self.game_state = States.no_game
        
        ######################### Start Game #########################
        @self.bot.message_handler(func=self.is_game_admin, regexp=keys.choose_character)
        def start_game(message):
            print("start_game")

            self.game_state = States.ongoing

            #### TEXT ####
            text = 'OK, choose your prefered character in the game.'
            keyboard = self.character_keyboard()

            #### MESSAGE ####
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
        
        ######################### admin choosing character #########################
        @self.bot.message_handler(func=self.is_admin_choosing_character)
        def admin_choose_characters(message):
            print("admin_choose_characters")

            add_remove_character = self.fix_name(message.text)

            if add_remove_character in self.choosed_characters:

                self.choosed_characters.remove(add_remove_character)
                text = f"{add_remove_character} was removed from the game"

            else:
                self.choosed_characters.append(add_remove_character)
                text = f"{add_remove_character} was added to the game"

            keyboard = self.character_keyboard()

            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
        
        ######################### Join Game #########################
        @self.bot.message_handler(regexp=keys.join_game)
        def join_game(message):
            print("join_game")
            
            #### ACTIONS ####
            self.add_player(message)
            name = self.ids_to_names[message.chat.id]

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
            print("send_info")

            #### ACTIONS ####
            self.define_game()
            self.committee_choosing_init()
            keyboard = self.remove_keyboard()

            for name, character in self.Game.assigned_character.items():

                message = character.message
                self.bot.send_message(self.names_to_ids[name], message)

                if character.name  == "King":
                    self.king_id = self.names_to_ids[name]

                if character.name == "Assassin":
                    self.assassin_id = self.names_to_ids[name]
                    
                if character.has_info:
                    
                    c_1 = character.name == "Minion"
                    c_2 = character.name == "Assassin"
                    c_3 = character.name == "Morgana"
                    c_4 = character.name == "Mordred"
                    c_5 = character.name == "King"

                    if c_1 or c_2 or c_3 or c_4:

                        info = "\n".join(self.Game.all_info["Evil_Team"])
                        self.bot.send_message(self.names_to_ids[name], info, reply_markup=keyboard)
                        self.Evil_team_id.append(self.names_to_ids[name])

                    else:

                        if not c_5:

                            self.names_to_send_to_assassin.append(name)
                            self.checked_names_to_send_to_assassin.append(f"{emojize(keys.check_box)}{name}")
                        
                        info = "\n".join(self.Game.all_info[character.name])
                        self.bot.send_message(self.names_to_ids[name], info, reply_markup=keyboard)


            self.commander_order = self.names[:]
            if self.shuffle_commander_order:

                shuffle(self.commander_order)
        
            commander_order_message_1 = "Here is the order of the commanders.\n"
            commander_order_message_2 = "\n:downwards_button:\n".join(self.commander_order)
            text = emojize(commander_order_message_1 + commander_order_message_2)

            for id in self.ids:

                self.bot.send_message(id, text)

            self.resolve_commander()
            commander_id = self.names_to_ids[self.current_commander]

            n_committee = self.Game.all_round[self.Game.round]
            commander_text = f"It's your turn to choose your committee. In this round, you should pick {n_committee} player."

            keyboard = self.commander_keyboard()
            self.bot.send_message(commander_id, commander_text, reply_markup = keyboard)
            # to committee chosing

        ######################### ccommander choosing name #########################
        @self.bot.message_handler(func=self.is_commander_choosing_name)
        def commander_choose_name(message):
            print("commander_choose_name")

            add_remove_name = self.fix_name(message.text)

            if add_remove_name in self.mission_voters:

                self.mission_voters.remove(add_remove_name)
                text = f"{add_remove_name} was removed from the committee"

            else:

                self.mission_voters.append(add_remove_name)
                text = f"{add_remove_name} was add to the committee"

            keyboard = self.commander_keyboard()
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
            # to committee chosing or committee press button
        ######################### commander pressing_button #########################
        @self.bot.message_handler(func=self.is_commander_pressing_button)
        def commander_press_button(message):
            print("commander_press_button")

            self.Game.check_committee(self.mission_voters)
            
            if self.Game.acceptable_round:

                if message.text == keys.propose:

                    text = f"{keys.propose}:\n"
                    committee_member_text = "\n".join(self.mission_voters)
                    whole_text = text + committee_member_text
                    keyboard = self.remove_keyboard()

                    for id in self.ids:

                        self.bot.send_message(id, whole_text)

                    # to committee choosing (Done)

                elif message.text == keys.final:

                    round = self.Game.round + 1
                    rejected = self.Game.reject_count

                    text = f"{keys.final}:\n"
                    committee_member_text = "\n".join(self.mission_voters)

                    whole_text = text + committee_member_text
                    keyboard = self.committee_vote_keyboard()
                    self.committee_voters = self.names[:]

                    for id in self.ids:
                        self.bot.send_message(id, whole_text, reply_markup=keyboard)

                    self.committee_summary = self.add_committee_header(round, rejected)
                    self.all_time_summary += self.add_committee_header(round, rejected)
                    self.committee_voting_init()

                    # to committee voting (Done)

            else:

                text = "The number of players in the "\
                        f"committee should be {self.Game.all_round[self.Game.round]}"
                
                keyboard = self.commander_keyboard()
                self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
                # to committee choosing (Done)

        ######################### vote inside #########################
        @self.bot.message_handler(func=self.is_eligible_vote)
        def vote_for_committee(message):
            print("vote_for_committee")

            name = self.ids_to_names[message.chat.id]

            if name in self.committee_voters:

                self.committee_voters.remove(name)

                if self.committee_voters:

                    keyboard = self.remove_keyboard()
                    self.transfer_committee_vote(message)

                    text = emojize(f"your vote: {message.text}")
                    self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

                    self.committee_summary += self.add_committee_vote(name, message.text)
                    self.all_time_summary += self.add_committee_vote(name, message.text)
                    # to committee voting (Done)

                else:
                    
                    keyboard = self.remove_keyboard()
                    self.transfer_committee_vote(message)

                    text = emojize(f"your vote: {message.text}")
                    self.bot.send_message(message.chat.id, text, reply_markup=keyboard)


                    self.committee_summary += self.add_committee_vote(name, message.text)
                    self.all_time_summary += self.add_committee_vote(name, message.text)

                    self.Game.count_committee_vote(self.committee_votes)

                    for id in self.ids:

                        self.bot.send_message(id, self.committee_summary)

                    if self.Game.committee_accept:
                        
                        round = self.Game.round + 1
                        self.mission_summary = self.add_mission_header(round)
                        self.all_time_summary += self.add_mission_header(round)

                        self.mission_votes = list()
                        self.Game.round += 1

                        self.game_state = States.mission_voting
                        members_text = "the proposed committee was accepted"
                        committee_text  ="Choose between Fail and Success"

                        for id in self.ids:

                            self.bot.send_message(id, members_text)

                        keyboard = self.mission_keyboard()

                        for name in self.mission_voters:

                            id = self.names_to_ids[name]
                            self.bot.send_message(id, committee_text, reply_markup=keyboard)

                        self.mission_voting_init()
                        # to mission voting

                    elif self.Game.reject_count == 5:

                        self.Game.continues = False
                        self.Game.win_side = "Evil"
                        
                        keyboard = self.remove_keyboard()
                        

                        for id in self.ids:
                            
                            text = "Evil Won.\n "\
                                "Reason: 5 consecitive rejection of the committee"
                            self.bot.send_message(id, text, reply_markup=keyboard)
                            self.bot.send_message(id, self.all_time_summary)

                        self.game_state = States.no_game
                        # to end of game (write the functions)
                        
                    else:
                        
                        
                        members_text = "The proposed committee was rejected"

                        for id in self.ids:

                            keyboard = self.remove_keyboard()
                            self.bot.send_message(id, members_text, reply_markup=keyboard)
                        
                        
                        n_committee = self.Game.all_round[self.Game.round]
                        commander_text = "It's your turn to choose your committee. "\
                                        f"In this round, you should pick {n_committee} player."

                        self.resolve_commander()
                        commander_id = self.names_to_ids[self.current_commander]

                        keyboard = self.commander_keyboard()
                        self.bot.send_message(commander_id, commander_text, reply_markup=keyboard)
                        self.committee_choosing_init()
                        # to committee_choosing(Done)
            else:

                text = emojize(":slightly_smiling_face:you have voted before")
                self.bot.send_message(message.chat.id, text)
                # to committee_voting(Done)

        ######################### mission out #########################
        @self.bot.message_handler(func=self.is_eligible_fail_success)
        def vote_for_mission(message):
            print("vote_for_mission")
            
            self.mission_voters.remove(self.ids_to_names[message.chat.id])

            if self.mission_voters:

                self.transfer_mission_vote(message)
                text = emojize(f"your vote has been received")
                self.bot.send_message(message.chat.id, text)
                # to mission_voting(Done)

            else:

                self.transfer_mission_vote(message)
                text = emojize(f"your vote has been received")
                self.bot.send_message(message.chat.id, text)

                self.Game.mission_result(self.mission_votes)

                if self.Game.evil_wins == 3:
                    
                    if keys.King in self.choosed_characters:

                        text = ("The evil team has won 3 rounds.\n"
                                "Now it is time for the king to guess all the member of the evil team."
                                f"The king in this game is: {self.ids_to_names[self.king_id]}")

                        for id in self.ids:

                            self.bot.send_message(id, text)
                        
                        king_message = ("who do you think was the member of evil team in this game ?")

                        keyboard = self.king_keyboard()
                        self.bot.send_message(self.king_id, king_message, reply_markup=keyboard) 

                        self.game_state = States.kings_guess
                        # to king_guess (write function)

                    else:

                        summary_text = "\n".join(self.all_time_summary)
                        for id in self.ids:
                            
                            text = "Evil won.\n"\
                                "Reason: they won three times"
                            self.bot.send_message(id, text)
                            self.bot.send_message(id, summary_text)

                        self.game_state = States.no_game
                        # to end of the game(write_functions)

                elif self.Game.city_wins == 3:

                    member_text = "City won 3 rounds, it is time for assassin to shoot"
                    keyboard = self.remove_keyboard()
                    
                    for id in self.ids:
                        self.bot.send_message(id, member_text, reply_markup=keyboard)

                    assassin_text = "who do you want to shoot?"
                    keyboard = self.assassin_keyboard()
                    self.bot.send_message(self.assassin_id, assassin_text, reply_markup=keyboard)

                    self.game_state = States.assassin_shoots
                    # to assassin shoots(write function)

                else:
                    

                    member_text = f"there was {self.Game.fail_count} fail vote(s), "\
                            f"and {self.Game.success_count} success vote(s)"\
                            f"Hence the {self.Game.who_won} won this round"
                    summary_text = "\n".join(self.all_time_summary)
                    keyboard = self.remove_keyboard()
                    for id in self.ids:

                        self.bot.send_message(id, member_text, reply_markup=keyboard)
                        self.bot.send_message(id, summary_text) 

                    n_committee = self.Game.all_round[self.Game.round]
                    commander_text = "It's your turn to choose your committee. "\
                                    f"In this round, you should pick {n_committee} player."
                    
                    self.resolve_commander()
                    commander_id = self.names_to_ids[self.current_commander]

                    keyboard = self.commander_keyboard()
                    self.bot.send_message(commander_id, commander_text, reply_markup=keyboard)
                    self.committee_choosing_init()
                    # to committee choose(Done)

        @self.bot.message_handler(func=self.is_king_choosing_names)
        def king_choosing_names(message):
            print("king_choosing_names")
            
            name = self.fix_name(message.text)

            
            if name in self.kings_guess:

                self.kings_guess.remove(name)
                text = f"{name} was removed from you guesses"

            else:

                self.kings_guess.append(name)
                text = f"{name} was added your guesses"
        
            keyboard = self.king_keyboard()
            self.bot.send_message(self.king_id, text, reply_markup=keyboard)
            # to king guesses(Done)

        @self.bot.message_handler(func=self.is_king_pressing_button)
        def king_pressing_button(message):
            print("king_pressing_button")

            if len(self.kings_guess) == len(self.Game.all_info["king"]):

                self.Game.king_guess(self.kings_guess)

                if self.Game.king_guessed_right:
                    
                    text = (f"Great job\n the king has guessed all {len(self.Game.all_info['king'])} players right.\n"
                             "Now it is time for the assassin to try and fine merlin")
                    
                    for id in self.ids:
                        self.bot.send_message(id, text)

                    assassin_text = f"Who do you think is the Merlin ?"
                    keyboard = self.assassin_keyboard()
                    self.bot.send_message(self.assassin_id, assassin_text, reply_markup=keyboard)

                    self.game_state = States.assassin_shoots
                    # to assassin shoots(write function)

                else:
                    pass


                    # if king guesses wrong
                    self.game_state = States.no_game
                    # to the end of the game

            else:

                text = f"you should guess exactly {len(self.Game.all_info['king'])} players"
                keyboard = self.king_keyboard()
                self.bot.send_message(self.king_id, text, reply_markup=keyboard)
                # to king guess(Done)
        
        @self.bot.message_handler(func=self.is_assassin_choosing_name)
        def assassin_choosing_name(message):
            print("assassin_choosing_name")
            
            name = self.fix_name(message.text)

            if name == self.assassins_guess:

                self.assassins_guess = str()

            else:

                self.assassins_guess = name

            keyboard = self.assassin_keyboard()
            text = emojize(f":thinking_face: You have chose {name} as Merlin, Hmmm ...")
            self.bot.send_message(self.assassin_id, text, reply_markup=keyboard)
            # to assassin shoots(Done)
        @self.bot.message_handler(func=self.is_assassin_pressing_button)
        def assassin_pressing_button(message):
            print("assassin_pressing_button")

            if self.assassins_guess == str():

                text = "You should choose someone !!!"
                keyboard = self.assassin_keyboard()
                self.bot.send_message(self.assassin_id, text, reply_markup=keyboard)
                # to assassin shoots(Done)
            else:

                self.game_state = States.no_game
                name = self.ids_to_names[message.chat.id]
                self.Game.assassin_shoot(name)
                keyboard = self.remove_keyboard()

                if self.Game.assassin_shooted_right:
                    
                    text = f"Congratulations. Assassins shooted {name} which was Merlin and the Evil won."
                    
                    for id in self.ids:
                        self.bot.send_message(id, text, reply_markup=keyboard)

                else:

                    text = f"Congratulations. Assassins shooted {name} which was not Merlin and the City won."

                    for id in self.ids:
                        self.bot.send_message(id, text, reply_markup=keyboard)
                # to the end of the game(Done) 

        ######################### Admin Request command #########################
        @self.bot.message_handler(commands=["adminrequest"])
        def admin_request(message):

            if not self.someone_requested and self.game_state==States.no_game:
                print("admin_request")
                self.someone_requested = True
                self.requested_name = self.ids_to_names[message.chat.id]
                request = f"{self.requested_name} requested to be an admin"

                self.temp_admin_id = message.chat.id
                keyboard = self.decline_accept_keyboard()
                self.bot.send_message(self.super_admin_id, request, reply_markup=keyboard)

                keyboard = self.remove_keyboard()
                message_to_user= "your request has been sent to the super admin."
                self.bot.send_message(message.chat.id, message_to_user, reply_markup=keyboard)

            elif self.someone_requested:
                print("admin_request")

                text = "you should wait, someone already requested"
                self.bot.send_message(message.chat.id, text)
        
        ######################### Accept Request #########################
        @self.bot.message_handler(func=self.is_super_admin)
        def accept_request(message):
            print("accept_request")
            
            keyboard = self.remove_keyboard()

            if message.text == keys.accept:

                self.admin_id = self.temp_admin_id
                answer = f"you are now an admin"
                self.bot.send_message(self.temp_admin_id, answer, reply_markup=keyboard)

                admin_answer = f"{self.requested_name} is now an admin"
                
                self.bot.send_message(self.super_admin_id, admin_answer, reply_markup=keyboard)

            elif message.text == keys.decline:
                
                self.admin_id = None
                answer = f"your request has been declined"
                self.bot.send_message(self.temp_admin_id, answer, reply_markup=keyboard)

                admin_answer = f"you have declined the request"

                self.bot.send_message(self.super_admin_id, admin_answer, reply_markup=keyboard)

            self.someone_requested = False

        ######################### Print Input #########################
        @self.bot.message_handler()
        def print_function(message):
            print("print_function")
            
            self.bot.send_message(message.chat.id, demojize(message.text))

    ######################### rule checkers #########################
    def is_super_admin(self, message):
        print("is_super_admin")

        c_1 = self.super_admin_id == message.chat.id

        return c_1

    def is_super_admin_accept_decline(self, message):
        print("is_super_admin_accept_decline")

        c_1 = self.is_super_admin(message)
        c_2 = message.text in [keys.accept, keys.decline]

        return c_1 and c_2

    def is_admin(self, message):
        print("is_admin")

        c_1 = self.is_super_admin(message)
        c_2 = self.admin_id == message.chat.id

        return c_1 or c_2
    
    def is_game_admin(self, message):
        print("is_game_admin")

        c_1 = self.game_admin_id == message.chat.id

        return c_1
    
    def is_commander(self, message):
        print("is_commander")

        c_1 = self.current_commander == self.ids_to_names[message.chat.id]

        return c_1

    def is_in_mission_voters(self, message):
        print("is_in_mission_voters")

        c_1 = self.ids_to_names[message.chat.id] in self.mission_voters

        return c_1

    def is_admin_choosing_character(self, message):
        print("is_admin_choosing_character")

        c_1 = self.gmae_state = States.ongoing
        c_2 = self.is_game_admin(message)
        c_4 = message.text in self.optional_characters
        c_3 = message.text in self.checked_optional_characters

        return c_1 and c_2 and (c_3 or c_4)

    def is_commander_choosing_name(self,message):
        print("is_commander_choosing_name")

        c_1 = self.game_state == States.committee_choose
        c_2 = self.is_commander(message)
        c_3 = message.text in self.names
        c_4 = message.text in self.checked_names
        print(c_1, c_2, c_3, c_4)
        return c_1 and c_2 and (c_3 or c_4)

    def is_commander_pressing_button(self, message):
        print("is_commander_pressing_button")

        c_1 = self.game_state == States.committee_choose
        c_2 = self.is_commander(message)
        c_3 = message.text in [keys.final, keys.propose]

        return c_1 and c_2 and c_3

    def is_eligible_vote(self, message):
        print("is_eligible_vote")

        name = self.ids_to_names[message.chat.id]
        c_1 = self.game_state == States.committee_voting
        c_2 = emojize(message.text) in [keys.agree, keys.disagree]
        c_3 = name in self.committee_voters

        return c_1 and c_2 and c_3

    def is_eligible_fail_success(self, message):
        print("is_eligible_fail_success")

        c_1 = self.is_in_mission_voters(message)
        c_2 = message.text in [keys.success, keys.fail]
        c_3 = self.game_state == States.mission_voting

        return c_1 and c_2 and c_3
    
    def is_king_choosing_names(self, message):
        print("is_king_choosing_names")

        c_1 = self.game_state == States.kings_guess
        c_2 = message.chat.id == self.king_id
        c_3 = message.text in [self.names_to_send_to_king]
        c_4 = message.text in [self.checked_names_to_send_to_king]

        return c_1 and c_2 and (c_3 or c_4)
    
    def is_king_pressing_button(self, message):
        print("is_king_pressing_button")

        c_1 = self.game_state == States.kings_guess
        c_2 = message.chat.id == self.king_id
        c_3 = message.text == keys.kings_guess

        return c_1 and c_2 and c_3
        
    def is_assassin_choosing_name(self, message):
        print("is_assassin_choosing_name")

        c_1 = self.game_state == States.assassin_shoots
        c_2 = message.chat.id == self.assassin_id
        c_3 = message.text in [self.names_to_send_to_assassin]
        c_4 = message.text in [self.checked_names_to_send_to_assassin]
        print(message.text)
        print(self.names_to_send_to_assassin)
        print(self.checked_names_to_send_to_assassin)
        print(c_1, c_2, c_3, c_4)

        return c_1 and c_2 and (c_3 or c_4)

    def is_assassin_pressing_button(self, message):
        print("is_assassin_pressing_button")

        c_1 = self.game_state == States.assassin_shoots
        c_2 = message.chat.id == self.assassin_id
        c_3 = message.text == keys.assassin_shoots
        print(c_1, c_2, c_3)

        return c_1 and c_2 and c_3

    ######################### keyboard makers #########################
    def decline_accept_keyboard(self):

        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons_str = [keys.accept, keys.decline]

        buttons = map(types.KeyboardButton, buttons_str)
        keyboard.add(*buttons)

        return keyboard

    def character_keyboard(self):

        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        buttons = []

        for character in self.optional_characters:

            if character in self.choosed_characters:
                
                temp_str = demojize(keys.check_box)

            else:

                temp_str = ""

            buttons.append(types.KeyboardButton(emojize(temp_str + character)))

        keyboard.add(*buttons)
        buttons_last_layers = [keys.finished_choosing]

        last_layer_buttons = map(types.KeyboardButton, buttons_last_layers)

        keyboard.add(*last_layer_buttons)

        return keyboard

    def commander_keyboard(self):
        
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        for name in self.names:

            if name in self.mission_voters:

                temp_str = demojize(keys.check_box)

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
    
    def king_keyboard(self):

        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        for name in self.names:

            if self.names_to_ids[name] == self.king_id:

                continue

            if name in self.kings_guess:

                temp_str = demojize(keys.check_box)

            else:

                temp_str = ""

            button = types.KeyboardButton(emojize(f"{temp_str}{name}"))
            keyboard.row(button)

        buttons_str = keys.kings_guess
        buttons = types.KeyboardButton(buttons_str)
        keyboard.row(buttons)

        return keyboard

    def assassin_keyboard(self):
        
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

        for name in self.names:

            if self.names_to_ids[name] in self.Evil_team_id:

                continue

            if name == self.assassins_guess:

                temp_str = demojize(keys.check_box)

            else:

                temp_str = ""

            button = types.KeyboardButton(emojize(f"{temp_str}{name}"))
            keyboard.row(button)

        buttons_str = keys.assassin_shoots
        buttons = types.KeyboardButton(buttons_str)
        keyboard.row(buttons)

        return keyboard

    def remove_keyboard(self):
        return types.ReplyKeyboardRemove()

    ######################### auxilary functions #########################
    def resolve_commander(self):
        
        self.current_commander = self.commander_order[0]
        self.commander_order.append(self.commander_order[0])
        del self.commander_order [0]

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

    def committee_choosing_init(self):

        self.game_state = States.committee_choose

    def committee_voting_init(self):

        self.game_state = States.committee_voting
        self.committee_voters = self.names[:]
        self.committee_votes = list()

    def mission_voting_init(self):

        self.mission_voters = list()
        self.mission_votes = list()
        self.game_state = States.mission_voting

        

    def add_committee_header(self, round, rejected_count):

        return (f"committee votes (round: {round}, rejected: {rejected_count}):" +
                "\n" + (f"-" * 10) + 
                "\n")
    
    def add_committee_vote(self, name, vote):
        
        return emojize(f"{name} voted: {vote}" + 
                       "\n")
    
    def add_mission_header(self, round):

        return ("\n" + f"mission_votes (round: {round}):" + 
                "\n" + ("-" * 10) + 
                "\n")
    
    def add_mission_vote(self, fail, success):

        return (f"{fail} fails and {success} success" + 
                "\n")
    
    def add_result(self, evil, city):
        
        return ("\n" + "Results:" +
                "\n" + ("-" * 10) +
                "\n" + f"# City Wins : {city}" +
                "\n" + f"# Evil Wins : {evil}" +
                "\n" + "-" * 30 +
                "\n" +
                "\n")


if __name__ == "__main__":

    my_bot = Bot()
