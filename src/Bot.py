from ctypes import c_int32, c_uint32
import os
from random import shuffle

import telebot
from emoji import demojize, emojize
from loguru import logger
from telebot import types
import time

from Constants import Sub_States, States, Keys, Texts
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
        self.mission_voters_name = list()
        self.mission_votes = list()
        
        # assassin parameters
        self.assassin_id = int()
        self.assassins_guess = str()

        # summary parameters
        self.committee_summary = str()
        self.mission_summary = str()
        self.all_time_summary = "Game Summary: \n"\
                                f"{'*' * 30}"

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
        def starting_word(message):#OKSTATE
            print("starting_word")
            id = message.chat.id

            if self.game_state == States.no_game:
                
                ##########################
                self.created_game_state(message)
                ##########################

                self.add_player(message)
                name = self.ids_to_names[id]
                keyboard = self.start_game_keyboard()
                self.bot.send_message(id, f"{Texts.CG}{name}.", reply_markup=keyboard)

            else:

                self.bot.send_message(id, Texts.GOG)
                ##########################
                #Return State
                ##########################

        ######################### Terminate Game #########################
        @self.bot.message_handler(regexp=self.terminating_word)
        def terminating_word(message):#OKSTATE
            print("terminate_game")

            id = message.chat.id

            if self.game_state == States.no_game:
                
                self.bot.send_message(id, Texts.NGET)

                ##########################
                #State Less
                ##########################

            else:

                keyboard = self.remove_keyboard()

                for id in self.ids:
                    self.bot.send_message(id, Texts.TGT, reply_markup=keyboard)

                ##########################
                self.ended_game_state()
                ##########################

        ######################### Search Command #########################
        @self.bot.message_handler(commands=["search"])
        def search_command(message):#OKSTATE
            print("search_command")

            id = message.chat.id
            if id not in self.ids:

                self.bot.send_message(id, text=Texts.SFG)
                time.sleep(1)

                if self.game_state == States.no_game:

                    self.bot.send_message(id, Texts.NGSC)
                    
                elif self.game_state == States.ongoing:
                    
                    self.bot.send_message(id, Texts.GOSC)

                elif self.game_state == States.starting:

                    keyboard = self.join_game_keyboard()
                    self.bot.send_message(id, Texts.GESC, reply_markup=keyboard)

            else:

                self.bot.send_message(id, Texts.YAJ)

            ##########################
            #State Less
            ##########################

        ######################### Join Game #########################
        @self.bot.message_handler(regexp=Keys.join_game)
        def join_game(message):#OKSTATE
            print("join_game")
            
            id = message.chat.id
            if id not in self.ids:

                self.add_player(message)
                name = self.ids_to_names[id]

                text = f"{Texts.YJGS}\n{Texts.YN}{name}."
                
                text_to_admin = f"{name} {Texts.GAJG}"
                keyboard = self.remove_keyboard()

                self.bot.send_message(id, text, reply_markup=keyboard)
                self.bot.send_message(self.game_admin_id, text_to_admin)

            else:

                self.bot.send_message(id, Texts.YAJ)
            
            ##########################
            #State Less
            ##########################

        ######################### Send Info #########################
        @self.bot.message_handler(func=self.is_game_admin, regexp=Keys.start_game)
        def send_info(message):#OKSTATE
            print("send_info")
            
            id = message.chat.id

            if self.game_state == States.starting:

                try:

                    self.define_game()

                    ##########################
                    self.started_game_state()
                    ##########################

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

                    text = emojize(f"{Texts.CO}\n" + self.order(self.commander_order))
                    keyboard = self.remove_keyboard()

                    for id in self.ids:

                        self.bot.send_message(id, text, reply_markup=keyboard)

                    self.resolve_commander()
                    commander_id = self.names_to_ids[self.current_commander]

                    n_committee = self.game.all_round[self.game.round]
                    commander_text = f"{Texts.CCN1}{Texts.CCN2_1}{n_committee}{Texts.CCN2_2}"

                    keyboard = self.commander_keyboard()
                    self.bot.send_message(commander_id, commander_text, reply_markup = keyboard)

                except ValueError as e:

                    self.bot.send_message(id, e.args[0])

            else:
                
                self.bot.send_message(id, Texts.TGHS)
                ##########################
                #Return State
                ##########################
                
        ######################### ccommander choosing name #########################
        @self.bot.message_handler(func=self.is_commander_choosing_name)
        def commander_choose_name(message):#OKSTATE
            print("commander_choose_name")
            id = message.chat.id
            add_remove_name = self.fix_name(message.text)

            if add_remove_name in self.mission_voters:

                self.mission_voters.remove(add_remove_name)
                text = f"{add_remove_name}{Texts.RFC}"

            else:

                self.mission_voters.append(add_remove_name)
                text = f"{add_remove_name}{Texts.ATC}"

            keyboard = self.commander_keyboard()
            self.bot.send_message(id, text, reply_markup=keyboard)

            ##########################
            #Return State
            ##########################

        ######################### commander pressing button #########################
        @self.bot.message_handler(func=self.is_commander_pressing_button)
        def commander_press_button(message):#OKSTATE
            print("commander_press_button")

            id = message.chat.id
            if self.game_sub_state == Sub_States.committee_choosing:

                self.game.check_committee(self.mission_voters)
                
                if self.game.acceptable_round:

                    if message.text == Keys.propose:

                        text = f"{Texts.propose}\n-" + "\n-".join(self.mission_voters)

                        for id in self.ids:

                            self.bot.send_message(id, text)

                    ##########################
                    #Return State
                    ##########################

                    elif message.text == Keys.final:

                        text = f"{Texts.final}\n-" + "\n-".join(self.mission_voters)
                        keyboard = self.committee_vote_keyboard()
                        self.committee_voters = self.names[:]

                        for id in self.ids:
                            self.bot.send_message(id, text, reply_markup=keyboard)

                        ##########################
                        self.committee_voting_state()
                        ##########################

                else:

                    n_committee = self.game.all_round[self.game.round]
                    text = f"{Texts.CCN2_1}{n_committee}{Texts.CCN2_2}"
                    keyboard = self.commander_keyboard()
                    id = message.chat.id
                    self.bot.send_message(id, text, reply_markup=keyboard)

                    ##########################
                    #Return State
                    ##########################

            else:

                self.bot.send_message(message.chat.id, Texts.YHFYD)

                ##########################
                #Return State
                ##########################

        ######################### committee vote #########################
        @self.bot.message_handler(func=self.is_eligible_vote)
        def vote_for_committee(message):
            print("vote_for_committee")

            name = self.ids_to_names[message.chat.id]

            if name in self.committee_voters:

                self.committee_voters.remove(name)

                if self.committee_voters:

                    self.transfer_committee_vote(message)

                    text = emojize(f"your vote: {message.text}")
                    keyboard = self.remove_keyboard()
                    self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

                    self.committee_summary += self.add_committee_vote(name, message.text)

                    ##########################
                    #Return State
                    ##########################

                else:
                    
                    self.transfer_committee_vote(message)

                    text = emojize(f"your vote: {message.text}")
                    keyboard = self.remove_keyboard()
                    self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

                    self.game.count_committee_vote(self.committee_votes)

                    if self.game.reject_count == 5:
                        
                        text = "The Evil won."
                        keyboard = self.remove_keyboard()

                        for id in self.ids:
                            
                            self.bot.send_message(id, text, reply_markup=keyboard)
                            self.bot.send_message(id, self.all_time_summary)

                        ##########################
                        self.ended_game_state()
                        ##########################

                    elif self.game.committee_accept:

                        rejected = self.game.reject_count
                        self.game.reject_count = 0

                        self.committee_summary += self.add_committee_vote(name, message.text)
                        self.committee_summary = self.add_committee_header(rejected) + self.committee_summary
                        self.committee_summary += self.add_committee_footer()
                        keyboard = self.remove_keyboard()

                        for id in self.ids:

                            self.bot.send_message(id, self.committee_summary, reply_markup=keyboard)
                        
                        committee_text  = "Choose between Fail and Success"

                        for name in self.mission_voters:

                            self.mission_voters_name.append(name)
                            keyboard = self.mission_keyboard()

                            id = self.names_to_ids[name]
                            self.bot.send_message(id, committee_text, reply_markup=keyboard)

                        ##########################
                        self.mission_voting_state()
                        ##########################
                        
                    else:
                        
                        self.game.reject_count += 1
                        rejected = self.game.reject_count

                        self.committee_summary += self.add_committee_vote(name, message.text)
                        self.committee_summary = self.add_committee_header(rejected) + self.committee_summary
                        self.committee_summary += self.add_committee_footer()
                        keyboard = self.remove_keyboard()

                        for id in self.ids:

                            self.bot.send_message(id, self.committee_summary, reply_markup=keyboard)
                        
                        self.resolve_commander()

                        commander_id = self.names_to_ids[self.current_commander]
                        text = f"the next commander is {self.current_commander}"

                        for id in self.ids:
                            self.bot.send_message(id, text)

                        n_committee = self.game.all_round[self.game.round]
                        commander_text = "It's your turn to choose your committee. "\
                                        f"In this round, you should pick {n_committee} player."
                        
                        ##########################
                        self.committee_choosing_state()
                        ##########################

                        keyboard = self.commander_keyboard()
                        self.bot.send_message(commander_id, commander_text, reply_markup=keyboard)

            else:

                text = emojize(":slightly_smiling_face: you have voted before")
                self.bot.send_message(message.chat.id, text)
                ##########################
                #Return State
                ##########################

        ######################### mission vote #########################
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
                    ##########################
                    #Return State
                    ##########################

                else:
                    
                    self.transfer_mission_vote(message)
                    text = emojize(f"your vote has been received")
                    keyboard = self.remove_keyboard()

                    self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
                    self.game.mission_result(self.mission_votes)
                    print("Stop1")

                    Round = self.game.round - 1
                    who_won = self.game.who_won
                    names = "\n-".join(self.mission_voters_name)
                    commander = self.current_commander

                    self.all_time_summary += self.add_mission_vote(names, self.game.fail_count,
                                                                   self.game.success_count,
                                                                   who_won, Round, commander)
                    print("Stop2")
                    if self.game.evil_wins == 3:
                        print("Stop3")
                        text = "Evil won."
                        keyboard = self.remove_keyboard()

                        for id in self.ids:
                            
                            self.bot.send_message(id, self.all_time_summary)
                            self.bot.send_message(id, text, reply_markup=keyboard)
                        
                        ##########################
                        self.ended_game_state()
                        ##########################


                    elif self.game.city_wins == 3:
                        print("Stop4")
                        text = "City won 3 rounds, it's time for assassin to shoot"
                        keyboard = self.remove_keyboard()

                        for id in self.ids:
                            
                            self.bot.send_message(id, self.all_time_summary)
                            self.bot.send_message(id, text, reply_markup=keyboard)

                        assassin_text = "who do you want to shoot?"
                        keyboard = self.assassin_keyboard()
                        self.bot.send_message(self.assassin_id, assassin_text, reply_markup=keyboard)

                        ##########################
                        self.assassin_shooting_state()
                        ##########################

                    else:
                        print("Stop5")
                        keyboard = self.remove_keyboard()
                        self.resolve_commander()

                        commander_id = self.names_to_ids[self.current_commander]
                        text = f"the next commander is {self.current_commander}"

                        n_committee = self.game.all_round[self.game.round]
                        commander_text = "It's your turn to choose your committee. "\
                                        f"In this round, you should pick {n_committee} player."
                        print("Stop6")
                        for id in self.ids:

                            self.bot.send_message(id, self.all_time_summary, reply_markup=keyboard) 
                            self.bot.send_message(id, text)
                        print("Stop7")
                        ##########################
                        self.committee_choosing_state()
                        ##########################

                        keyboard = self.commander_keyboard()
                        self.bot.send_message(commander_id, commander_text, reply_markup=keyboard)

            else:

                text = emojize(f"your vote has been received")
                keyboard = self.remove_keyboard()
                self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
                ##########################
                #Return State
                ##########################

        @self.bot.message_handler(func=self.is_assassin_choosing_name)
        def assassin_choosing_name(message):#STATEOK
            print("assassin_choosing_name")
            
            self.assassins_guess = self.fix_name(message.text)

            keyboard = self.assassin_keyboard()
            text = emojize(f"You chose {self.assassins_guess} as Merlin.")
            self.bot.send_message(self.assassin_id, text, reply_markup=keyboard)

            ##########################
            #State Less
            ##########################

        @self.bot.message_handler(func=self.is_assassin_pressing_button)
        def assassin_pressing_button(message):#STATEOK
            print("assassin_pressing_button")

            if self.assassins_guess == str():

                text = "You should choose someone !!!"
                keyboard = self.assassin_keyboard()
                self.bot.send_message(self.assassin_id, text, reply_markup=keyboard)

                ##########################
                #Return State
                ##########################

            else:

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

                ##########################
                self.ended_game_state()
                ##########################

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

            print("private")

            if((message.chat.first_name != None) and (message.chat.last_name != None)):
                name = message.chat.first_name + " " + message.chat.last_name

            elif not (message.chat.last_name):
                name = message.chat.first_name

            elif not (message.chat.first_name):
                name = message.chat.last_name

            return name
        
        elif message.chat.type == "group" or message.chat.type =="supergroup":
            print("group")
            
            if((message.from_user.first_name != None) and (message.from_user.last_name != None)):
                name = message.from_user.first_name + " " + message.from_user.last_name

            elif not (message.from_user.last_name):
                name = message.from_user.first_name

            elif not (message.from_user.first_name):
                name = message.from_user.last_name

            name = name + " @ " + message.chat.title

            return name
    def order(self, commander_order):

        commander_order_show = str()

        for i , name in enumerate(commander_order):

            commander_order_show += f"{i +1 }-" +  f"{name}\n"

        return commander_order_show
    
    def fix_name(self, currupted_name):

        '''
        This function return the uncheked version of a checked name.
        if the names is unchecked already, it returns the names itself.
        '''

        if currupted_name[0:len(Keys.check_box)] == Keys.check_box:

            return currupted_name[len(Keys.check_box):]

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

        self.checked_names.append(emojize(f"{Keys.check_box}{name}"))

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

        if message.text == Keys.agree:
            self.committee_votes.append(1)

        elif message.text == Keys.disagree:
            self.committee_votes.append(0)

    def transfer_mission_vote(self, message):

        if message.text == Keys.success:
            self.mission_votes.append(1)

        elif message.text == Keys.fail:
            self.mission_votes.append(0)

    ######################### State functions #########################
    def created_game_state(self, message):

        self.game_state = States.starting
        self.game_admin_id = message.chat.id

    def started_game_state(self):

        self.game_state = States.ongoing
        self.committee_choosing_state()

    def committee_choosing_state(self):

        self.game_sub_state = Sub_States.committee_choosing
        self.mission_voters = list()
        self.mission_voters_name = list()

    def committee_voting_state(self):
        
        self.game_state = States.ongoing
        self.game_sub_state = Sub_States.committee_voting
        self.committee_voters = self.names[:]

        self.committee_votes = list()
        self.committee_summary = str()

    def mission_voting_state(self):

        self.game_state = States.ongoing
        self.game_sub_state = Sub_States.mission_voting
        self.mission_votes = list()

    def assassin_shooting_state(self):

        self.game_state = States.ongoing
        self.game_sub_state = Sub_States.assassin_shooting
        
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

        c_1 = self.game_state == States.ongoing 
        c_2  = self.game_sub_state == Sub_States.committee_choosing
        c_3 = self.is_commander(message)
        c_4 = message.text in self.names
        c_5 = message.text in self.checked_names

        return c_1 and c_2 and c_3 and(c_4 or c_5)

    def is_commander_pressing_button(self, message):
        print("is_commander_pressing_button")

        c_1 = self.game_state == States.ongoing 
        c_2  = self.game_sub_state == Sub_States.committee_choosing
        c_3 = self.is_commander(message)
        c_4 = message.text in [Keys.final, Keys.propose]

        return c_1 and c_2 and c_3 and c_4

    def is_eligible_vote(self, message):
        print("is_eligible_vote")

        c_1 = self.game_state == States.ongoing 
        c_2  = self.game_sub_state == Sub_States.committee_voting
        c_3 = emojize(message.text) in [Keys.agree, Keys.disagree]

        return c_1 and c_2 and c_3

    def is_eligible_fail_success(self, message):
        print("is_eligible_fail_success")

        c_1 = self.game_state == States.ongoing 
        c_2  = self.game_sub_state == Sub_States.mission_voting
        c_3 = message.text in [Keys.success, Keys.fail]

        return c_1 and c_2 and c_3
        
    def is_assassin_choosing_name(self, message):
        print("is_assassin_choosing_name")

        c_1 = self.game_state == States.ongoing 
        c_2  = self.game_sub_state == Sub_States.assassin_shooting
        c_4 = message.chat.id == self.assassin_id
        c_3 = message.text != Keys.assassin_shoots

        return c_1 and c_2 and c_3 and c_4

    def is_assassin_pressing_button(self, message):
        print("is_assassin_pressing_button")

        c_1 = self.game_state == States.ongoing 
        c_2  = self.game_sub_state == Sub_States.assassin_shooting
        c_3 = message.chat.id == self.assassin_id
        c_4 = message.text == Keys.assassin_shoots

        return c_1 and c_2 and c_3 and c_4

    ######################### keyboard makers #########################
    # the following functions make keyboard for players.
    def start_game_keyboard(self):

        buttons_text= [Keys.start_game]
        buttons = map(types.KeyboardButton, buttons_text)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(*buttons)

        return keyboard
    
    def join_game_keyboard(self):

        buttons_text= [Keys.join_game]
        buttons = map(types.KeyboardButton, buttons_text)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)

        return keyboard
    
    def commander_keyboard(self):
        
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

        for name in self.names:

            if name in self.mission_voters:

                temp_str = demojize(Keys.check_box)

            else:

                temp_str = ""

            button = types.KeyboardButton(emojize(f"{temp_str}{name}"))
            keyboard.row(button)

        buttons_str = [Keys.propose, Keys.final]
        buttons = map(types.KeyboardButton, buttons_str)
        keyboard.row(*buttons)

        return keyboard

    def committee_vote_keyboard(self):

        buttons_str = [Keys.agree, Keys.disagree]
        buttons = map(types.KeyboardButton, buttons_str)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        keyboard.add(*buttons)
        return keyboard

    def mission_keyboard(self):

        buttons_str = [Keys.success, Keys.fail]
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

                temp_str = demojize(Keys.check_box)

            else:

                temp_str = ""

            button = types.KeyboardButton(emojize(f"{temp_str}{name}"))
            keyboard.row(button)

        buttons_str = Keys.assassin_shoots
        buttons = types.KeyboardButton(emojize(buttons_str))
        keyboard.row(buttons)

        return keyboard

    def remove_keyboard(self):
        return types.ReplyKeyboardRemove()

    ######################### Summary Functions #########################
    # the following function are to make summary during the fellow of the game.

    def add_committee_header(self, rejected_count):
        sep = "-" * 15
        return ("\n" + f"Rejection Count: {rejected_count}" +
                "\n" + sep +
                "\n" + f"Committee Votes:" +
                "\n")
    
    def add_committee_vote(self, name, vote):
        
        return emojize(f"-{name} voted: {vote}" + 
                       "\n")

    def add_committee_footer(self):

        sign = Keys.accept if self.game.committee_accept else Keys.declined
        sep = "-" * 15

        return (sep +
                "\n" + "Committee Result:"
                "\n" + sign)

    def add_mission_vote(self, names, fail, success, who_won, Round, commander):

        sign = ":red_square:" if who_won == "Evil" else ":green_square:"
        sep = "-" * 15
        round_sep = "*" * 30

        return ("\n" +
                "\n" + f"Round: {Round} (Commander: {commander})" +
                "\n" + f"{sep}" +
                "\n" + f"Committee Memebers:"+
                "\n" + "-" + names +
                "\n" + f"{sep}" +
                "\n" + f"Mission Results:"+
                "\n" + f"# Sucesses: {success}" +
                "\n" + f"# Fails: {fail}" +
                "\n" + f"{sep}" +
                "\n" + f"Round Winner:" +
                "\n" + emojize(f"{sign} {who_won}") +
                "\n" +
                "\n" + f"{round_sep}")
    
if __name__ == "__main__":

    my_bot = Bot()
