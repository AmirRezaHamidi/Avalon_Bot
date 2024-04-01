from random import shuffle

import telebot
from emoji import demojize, emojize
from loguru import logger
from telebot import types

from Constants import Directories, \
    Keys, Sub_States, States, \
    GaS_T, Char_T, Ass_T, GaSi_T, Co_T, Vote_T, Oth_T
from Engines import Avalon_Engine
from utils.io import read_txt_file  # write_json_file

TOKEN = read_txt_file(Directories.Token)
creating_game_word = read_txt_file(Directories.CGW)
terminating_game_word = read_txt_file(Directories.TGW)


class Bot():

    def initial_condition(self):

        # admin parameters
        self.creating_game_word = creating_game_word
        self.terminating_game_word = terminating_game_word
        self.admin_id = int()

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
        # characters
        merlin = Char_T.merlin
        assassin = Char_T.assassin
        mordred = Char_T.mordred
        obron = Char_T.oberon
        persival = Char_T.persival_morgana
        # lady = Char_T.lady

        key = Keys.check_box
        self.choosed_characters = [merlin, assassin]
        optional = [obron, mordred, persival]
        self.optional_characters = optional
        self.checked_optional_characters = [f"{key}{i}" for i in optional]

        # commander parameters
        self.commander_order = list()
        self.current_commander = str()
        self.current_commander_id = int()
        self.shuffle_commander_order = True
        self.commander_number = 0

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
        self.game_summary = str()

    def __init__(self):

        # Initializing the bot ...
        self.initial_condition()
        self.bot = telebot.TeleBot(TOKEN)

        # defining bot handlders ...
        logger.info("Defining the handlers ...")
        self.handlers()

        # Start polling ...
        logger.info("Start Polling ...")
        self.bot.infinity_polling()

    def handlers(self):

        # Create game #
        @self.bot.message_handler(regexp=self.creating_game_word)
        def creating_game_word(message):
            print("creating_game_word")

            if self.game_state == States.no_game:

                self.created_game_state(message)
                self.add_player(message)

                name = self.ids_to_names[message.chat.id]
                self.bot.send_message(message.chat.id, f"{GaS_T.CG}{name}.")

                chat_id = message.chat.id
                text = GaS_T.CHC
                keyboard = self.character_keyboard()

            else:

                chat_id = message.chat.id
                text = GaS_T.GOG
                keyboard = self.remove_keyboard()

            self.bot.send_message(chat_id, text, reply_markup=keyboard)

        # Terminate Game #
        @self.bot.message_handler(func=self.is_admin_terminating_game)
        def terminating_game_word(message):
            print("terminate_game")

            if self.game_state == States.no_game:

                chat_id = message.chat.id
                text = GaS_T.NGET
                keyboard = self.remove_keyboard()

                self.bot.send_message(chat_id, text, reply_markup=keyboard)

            else:

                text = GaS_T.TGT
                keyboard = self.remove_keyboard()

                for id in self.ids:

                    self.bot.send_message(id, text, reply_markup=keyboard)

                self.ended_game_state()

        # Search Command #
        @self.bot.message_handler(commands=["search"])
        def search_command(message):
            print("search_command")

            chat_id = message.chat.id
            text = GaS_T.SFG
            keyboard = self.remove_keyboard()

            self.bot.send_message(chat_id, text, reply_markup=keyboard)

            if self.game_state == States.no_game:

                text = GaS_T.NGSC
                keyboard = self.remove_keyboard()

            else:

                text = GaS_T.GESC
                keyboard = self.join_game_keyboard()

            self.bot.send_message(chat_id, text, reply_markup=keyboard)

        # Join Game #
        @self.bot.message_handler(regexp=Keys.join_game)
        def joining_game(message):
            print("join_game")

            chat_id = message.chat.id

            if self.game_state == States.created:

                if chat_id not in self.ids:

                    self.add_player(message)
                    name = self.ids_to_names[chat_id]

                    text = f"{name}{GaS_T.GAJG}"
                    self.bot.send_message(self.admin_id, text)

                    text = f"{GaS_T.YJGS}\n{GaS_T.YN}{name}."
                    keyboard = self.remove_keyboard()

                else:

                    text = GaS_T.YAJ
                    keyboard = self.remove_keyboard()

            elif self.game_state == States.started:

                text = GaS_T.GIOG
                keyboard = self.remove_keyboard()

            elif self.game_state == States.no_game:

                text = GaS_T.NGSC
                keyboard = self.remove_keyboard()

            self.bot.send_message(chat_id, text, reply_markup=keyboard)

        # Print Input #
        @self.bot.message_handler()
        def print_function(message):
            print("print_function")

            text = Vote_T.CNF
            chat_id = message.chat.id

            self.bot.send_message(chat_id, text)
            print(demojize(message.text))

        # Choose_character #
        @self.bot.callback_query_handler(func=self.is_admin_choosing_character)
        def Choose_character_query(query):
            print("choose_character")

            self.admin_choose_characters(query)

        # Send Info #
        @self.bot.callback_query_handler(func=self.is_admin_starting_game)
        def starting_game_query(query):
            print("starting_game_query")

            if self.game_state == States.created:

                self.start_game(query)

            elif self.game_state == States.no_game:

                text = GaS_T.YSCG
                self.bot.answer_callback_query(query.id, text)

            else:

                text = GaS_T.TGHS
                self.bot.answer_callback_query(query.id, text)

        # ccommander choosing name #
        @self.bot.callback_query_handler(func=self.is_commander_choosing_name)
        def commander_choosing_name(query):
            print("commander_choosing_name")

            self.commander_choose_name(query)

        # commander pressing button #
        @self.bot.callback_query_handler(
                func=self.is_commander_pressing_button)
        def commander_press_button(query):
            print("commander_press_button")

            self.game.check_committee(self.mission_voters)

            if self.game.acceptable_round:

                self.commander_decision(query)

            else:

                self.pick_right_players(query)

        # committee vote #
        @self.bot.callback_query_handler(func=self.is_eligible_vote)
        def vote_for_committee(query):
            print("vote_for_committee")

            name = self.ids_to_names[query.message.chat.id]

            if name in self.committee_voters:

                self.committee_voters.remove(name)

                if self.committee_voters:

                    self.handle_committee_vote(query)

                else:

                    self.handle_committee_vote(query)
                    self.game.count_committee_vote(self.committee_votes)
                    self.send_committee_summary()

                    if self.game.reject_count == 5:

                        self.end_5_reject()

                    elif self.game.committee_accept:

                        self.go_to_mission_voting()

                    else:

                        self.go_to_next_commander()

            else:

                self.you_voted(query)

        # mission vote #
        @self.bot.callback_query_handler(func=self.is_eligible_fail_success)
        def vote_for_mission(query):
            print("vote_for_mission")

            name = self.ids_to_names[query.message.chat.id]

            if name in self.mission_voters:

                self.mission_voters.remove(name)

                if self.mission_voters:

                    self.handle_mission_vote(query)

                else:

                    self.handle_mission_vote(query)
                    self.game.mission_result(self.mission_votes)
                    self.send_mission_summary()

                    if self.game.evil_wins == 3:

                        self.end_evil_3_won()

                    elif self.game.city_wins == 3:

                        self.city_3_won()

                    else:

                        self.go_to_next_commander()

            else:

                self.you_voted(query)

        @self.bot.callback_query_handler(func=self.is_assassin_choosing_name)
        def assassin_choosing_name(query):
            print("assassin_choosing_name")

            self.assassin_choose_name(query)

        @self.bot.callback_query_handler(func=self.is_assassin_pressing_button)
        def assassin_pressing_button(query):
            print("assassin_pressing_button")

            if self.assassins_guess == str():

                self.choose_someone(query)

            else:

                self.end_assassin_shot()

        # Pin Query #
        @self.bot.callback_query_handler(func=self.is_player_query_pin)
        def pin_query(query):
            print("pin_query")

            chat_id = query.message.chat.id
            message_id = query.message.id
            keyboard = self.unpin_keyboard()

            self.bot.pin_chat_message(chat_id, message_id)
            self.bot.edit_message_reply_markup(chat_id, message_id,
                                               reply_markup=keyboard)

        # Pin Query #
        @self.bot.callback_query_handler(func=self.is_player_query_unpin)
        def unpin_query(query):
            print("pin_query")

            chat_id = query.message.chat.id
            message_id = query.message.id
            keyboard = self.pin_keyboard()

            self.bot.unpin_chat_message(chat_id, message_id,)
            self.bot.edit_message_reply_markup(chat_id, message_id,
                                               reply_markup=keyboard)

        # OKs Query #
        @self.bot.callback_query_handler(func=self.is_player_query_ok)
        def ok_query(query):
            print("ok_query")

            chat_id = query.message.chat.id
            message_id = query.message.id

            self.bot.delete_message(chat_id, message_id)

        # delete inline keyboard #
        @self.bot.callback_query_handler(func=lambda x: x)
        def delete_inline_keyboards(query):
            print("delete_inline_keyboard")

            chat_id = query.message.chat.id
            message_id = query.message.id

            if self.game_state == States.no_game:

                self.bot.delete_message(chat_id, message_id)

            else:

                word_list = [Keys.fail,
                             Keys.success,
                             Keys.agree,
                             Keys.disagree,
                             Keys.pin,
                             Keys.unpin,
                             *self.names,
                             *self.checked_names,
                             *self.optional_characters,
                             *self.checked_optional_characters]

                if query.data in word_list:

                    self.bot.answer_callback_query(query.id, Oth_T.TA)

                else:

                    self.bot.delete_message(chat_id, message_id)

    def grab_name(self, message):

        name = str()

        if message.chat.type == "private":

            if ((message.chat.first_name is not None)
               and (message.chat.last_name is not None)):
                name = message.chat.first_name + " " + message.chat.last_name

            elif not (message.chat.last_name):
                name = message.chat.first_name

            elif not (message.chat.first_name):
                name = message.chat.last_name

            return name

        elif message.chat.type == "group" or message.chat.type == "supergroup":

            if ((message.from_user.first_name is not None)
               and (message.from_user.last_name is not None)):

                name = (message.from_user.first_name +
                        " " + message.from_user.last_name)

            elif not (message.from_user.last_name):
                name = message.from_user.first_name

            elif not (message.from_user.first_name):
                name = message.from_user.last_name

            name = name + " @ " + message.chat.title

            return name

    def fix_name(self, currupted_name):

        if currupted_name[0:len(Keys.check_box)] == Keys.check_box:

            return currupted_name[len(Keys.check_box):]

        else:

            return currupted_name

    def add_player(self, message):

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

    def admin_choose_characters(self, query):

        add_remove_name = self.fix_name(query.data)

        if add_remove_name in self.choosed_characters:

            self.choosed_characters.remove(add_remove_name)
            text = f"{add_remove_name}{GaS_T.RFG}"

        else:

            self.choosed_characters.append(add_remove_name)
            text = f"{add_remove_name}{GaS_T.ATG}"

        self.bot.answer_callback_query(query.id, text)

        chat_id = query.message.chat.id
        message_id = query.message.id
        keyboard = self.character_keyboard()

        self.bot.edit_message_reply_markup(chat_id, message_id,
                                           reply_markup=keyboard)

    def define_game(self):

        name_for_game = self.names[:]
        character_for_game = self.choosed_characters[:]
        self.game = Avalon_Engine(name_for_game, character_for_game)

    def send_info(self):

        self.define_game()
        self.started_game_state()
        small_sep = GaS_T.small_sep
        big_sep = GaS_T.big_sep

        for name, character in self.game.names_to_characters.items():

            if character.name == Char_T.assassin:
                self.assassin_id = self.names_to_ids[name]

            chat_id = self.names_to_ids[name]

            text = (GaS_T.IGI +
                    "\n" + big_sep +
                    "\n" + GaS_T.YR +
                    "\n" + "-" + self.game.all_messages[character.name] +
                    "\n" + big_sep +
                    "\n" + GaS_T.PINF +
                    "\n" + f"# Players: {self.game.n_players}" +
                    "\n" + f"# Cities: {self.game.n_city}" +
                    "\n" + f"# Evils: {self.game.n_evil}" +
                    "\n" + small_sep +
                    "\n" + GaS_T.CIG +
                    "\n" + self.game.character_in_game +
                    big_sep +
                    "\n" + "Rounds:" +
                    "\n" +
                    "\n" + self.add_round_info())

            keyboard = self.pin_keyboard()
            self.bot.send_message(chat_id, text, reply_markup=keyboard)

    def make_commander_order(self):

        self.commander_order = self.names[:]

        if self.shuffle_commander_order:

            shuffle(self.commander_order)

    def resolve_commander(self):

        if self.commander_number == len(self.names):

            self.commander_number = 0

        self.current_commander = self.commander_order[self.commander_number]
        self.current_commander_id = self.names_to_ids[self.current_commander]
        self.commander_number += 1

    def add_round_info(self):

        round_info = str()
        two_fail = "(2)" if self.game.two_fails else ""

        for index, this_round in enumerate(self.game.all_round[1:]):

            if index + 1 >= self.game.round:

                sign = "" if index == 0 else "|"

                if index + 1 == 4:

                    if index + 1 == self.game.round:

                        text = emojize(f":keycap_{this_round}: {two_fail}")

                    else:

                        text = f"{this_round} {two_fail}"

                else:

                    if index + 1 == self.game.round:

                        text = emojize(f":keycap_{this_round}:")

                    else:

                        text = f"{this_round}"

                round_info += sign
                round_info += f"{text: ^10}"

            else:

                result = self.game.all_wins[index + 1]
                sign = "" if index == 0 else "|"

                if result == 1:

                    text = f"{Keys.city_win}"

                elif result == -1:

                    text = f"{Keys.evil_win}"

                round_info += sign
                round_info += f"{text: ^7}"

        return round_info

    def send_commander_order(self):

        commander_order_show = str()

        for index, name in enumerate(self.commander_order):

            if index == self.commander_number - 1:

                commander_order_show += emojize(f"{name} --> (:crown:)\n")

            else:

                commander_order_show += f"{name}\n"

        text = emojize(f"{Co_T.CO} \n\n" + commander_order_show)
        keyboard = self.ok_keyboard()

        for id in self.ids:

            self.bot.send_message(id, text, reply_markup=keyboard)

    def go_to_next_commander(self):

        self.committee_choosing_state()
        self.resolve_commander()
        self.send_commander_order()

        n_committee = self.game.all_round[self.game.round]

        text = f"{Co_T.CCN1}{Co_T.CCN2_1}{n_committee}{Co_T.CCN2_2}"
        keyboard = self.commander_keyboard()

        self.bot.send_message(self.current_commander_id,
                              text, reply_markup=keyboard)

    def start_game(self, query):

        try:

            self.send_info()
            self.make_commander_order()
            self.go_to_next_commander()

        except ValueError as e:

            query_id = query.id
            self.bot.answer_callback_query(query_id, e.args[0])

    def transfer_committee_vote(self, query):

        if query.data == Keys.agree:
            self.committee_votes.append(1)

        elif query.data == Keys.disagree:
            self.committee_votes.append(0)

    def transfer_mission_vote(self, query):

        if query.data == Keys.success:
            self.mission_votes.append(1)

        elif query.data == Keys.fail:
            self.mission_votes.append(0)

    def commander_choose_name(self, query):

        query_id = query.id
        add_remove_name = self.fix_name(query.data)

        if add_remove_name in self.mission_voters:

            self.mission_voters.remove(add_remove_name)
            text = f"{add_remove_name}{Co_T.RFC}"

        else:

            self.mission_voters.append(add_remove_name)
            text = f"{add_remove_name}{Co_T.ATC}"

        self.bot.answer_callback_query(query_id, text)

        chat_id = query.message.chat.id
        message_id = query.message.id
        keyboard = self.commander_keyboard()

        self.bot.edit_message_reply_markup(chat_id, message_id,
                                           reply_markup=keyboard)

    def commander_decision(self, query):

        if query.data == Keys.propose:

            text = f"{Co_T.PCC}\n-" + "\n-".join(self.mission_voters)
            keyboard = self.ok_keyboard()

            for id in self.ids:

                self.bot.send_message(id, text, reply_markup=keyboard)

        elif query.data == Keys.final:

            text = f"{Co_T.FCC}\n-" + "\n-".join(self.mission_voters)
            keyboard = self.committee_vote_keyboard()

            for id in self.ids:
                self.bot.send_message(id, text, reply_markup=keyboard)

            self.bot.delete_message(query.message.chat.id, query.message.id)
            self.committee_voting_state()

    def pick_right_players(self, query):

        query_id = query.id
        n_committee = self.game.all_round[self.game.round]
        text = f"{Co_T.CCN2_1}{n_committee}{Co_T.CCN2_2}"

        self.bot.answer_callback_query(query_id, text)

    def go_to_mission_voting(self):

        text = Vote_T.MV

        for name in self.mission_voters:

            self.mission_voters_name.append(name)
            chat_id = self.names_to_ids[name]
            keyboard = self.mission_vote_keyboard()

            self.bot.send_message(chat_id, text, reply_markup=keyboard)

        self.mission_voting_state()

    def handle_committee_vote(self, query):

        self.transfer_committee_vote(query)

        chat_id = query.message.chat.id
        message_id = query.message.id
        text = emojize(f"{Vote_T.CV}{query.data}")

        self.bot.answer_callback_query(query.id, text)
        self.bot.delete_message(chat_id, message_id)

        name = self.ids_to_names[chat_id]
        self.committee_summary += self.add_committee_vote(name, query.data)

    def handle_mission_vote(self, query):

        self.transfer_mission_vote(query)

        chat_id = query.message.chat.id
        message_id = query.message.id
        text = Vote_T.SFV

        self.bot.answer_callback_query(query.id, text)
        self.bot.delete_message(chat_id, message_id)

    def you_voted(self, query):

        query_id = query.id
        text = emojize(Vote_T.YVB)

        self.bot.answer_callback_query(query_id, text)

    def city_3_won(self):

        text = GaSi_T.CW3R
        keyboard = self.remove_keyboard()

        for id in self.ids:

            self.bot.send_message(id, text, reply_markup=keyboard)

        text = Ass_T.ASS1
        keyboard = self.assassin_keyboard()

        self.bot.send_message(self.assassin_id, text, reply_markup=keyboard)

        self.assassin_shooting_state()

    def assassin_choose_name(self, query):

        self.assassins_guess = self.fix_name(query.data)

        text = emojize(f"{Ass_T.ASS2_1}{self.assassins_guess}{Ass_T.ASS2_2}")
        self.bot.answer_callback_query(query.id, text)

        chat_id = query.message.chat.id
        message_id = query.message.id
        keyboard = self.assassin_keyboard()

        self.bot.edit_message_reply_markup(chat_id, message_id,
                                           reply_markup=keyboard)

    def choose_someone(self, query):

        query_id = query.id
        text = Ass_T.ASS3
        self.bot.answer_callback_query(query_id, text)

    def end_assassin_shot(self):

        self.game.assassin_shoot(self.assassins_guess)

        if self.game.assassin_shooted_right:

            text = f"{GaSi_T.EW}{GaSi_T.REW2}"

        else:

            text = f"{GaSi_T.CW}{GaSi_T.RCW}"

        keyboard = self.remove_keyboard()

        for id in self.ids:

            self.bot.send_message(id, text, reply_markup=keyboard)

        self.ended_game_state()

    def end_evil_3_won(self):

        text = f"{GaSi_T.EW}{GaSi_T.REW3}"
        keyboard = self.remove_keyboard()

        for id in self.ids:

            self.bot.send_message(id, text, reply_markup=keyboard)

        self.ended_game_state()

    def end_5_reject(self):

        text = f"{GaSi_T.EW}{GaSi_T.REW1}"
        keyboard = self.remove_keyboard()

        for id in self.ids:

            self.bot.send_message(id, text, reply_markup=keyboard)

        self.ended_game_state()

    # State functions
    # These functions help keep track of the state during the game.

    def created_game_state(self, message):

        self.game_state = States.created
        self.admin_id = message.chat.id

    def started_game_state(self):

        self.game_state = States.started

    def committee_choosing_state(self):

        self.game_state = States.started
        self.game_sub_state = Sub_States.committee_choosing

        self.mission_voters = list()
        self.mission_voters_name = list()

    def committee_voting_state(self):

        self.game_state = States.started
        self.game_sub_state = Sub_States.committee_voting
        self.committee_voters = self.names[:]

        self.committee_votes = list()
        self.committee_summary = str()

    def mission_voting_state(self):

        self.game_state = States.started
        self.game_sub_state = Sub_States.mission_voting
        self.mission_votes = list()

    def assassin_shooting_state(self):

        self.game_state = States.started
        self.game_sub_state = Sub_States.assassin_shooting

    def ended_game_state(self):

        self.initial_condition()

    # rule checkers
    # the following functions check the necessary rules
    # for each message handler. their output is either True or False.

    # Whos Conditions

    def is_admin_message(self, message):

        c_1 = self.admin_id == message.chat.id

        return c_1

    def is_admin(self, query):
        print("is_admin")

        c_1 = self.admin_id == query.message.chat.id

        return c_1

    def is_player(self, query):
        print("is_player")

        c_1 = query.message.chat.id in self.ids

        return c_1

    def is_commander(self, query):
        print("is_commander")

        c_1 = self.current_commander_id == query.message.chat.id

        return c_1

    def is_assassin(self, query):
        print("is_assassin")

        c_1 = self.assassin_id == query.message.chat.id

        return c_1

    # Whens Conditions
    # Main State
    def is_no_game_state(self):
        print("is_no_game_state")

        c_1 = self.game_state == States.no_game
        return c_1

    def is_created_state(self):
        print("is_created_state")

        c_1 = self.game_state == States.created
        return c_1

    def is_started_state(self):
        print("is_started_state")

        c_1 = self.game_state == States.started
        return c_1

    # Whens Conditions
    # Sub States
    def is_committee_choosing_state(self):

        c_1 = self.is_started_state()
        c_2 = self.game_sub_state == Sub_States.committee_choosing

        return c_1 and c_2

    def is_committee_voting_state(self):

        c_1 = self.is_started_state()
        c_2 = self.game_sub_state == Sub_States.committee_voting

        return c_1 and c_2

    def is_mission_voting_state(self):

        c_1 = self.is_started_state()
        c_2 = self.game_sub_state == Sub_States.mission_voting

        return c_1 and c_2

    def is_assassin_shooting_state(self):

        c_1 = self.is_started_state()
        c_2 = self.game_sub_state == Sub_States.assassin_shooting

        return c_1 and c_2

    # Whos, Whens, Whats (Copmlex Conditions)
    def is_admin_starting_game(self, query):

        # who
        c_1 = self.is_admin(query)

        # when
        c_2 = self.is_created_state()

        # what
        c_3 = query.data == Keys.start_game

        return c_1 and c_2 and c_3

    def is_admin_terminating_game(self, message):

        # who
        c_1 = self.is_admin_message(message)

        # when
        c_2 = self.is_created_state()
        c_3 = self.is_started_state()

        # what
        c_4 = message.text == self.terminating_game_word

        return c_1 and (c_2 or c_3) and c_4

    def is_admin_choosing_character(self, query):
        print("is_admin_choosing_character")

        # who
        c_1 = self.is_admin(query)

        # when
        c_2 = self.is_created_state()

        # What
        c_3 = query.data in self.optional_characters
        c_4 = query.data in self.checked_optional_characters

        return c_1 and c_2 and (c_3 or c_4)

    def is_player_query_ok(self, query):

        # Who
        c_1 = self.is_player(query)

        # When: Any Time

        # What
        c_2 = query.data == Keys.ok

        return c_1 and c_2

    def is_player_query_pin(self, query):

        # Who
        c_1 = self.is_player(query)

        # When: Any Time

        # What
        c_2 = query.data == Keys.pin
        return c_1 and c_2

    def is_player_query_unpin(self, query):

        # Who
        c_1 = self.is_player(query)

        # When: Any Time

        # What
        c_2 = query.data == Keys.unpin
        return c_1 and c_2

    def is_commander_choosing_name(self, query):
        print("is_commander_choosing_name")

        # who
        c_1 = self.is_commander(query)

        # when
        c_2 = self.is_committee_choosing_state()

        # what
        c_3 = query.data in self.names
        c_4 = query.data in self.checked_names

        return c_1 and c_2 and (c_3 or c_4)

    def is_commander_pressing_button(self, query):
        print("is_commander_pressing_button")

        # who
        c_1 = self.is_commander(query)

        # when
        c_2 = self.is_committee_choosing_state()

        # what
        c_3 = query.data in [Keys.final, Keys.propose]

        return c_1 and c_2 and c_3

    def is_eligible_vote(self, query):
        print("is_eligible_vote")

        # what
        c_1 = self.is_player(query)

        # when
        c_2 = self.is_committee_voting_state()

        # what
        c_3 = query.data in [Keys.agree, Keys.disagree]
        # TODO: Do we need emojize ?
        return c_1 and c_2 and c_3

    def is_eligible_fail_success(self, query):
        print("is_eligible_fail_success")

        # when
        c_1 = self.is_player(query)

        # who
        c_2 = self.is_mission_voting_state()

        # what
        c_3 = query.data in [Keys.success, Keys.fail]

        return c_1 and c_2 and c_3

    def is_assassin_choosing_name(self, query):
        print("is_assassin_choosing_name")

        # who
        c_1 = self.is_assassin(query)

        # when
        c_2 = self.is_assassin_shooting_state()

        # what
        c_3 = query.data != Keys.assassin_shoots

        return c_1 and c_2 and c_3

    def is_assassin_pressing_button(self, query):
        print("is_assassin_pressing_button")

        # who
        c_1 = self.is_assassin(query)

        # when
        c_2 = self.is_assassin_shooting_state()

        # what
        c_3 = query.data == Keys.assassin_shoots

        return c_1 and c_2 and c_3

    # keyboard makers
    # the following functions make keyboard for players.

    def character_keyboard(self):

        keyboard = types.InlineKeyboardMarkup(row_width=1)

        for character in self.optional_characters:

            if character in self.choosed_characters:

                temp_str = demojize(Keys.check_box)

            else:

                temp_str = ""

            button = emojize(f"{temp_str}{character}")
            inline = types.InlineKeyboardButton(button, callback_data=button)
            keyboard.row(inline)

        start = Keys.start_game
        inline = types.InlineKeyboardButton(start, callback_data=start)
        keyboard.add(inline)

        return keyboard

    def join_game_keyboard(self):

        buttons_text = [Keys.join_game]
        buttons = map(types.KeyboardButton, buttons_text)
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        keyboard.add(*buttons)

        return keyboard

    def commander_keyboard(self):

        keyboard = types.InlineKeyboardMarkup(row_width=2)

        for name in self.names:

            if name in self.mission_voters:

                temp_str = demojize(Keys.check_box)

            else:

                temp_str = ""

            button = emojize(f"{temp_str}{name}")
            inline = types.InlineKeyboardButton(button, callback_data=button)
            keyboard.row(inline)

        final = Keys.final
        propose = Keys.propose

        f_inline = types.InlineKeyboardButton(final, callback_data=final)
        p_inline = types.InlineKeyboardButton(propose, callback_data=propose)

        keyboard.add(p_inline, f_inline)

        return keyboard

    def committee_vote_keyboard(self):

        keyboard = types.InlineKeyboardMarkup(row_width=2)

        agree = Keys.agree
        disagree = Keys.disagree
        a_inline = types.InlineKeyboardButton(agree, callback_data=agree)
        d_inline = types.InlineKeyboardButton(disagree, callback_data=disagree)

        keyboard.add(a_inline, d_inline)
        return keyboard

    def mission_vote_keyboard(self):

        keyboard = types.InlineKeyboardMarkup(row_width=2)

        sucess = Keys.success
        fail = Keys.fail

        s_inline = types.InlineKeyboardButton(sucess, callback_data=sucess)
        f_inline = types.InlineKeyboardButton(fail, callback_data=fail)

        inline_buttons = [s_inline, f_inline]
        shuffle(inline_buttons)

        keyboard.add(*inline_buttons)

        return keyboard

    def assassin_keyboard(self):

        keyboard = types.InlineKeyboardMarkup(row_width=1)

        for name in self.names:

            if name == self.assassins_guess:

                temp_str = demojize(Keys.check_box)

            else:

                temp_str = ""

            button = emojize(f"{temp_str}{name}")
            inline = types.InlineKeyboardButton(button, callback_data=button)
            keyboard.row(inline)

        assassin = Keys.assassin_shoots
        inline = types.InlineKeyboardButton(assassin, callback_data=assassin)
        keyboard.row(inline)

        return keyboard

    def ok_keyboard(self):

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        ok = Keys.ok

        inline = types.InlineKeyboardButton(ok, callback_data=ok)
        keyboard.row(inline)

        return keyboard

    def pin_keyboard(self):

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        pin = Keys.pin

        inline = types.InlineKeyboardButton(pin, callback_data=pin)
        keyboard.row(inline)

        return keyboard

    def unpin_keyboard(self):

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        pin = Keys.unpin

        inline = types.InlineKeyboardButton(pin, callback_data=pin)
        keyboard.row(inline)

        return keyboard

    def remove_keyboard(self):
        return types.ReplyKeyboardRemove()

    # Summary Functions
    # the following function are to make summary during the fellow of the game.

    def add_committee_header(self, rejected_count):

        sep = GaS_T.small_sep
        return ("\n" + f"Rejection Count: {rejected_count}" +
                "\n" + sep +
                "\n" + "Committee Votes:" +
                "\n")

    def add_committee_vote(self, name, vote):

        return emojize(f"-{name} voted: {vote}" +
                       "\n")

    def add_committee_footer(self):

        sign = Keys.accept if self.game.committee_accept else Keys.declined
        sep = GaS_T.small_sep

        return (sep +
                "\n" + "Committee Result:"
                "\n" + sign)

    def add_mission_vote(self, names, fail, success, Round, commander):
        sep = GaS_T.small_sep

        return (f"Round: {Round} (Commander: {commander})" +
                "\n" + sep +
                "\n" + "Committee Memebers:" +
                "\n" + "-" + names +
                "\n" + sep +
                "\n" + "Mission Results:" +
                "\n" + f"# Sucesses: {success}" +
                "\n" + f"# Fails: {fail}" +
                "\n" + sep +
                "\n" + "Game Results:"
                "\n" + sep +
                "\n")

    def send_committee_summary(self):

        if self.game.committee_accept:

            self.game.reject_count = 0

        else:

            self.game.reject_count += 1

        rejected = self.game.reject_count

        self.committee_summary = (self.add_committee_header(rejected) +
                                  self.committee_summary)
        self.committee_summary += self.add_committee_footer()

        keyboard = self.remove_keyboard()

        for id in self.ids:

            self.bot.send_message(
                id, self.committee_summary, reply_markup=keyboard)

    def send_mission_summary(self):

        Round = self.game.round - 1
        names = "\n-".join(self.mission_voters_name)
        commander = self.current_commander
        self.game_summary = self.add_mission_vote(names, self.game.fail_count,
                                                  self.game.success_count,
                                                  Round, commander)

        self.game_summary += self.add_round_info()
        keyboard = self.remove_keyboard()

        for id in self.ids:

            self.bot.send_message(id, self.game_summary, reply_markup=keyboard)


my_bot = Bot()
