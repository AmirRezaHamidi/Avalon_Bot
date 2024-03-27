import random
from Characters import (Assassin, Merlin, Minion, Mordred,
                        Morgana, Oberon, Persival, Servant)
from Constants import Char_Texts, Texts


class Avalon_Engine():

    def __init__(self, names, optional_characters=None):

        self.names = names

        # Character Parameters
        self.optional_characters = optional_characters
        self.game_character = [Assassin(), Merlin()]
        self.names_to_characters = dict()

        self.mordred_in_game = False
        self.morgana_in_game = False
        self.persival_in_game = False

        self.string_character = list()
        self.all_messages = dict()

        self.round = 1
        self.city_wins = int()
        self.evil_wins = int()
        self.reject_count = int()
        self.all_wins = [0] * 6

        self.acceptable_round = False
        self.committee_accept = False
        self.king_guessed_right = False
        self.assassin_shooted_right = False

        self.round_info()
        self.character_assignment()
        self.character_message()

    def round_info(self):

        if len(self.names) == 5:
            self.all_round = [0, 2, 3, 2, 3, 3]
            self.two_fails = False

        elif len(self.names) == 6:
            self.all_round = [0, 2, 3, 4, 3, 4]
            self.two_fails = False

        elif len(self.names) == 7:
            self.all_round = [0, 2, 3, 3, 4, 4]
            self.two_fails = True

        elif len(self.names) == 8:
            self.all_round = [0, 3, 4, 4, 5, 5]
            self.two_fails = True

        elif len(self.names) == 9:
            self.all_round = [0, 3, 4, 4, 5, 5]
            self.two_fails = True

        elif len(self.names) == 10:
            self.all_round = [0, 3, 4, 4, 5, 5]
            self.two_fails = True

    def count_side(self):

        current_city = 0
        current_evil = 0

        for character in self.game_character:

            if character.side == Char_Texts.city_side:

                current_city += 1

            elif character.side == Char_Texts.evil_side:
                current_evil += 1

        return current_city, current_evil

    def power_character(self):

        if self.optional_characters is not None:

            if Char_Texts.persival_morgana in self.optional_characters:

                self.game_character.append(Morgana())
                self.game_character.append(Persival())

            if Char_Texts.mordred in self.optional_characters:

                self.game_character.append(Mordred())

            if Char_Texts.oberon in self.optional_characters:

                self.game_character.append(Oberon())

    def non_power_characters(self, n_city, n_evil):

        current_city, current_evil = self.count_side()
        city_diff = n_city - current_city
        evil_diff = n_evil - current_evil

        if city_diff >= 0 and evil_diff >= 0:

            for _ in range(city_diff):
                self.game_character.append(Servant())

            for _ in range(evil_diff):
                self.game_character.append(Minion())
        else:
            message = Texts.PCE
            raise ValueError(message)

    def resolve_character(self):

        self.power_character()

        if len(self.names) < 5:

            message = Texts.PNE
            raise ValueError(message)

        if len(self.names) < len(self.game_character):
            message = Texts.PCE
            raise ValueError(message)

        else:

            if len(self.names) == 5:

                n_city = 3
                n_evil = 2
                self.non_power_characters(n_city, n_evil)

            elif len(self.names) == 6:

                n_city = 4
                n_evil = 2
                self.non_power_characters(n_city, n_evil)

            elif len(self.names) == 7:

                n_city = 4
                n_evil = 3
                self.non_power_characters(n_city, n_evil)

            elif len(self.names) == 8:

                n_city = 5
                n_evil = 3
                self.non_power_characters(n_city, n_evil)

            elif len(self.names) == 9:

                n_city = 6
                n_evil = 3
                self.non_power_characters(n_city, n_evil)

            elif len(self.names) == 10:

                n_city = 6
                n_evil = 4
                self.non_power_characters(n_city, n_evil)

    def character_assignment(self):

        self.resolve_character()

        random.shuffle(self.names)

        for index, name in enumerate(self.names):

            self.names_to_characters[name] = self.game_character[index]
            self.string_character.append(self.game_character[index].name)

    def character_message(self):

        for character in self.game_character:

            self.all_messages[character.name] = character.message

            if character.name == Char_Texts.mordred:
                self.mordred_in_game = True

            if character.name == Char_Texts.persival:
                self.persival_in_game = True

            if character.name == Char_Texts.morgana:
                self.morgana_in_game = True

        print(self.game_character)

        for name, character in self.names_to_characters.items():

            f_name = f"\n-{name}"
            if character.has_info:

                if character.side == Char_Texts.evil_side:

                    if character.name != Char_Texts.mordred:
                        self.all_messages[Char_Texts.merlin] += f_name

                    self.all_messages[Char_Texts.assassin] += f_name
                    self.all_messages[Char_Texts.mafia] += f_name

                    if self.morgana_in_game:
                        self.all_messages[Char_Texts.morgana] += f_name

                    if self.mordred_in_game:
                        self.all_messages[Char_Texts.mordred] += f_name

                    if self.persival_in_game:

                        if Char_Texts.morgana:
                            self.all_messages[Char_Texts.persival] += f_name
                # add merlin to persival

    def check_committee(self, mission_voters):

        if len(mission_voters) == self.all_round[self.round]:

            self.acceptable_round = True

        else:

            self.acceptable_round = False

    def count_committee_vote(self, committee_votes):

        negative_votes = committee_votes.count(0)
        positive_votes = committee_votes.count(1)

        if positive_votes >= negative_votes:

            self.committee_accept = True

        else:

            self.committee_accept = False

    def mission_result(self, mission_votes):

        self.fail_count = mission_votes.count(0)
        self.success_count = mission_votes.count(1)

        condition_1 = self.round == 4
        condition_2 = self.two_fails is True

        if (condition_1) and (condition_2):

            if self.fail_count >= 2:

                self.evil_wins += 1
                self.who_won = Char_Texts.evil_side
                self.all_wins[self.round] = -1

            else:

                self.city_wins += 1
                self.who_won = Char_Texts.city_side
                self.all_wins[self.round] = 1

        else:

            if self.fail_count >= 1:

                self.evil_wins += 1
                self.who_won = Char_Texts.evil_side
                self.all_wins[self.round] = -1

            else:

                self.city_wins += 1
                self.who_won = Char_Texts.city_side
                self.all_wins[self.round] = 1

        self.round += 1

    def assassin_shoot(self, shooted_name):

        if self.names_to_characters[shooted_name].name == Char_Texts.merlin:
            self.assassin_shooted_right = True
