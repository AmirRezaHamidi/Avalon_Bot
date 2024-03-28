from Constants import Char_T, CharM_T


# Arthur Side
class Servant():

    def __init__(self):
        self.message = CharM_T.khiar
        self.name = Char_T.khiar
        self.side = Char_T.city_side
        self.has_info = False


class Persival():

    def __init__(self):

        self.message = CharM_T.persival
        self.name = Char_T.persival
        self.side = Char_T.city_side
        self.has_info = True


class Merlin():

    def __init__(self):

        self.message = CharM_T.merlin
        self.name = Char_T.merlin
        self.side = Char_T.city_side
        self.has_info = True


# Mordered Side
class Minion():

    def __init__(self):

        self.message = CharM_T.mafia
        self.name = Char_T.mafia
        self.side = Char_T.evil_side
        self.has_info = True


class Morgana():

    def __init__(self):

        self.message = CharM_T.Morgana
        self.name = Char_T.morgana
        self.side = Char_T.evil_side
        self.has_info = True


class Assassin():

    def __init__(self):

        self.message = CharM_T.assassin
        self.name = Char_T.assassin
        self.side = Char_T.evil_side
        self.has_info = True


class Oberon():

    def __init__(self):

        self.message = CharM_T.oberon
        self.name = Char_T.oberon
        self.side = Char_T.evil_side
        self.has_info = False


class Mordred():

    def __init__(self):

        self.message = CharM_T.mordred
        self.name = Char_T.mordred
        self.side = Char_T.evil_side
        self.has_info = True
