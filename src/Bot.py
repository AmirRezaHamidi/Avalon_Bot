from ctypes import c_int32, c_uint32
import os
from random import shuffle

import telebot
from emoji import demojize, emojize
from loguru import logger
from telebot import types
import time

from Constants import Sub_States, States, keys
from Engines import Avalon_Engine
from utils.io import read_txt_file

current_working_directory = os.getcwd()
TOKEN = read_txt_file(f"{current_working_directory}\\src\\Data\\Bot_Token.txt")
starting_word = read_txt_file(f"{current_working_directory}\\src\\Data\\Starting_Word.txt")
terminating_word = read_txt_file(f"{current_working_directory}\\src\\Data\\Terminating_Word.txt")

class Bot():

    def initial_condition(self): #STATELESS
        
        # admin parameters
        self.starting_word = starting_word
        self.terminating_word = terminating_word
        self.game_admin_id = int()

        # game state parameter
        self.game_state = States.no_game
        self.game_sub_state = None

        # players parameters
        self.names = list()
        self.checked_names = list()
        self.ids = list()

        self.ids_to_names = dict()
        self.names_to_ids = dict()
        
        # Character parameters
        self.choosed_characters = ["Merlin", "Assassin"]
        self.Evil_team_id = list()

        # commander parameters
        self.commander_order = list()
        self.current_commander = str()
        self.shuffle_commander_order = True

        # committee parameters
        self.committee_voters = list()
        self.committee_votes = list()

        # mission parameters
        self.mission_voters = list()
        self.mission_votes = list()
        
        # assassin parameters
        self.assassin_id = int()
        self.assassins_guess = str()

        # summary parameters
        self.committee_summary = str()
        self.mission_summary = str()
        self.all_time_summary = f"{'*' * 30}"

    def __init__(self): #STATELESS

        # Initializing the bot
        self.initial_condition()
        self.bot = telebot.TeleBot(TOKEN)

        # defining bot handlders
        logger.info("Defining the handlers ...")
        self.handlers()

        # Start polling
        logger.info("Starting the bots ...")
        self.bot.infinity_polling()
    
    def handlers(self):

        ######################### Starting Word #########################
        @self.bot.message_handler(regexp=self.starting_word)
        def starting_word(message): #OKSTATE
            print("starting_word")
            
            if self.game_state == States.no_game:
                
                self.created_game_state()

                self.add_player(message)
                self.game_admin_id = message.chat.id

                name = name = self.ids_to_names[message.chat.id]
                Created_game_message ="The game was created, ask your friends to join the game"
                joining_game_message = f"Your name in the game: {name}.\n\n"

                buttons_text= [keys.start_game]
                buttons = map(types.KeyboardButton, buttons_text)
                keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
                keyboard.add(*buttons)

                self.bot.send_message(message.chat.id, text=Created_game_message)
                self.bot.send_message(message.chat.id, text = joining_game_message, reply_markup=keyboard)

            else:

                text =("A game is ongoing. Find it using search command")
                self.bot.send_message(message.chat.id, text=text)

        ######################### Terminate Game #########################
        @self.bot.message_handler(regexp=self.terminating_word)
        def terminating_word(message): #OKSTATE
            print("terminate_game")

            text = "The game has been terminated"
            keyboard = self.remove_keyboard()

            for id in self.ids:
                self.bot.send_message(id, text, reply_markup=keyboard)

            self.ended_game_state()
        ######################### Search Command #########################
        @self.bot.message_handler(commands=["search"])
        def search_command(message):#OKSTATE
            print("search_command")

            if message.chat.id not in self.ids:

                self.bot.send_message(message.chat.id, text="Searching ... ")
                time.sleep(1)

                if self.game_state == States.no_game:

                    text ="No game exist. try again ..."
                    self.bot.send_message(message.chat.id, text=text)
                    
                elif self.game_state == States.ongoing:
                    
                    text ="A game is ongoing. try again later ..."
                    self.bot.send_message(message.chat.id, text=text)

                elif self.game_state == States.starting:

                    text ="A game already exist and you can join it."
                    buttons_text= [keys.join_game]
                    buttons = map(types.KeyboardButton, buttons_text)
                    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                    keyboard.add(*buttons)

                    self.bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

            else:

                text = "you have already joined the game"
                self.bot.send_message(message.chat.id, text=text)

        ######################### Join Game #########################
        @self.bot.message_handler(regexp=keys.join_game)
        def join_game(message):#STATEOK
            print("join_game")
            
            if message.chat.id not in self.ids:

                self.add_player(message)
                name = self.ids_to_names[message.chat.id]

                text = f"You have join the game sucessfuly \n"\
                        f"your name in the game: {name}."
                
                text_to_admin = f"{name} has joined the game"
                keyboard = self.remove_keyboard()

                self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
                self.bot.send_message(self.game_admin_id, text_to_admin)

            else:

                text = "you have already joined the game"
                self.bot.send_message(message.chat.id, text=text)

        ######################### Send Info #########################
        @self.bot.message_handler(func=self.is_game_admin, regexp=keys.start_game)
        def send_info(message):#STATECHANGE
            print("send_info")
            
            if self.game_state == States.starting:

                self.game_state = States.ongoing
                self.define_game()
                self.committee_choosing_state()

                for name, character in self.game.assigned_character.items():

                    message = character.message
                    self.bot.send_message(self.names_to_ids[name], message)

                    if character.name == "Assassin":
                        self.assassin_id = self.names_to_ids[name]
                        
                    if character.has_info:
                        
                        c_1 = character.name == "Minion"
                        c_2 = character.name == "Assassin"

                        if c_1 or c_2:

                            info = "\n".join(self.game.all_info["Evil_Team"])
                            self.bot.send_message(self.names_to_ids[name], info)
                            self.Evil_team_id.append(self.names_to_ids[name])

                        else:
                            
                            info = "\n".join(self.game.all_info[character.name])
                            self.bot.send_message(self.names_to_ids[name], info)


                self.commander_order = self.names[:]
                if self.shuffle_commander_order:

                    shuffle(self.commander_order)
            
                commander_order_message_1 = "Here is the order of the commanders.\n"
                commander_order_message_2 = "\n:downwards_button:\n".join(self.commander_order)

                text = emojize(commander_order_message_1 + commander_order_message_2)
                keyboard = self.remove_keyboard()

                for id in self.ids:

                    self.bot.send_message(id, text, reply_markup=keyboard)

                self.resolve_commander()
                commander_id = self.names_to_ids[self.current_commander]

                n_committee = self.game.all_round[self.game.round]
                commander_text = "It's your turn to choose your committee.\n"\
                                f" In this round, you should pick {n_committee} player."

                keyboard = self.commander_keyboard()
                self.bot.send_message(commander_id, commander_text, reply_markup = keyboard)

            else:
                
                text =("The game has already started.")
                self.bot.send_message(message.chat.id, text=text)

            # to committee chosing
                
        ######################### ccommander choosing name #########################
        @self.bot.message_handler(func=self.is_commander_choosing_name)
        def commander_choose_name(message):#STATEOK
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
        def commander_press_button(message):#STATECHANGE
            print("commander_press_button")

            self.game.check_committee(self.mission_voters)
            
            if self.game.acceptable_round:

                if message.text == keys.propose:

                    text = f"{keys.propose}:\n"
                    committee_member_text = "\n".join(self.mission_voters)
                    whole_text = text + committee_member_text
                    keyboard = self.remove_keyboard()

                    for id in self.ids:

                        self.bot.send_message(id, whole_text)
                    # to committee choosing (Done)

                elif message.text == keys.final: #STATE_CHANGE

                    text = f"{keys.final}:\n"
                    committee_member_text = "\n".join(self.mission_voters)

                    whole_text = text + committee_member_text
                    keyboard = self.committee_vote_keyboard()
                    self.committee_voters = self.names[:]

                    for id in self.ids:
                        self.bot.send_message(id, whole_text, reply_markup=keyboard)

                    self.committee_voting_state()
                    # to committee voting (Done)

            else:

                n_committee = self.game.all_round[self.game.round]
                text = "The number of players in the "\
                        f"committee should be {n_committee}"
                
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

                    self.transfer_committee_vote(message)

                    keyboard = self.remove_keyboard()
                    text = emojize(f"your vote: {message.text}")
                    self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

                    self.committee_summary += self.add_committee_vote(name, message.text)
                    # to committee voting (Done)

                else:
                    
                    # the last person to vote.
                    self.transfer_committee_vote(message)

                    text = emojize(f"your vote: {message.text}")
                    keyboard = self.remove_keyboard()
                    self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

                    self.game.count_committee_vote(self.committee_votes)

                    round = self.game.round
                    rejected = self.game.reject_count

                    self.committee_summary += self.add_committee_vote(name, message.text)
                    self.committee_summary = self.add_committee_header(round, rejected) + self.committee_summary
                    self.all_time_summary += self.committee_summary

                    for id in self.ids:

                        self.bot.send_message(id, self.committee_summary)

                    if self.game.committee_accept:

                        self.mission_votes = list()

                        self.game_state = Sub_States.mission_voting
                        members_text = "the proposed committee was accepted"
                        committee_text  ="Choose between Fail and Success"

                        for id in self.ids:

                            self.bot.send_message(id, members_text)

                        for name in self.mission_voters:

                            keyboard = self.mission_keyboard()
                            id = self.names_to_ids[name]
                            self.bot.send_message(id, committee_text, reply_markup=keyboard)

                        self.mission_voting_state()
                        # to mission voting

                    elif self.game.reject_count == 5:
                        
                        keyboard = self.remove_keyboard()
                        
                        for id in self.ids:
                            
                            text = "Evil Won."
                            
                            self.bot.send_message(id, text, reply_markup=keyboard)
                            self.bot.send_message(id, self.all_time_summary)

                        self.game_state = States.no_game
                        # to end of game (write the functions)
                        
                    else:
                        
                        members_text = "The proposed committee was rejected"

                        for id in self.ids:

                            keyboard = self.remove_keyboard()
                            self.bot.send_message(id, members_text, reply_markup=keyboard)
                        
                        n_committee = self.game.all_round[self.game.round]
                        commander_text = "It's your turn to choose your committee. "\
                                        f"In this round, you should pick {n_committee} player."

                        self.resolve_commander()
                        commander_id = self.names_to_ids[self.current_commander]

                        self.committee_choosing_state()

                        keyboard = self.commander_keyboard()
                        self.bot.send_message(commander_id, commander_text, reply_markup=keyboard)

                        # to committee_choosing(Done)

            else:

                text = emojize(":slightly_smiling_face: you have voted before")
                self.bot.send_message(message.chat.id, text)
                # to committee_voting(Done)

        ######################### mission out #########################
        @self.bot.message_handler(func=self.is_eligible_fail_success)
        def vote_for_mission(message):
            print("vote_for_mission")
            
            name = self.ids_to_names[message.chat.id]

            if name in self.mission_voters:

                self.mission_voters.remove(name)

                if self.mission_voters:

                    self.transfer_mission_vote(message)
                    text = emojize(f"your vote has been received")
                    keyboard = self.remove_keyboard()
                    self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
                    # to mission_voting(Done)

                else:
                    
                    # last person vote
                    self.transfer_mission_vote(message)
                    text = emojize(f"your vote has been received")
                    keyboard = self.remove_keyboard()
                    self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

                    self.game.mission_result(self.mission_votes)

                    self.all_time_summary += self.add_mission_vote(self.game.fail_count,
                                                                        self.game.success_count,
                                                                        self.game.city_wins,
                                                                        self.game.evil_wins)
                    
                    if self.game.evil_wins == 3:
                        
                        text = "Evil won."
                        keyboard = self.remove_keyboard()

                        for id in self.ids:
                            
                            self.bot.send_message(id, self.all_time_summary)
                            self.bot.send_message(id, text, reply_markup=keyboard)

                        self.game_state = States.no_game
                        # to end of the game(write_functions)

                    elif self.game.city_wins == 3:

                        text = "City won 3 rounds, it's time for assassin to shoot"
                        keyboard = self.remove_keyboard()

                        for id in self.ids:
                            
                            self.bot.send_message(id, self.all_time_summary)
                            self.bot.send_message(id, text, reply_markup=keyboard)

                        assassin_text = "who do you want to shoot?"
                        keyboard = self.assassin_keyboard()
                        self.bot.send_message(self.assassin_id, assassin_text, reply_markup=keyboard)

                        self.game_state = Sub_States.assassin_shooting
                        # to assassin shoots(write function)

                    else:
                        
                        keyboard = self.remove_keyboard()
                        self.resolve_commander()

                        commander_id = self.names_to_ids[self.current_commander]
                        text = f"the next commander is {self.current_commander}"

                        n_committee = self.game.all_round[self.game.round]
                        commander_text = "It's your turn to choose your committee. "\
                                        f"In this round, you should pick {n_committee} player."
                        
                        for id in self.ids:

                            self.bot.send_message(id, self.all_time_summary, reply_markup=keyboard) 
                            self.bot.send_message(id, text)
                        
                        self.committee_choosing_state()

                        keyboard = self.commander_keyboard()
                        self.bot.send_message(commander_id, commander_text, reply_markup=keyboard)
                        
                        # to committee choose(Done)
            else:

                text = emojize(f"your vote has been received")
                keyboard = self.remove_keyboard()
                self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

        @self.bot.message_handler(func=self.is_assassin_choosing_name)
        def assassin_choosing_name(message):#STATEOK
            print("assassin_choosing_name")
            
            self.assassins_guess = self.fix_name(message.text)

            keyboard = self.assassin_keyboard()
            text = emojize(f"You chose {self.assassins_guess} as Merlin.")
            self.bot.send_message(self.assassin_id, text, reply_markup=keyboard)
            # to assassin shoots(Done)

        @self.bot.message_handler(func=self.is_assassin_pressing_button)
        def assassin_pressing_button(message):#STATEOK
            print("assassin_pressing_button")

            if self.game_substate == Sub_States.assassin_shooting:

                if self.assassins_guess == str():

                    text = "You should choose someone !!!"
                    keyboard = self.assassin_keyboard()
                    self.bot.send_message(self.assassin_id, text, reply_markup=keyboard)
                    # to assassin shoots(Done)

                else:

                    self.assassin_shooted_state()
                    self.game.assassin_shoot(self.assassins_guess)
                    keyboard = self.remove_keyboard()

                    if self.game.assassin_shooted_right:
                        
                        text = f"Assassins shooted {self.assassins_guess} which was the Merlin.\n"\
                                "The Evil won."

                    else:

                        text = f"Assassins shooted {self.assassins_guess} which was not the Merlin.\n"\
                                "The City won."

                    for id in self.ids:

                        self.bot.send_message(id, text, reply_markup=keyboard)

            elif self.game_sub_state == Sub_States.assassin_shooted:

                text = "Your have already shooted."
                self.bot.send_message(message.chat.id, text)
                # to the end of the game(Done)
                self.ended_game_state()

            else:

                text = 'debug in assassin section'
                self.bot.send_message(message.chat.id, text)


        ######################### Print Input #########################
        @self.bot.message_handler()
        def print_function(message):
            print("print_function")
            
            self.bot.send_message(message.chat.id, demojize(message.text))

    ######################### main functions #########################
    # These are the main function of this class.
    def grab_name(self, message):

        '''
        this function extract the names from the message of the players.
        '''
        name = str()

        if message.chat.type == "private":

            if((message.chat.first_name != None) and (message.chat.last_name != None)):
                name = message.chat.first_name + " " + message.chat.last_name

            elif not (message.chat.last_name):
                name = message.chat.first_name

            elif not (message.chat.first_name):
                name = message.chat.last_name

            return name
        
        elif message.chat.type == "group":

            if((message.from_user.first_name != None) and (message.from_user.last_name != None)):
                name = message.from_user.first_name + " " + message.from_user.last_name

            elif not (message.from_user.last_name):
                name = message.from_user.first_name

            elif not (message.from_user.first_name):
                name = message.from_user.last_name

            name = name + " @ " + message.chat.title

            return name
        
    def fix_name(self, currupted_name):

        '''
        This function return the uncheked version of a checked name.
        if the names is unchecked already, it returns the names itself.
        '''

        if currupted_name[0:len(keys.check_box)] == keys.check_box:

            return currupted_name[len(keys.check_box):]

        else:

            return currupted_name
    
    def add_player(self, message):

        '''
        this function add the players info name to the game 
        when pressing join game or create game by the players.
        '''

        name = self.grab_name(message)
        temp_name = name

        id = message.chat.id
        similar_name_count = 0

        while True:

            if temp_name in self.names:

                similar_name_count += 1
                temp_name = f"{name}_{similar_name_count}"

            else:
                
                name = temp_name
                break
        
        self.names.append(name)
        self.ids.append(id)

        self.checked_names.append(emojize(f"{keys.check_box}{name}"))

        self.names_to_ids[name] = id
        self.ids_to_names[id] = name

    def define_game(self):

        '''
        this function define the define the game engine using
        the names of the players and the prefered characters.
        '''
        
        name_for_game = self.names[:]
        character_for_game = self.choosed_characters[:]
        self.game = Avalon_Engine(name_for_game, character_for_game)

    ######################### auxilary functions #########################
    # the following functions helps the game be functinality.
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

    ######################### State functions #########################
    def created_game_state(self):

        self.game_state = States.starting

    def started_game_state(self):

        self.game_state = States.ongoing

    def committee_choosing_state(self):

        self.game_state = States.ongoing
        self.game_state = Sub_States.committee_choose
        self.mission_voters = list()
        
    def committee_chosed_state(self):
        pass

    def committee_voting_state(self):

        self.game_state = States.ongoing
        self.game_state = Sub_States.committee_voting
        self.committee_voters = self.names[:]

        self.committee_votes = list()
        self.committee_summary = str()

    def committee_voted_state(self):
        pass

    def mission_voting_state(self):

        self.game_state = States.ongoing
        self.game_state = Sub_States.mission_voting
        self.mission_votes = list()

    def mission_voted_state(self):
        pass

    def assassin_shooting_state(self):

        self.game_state = States.ongoing
        self.game_substate = Sub_States.assassin_shooting

    def assassin_shooted_state(self):

        self.game_state = States.ongoing
        self.game_substate= Sub_States.assassin_shooted
        
    def ended_game_state(self):

        self.initial_condition()

    ######################### rule checkers #########################
    # the following functions check the necessary rules
    # for each message handler. their output is either True or False.
    
    def is_game_admin(self, message):
        print("is_game_admin")

        c_1 = self.game_admin_id == message.chat.id

        return c_1
    
    def is_commander(self, message):
        print("is_commander")

        c_1 = self.current_commander == self.ids_to_names.get(message.chat.id, 'None')
        
        return c_1

    def is_commander_choosing_name(self,message):
        print("is_commander_choosing_name")

        c_1 = self.is_commander(message)
        c_2 = message.text in self.names
        c_3 = message.text in self.checked_names
        c_4 = self.game_state == Sub_States.committee_choose

        return c_1 and c_2 and (c_3 or c_4)

    def is_commander_pressing_button(self, message):
        print("is_commander_pressing_button")

        c_1 = self.is_commander(message)
        c_2 = message.text in [keys.final, keys.propose]
        c_3 = self.game_state == Sub_States.committee_choose

        return c_1 and c_2 and c_3

    def is_eligible_vote(self, message):
        print("is_eligible_vote")

        c_1 = emojize(message.text) in [keys.agree, keys.disagree]
        c_2 = self.game_state == Sub_States.committee_voting

        return c_1 and c_2

    def is_eligible_fail_success(self, message):
        print("is_eligible_fail_success")

        c_1 = message.text in [keys.success, keys.fail]
        c_2 = self.game_state == Sub_States.mission_voting

        return c_1 and c_2
        
    def is_assassin_choosing_name(self, message):
        print("is_assassin_choosing_name")

        c_1 = self.game_state == Sub_States.assassin_shooting
        c_2 = message.chat.id == self.assassin_id
        c_3 = message.text != keys.assassin_shoots

        return c_1 and c_2 and c_3

    def is_assassin_pressing_button(self, message):
        print("is_assassin_pressing_button")

        c_1 = self.game_state == Sub_States.assassin_shooting
        c_2 = message.chat.id == self.assassin_id
        c_3 = message.text == keys.assassin_shoots
        print(c_1, c_2, c_3)

        return c_1 and c_2 and c_3

    ######################### keyboard makers #########################
    # the following functions make keyboard for players.

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
        shuffle(buttons_str)
        buttons = map(types.KeyboardButton, buttons_str)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(*buttons)
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
        buttons = types.KeyboardButton(emojize(buttons_str))
        keyboard.row(buttons)

        return keyboard

    def remove_keyboard(self):
        return types.ReplyKeyboardRemove()

    ######################### Summary Functions #########################
    # the following function are to make summary during
    # the fellow of the game.

    def add_committee_header(self, round, rejected_count):
        
        return ("\n" + f"# Round: {round}, # Rejection: {rejected_count}" +
                "\n" + f"{'=' * 10}" +
                "\n" + f"-Committee Votes:" +
                "\n")
    
    def add_committee_vote(self, name, vote):
        
        return emojize(f"{name} voted: {vote}" + 
                       "\n")
    
    def add_mission_vote(self, fail, success, city, evil):

        return ("-" * 10 + "\n" + f"-Mission Votes:"+
                "\n" + f"# Sucesses: {success}" +
                "\n" + f"# Fails: {fail}" +
                "\n" + "-" * 10 +
                "\n" + "-Results:" +
                "\n" + f"# City Wins : {city}" +
                "\n" + f"# Evil Wins : {evil}" +
                "\n" +
                "\n" + "*" * 30)

if __name__ == "__main__":

    my_bot = Bot()
