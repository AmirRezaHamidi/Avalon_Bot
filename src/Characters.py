from Constants import Char_Texts


# Arthur Side
class Servant():

    def __init__(self):
        self.message = 'You are a "Khiar".'
        self.name = Char_Texts.khiar
        self.side = Char_Texts.city_side
        self.has_info = False


class Persival():

    def __init__(self):

        self.message = ('You are the "Persival".' +
                        "\n" + "Merlin and Morgana:" +
                        "\n" +
                        "\n")
        self.name = Char_Texts.persival
        self.side = Char_Texts.city_side
        self.has_info = True


class Merlin():

    def __init__(self):

        self.message = ('You are the "Merlin".' +
                        "\n" + "Mafia Team:" +
                        "\n" +
                        "\n")
        self.name = Char_Texts.merlin
        self.side = Char_Texts.city_side
        self.has_info = True


# Mordered Side
class Minion():

    def __init__(self):

        self.message = ('You are a "Mafia Mamooli".' +
                        "\n" + "Mafia Team:"
                        "\n" +
                        "\n")
        self.name = Char_Texts.mafia
        self.side = Char_Texts.evil_side
        self.has_info = True


class Morgana():

    def __init__(self):

        self.message = ('You are the "Morgana".' +
                        "\n" + "Mafia Team:" +
                        "\n" +
                        "\n")
        self.name = Char_Texts.morgana
        self.side = Char_Texts.evil_side
        self.has_info = True


class Assassin():

    def __init__(self):

        self.message = ('You are the "Assassin".' +
                        "\n" + "Mafia Team:" +
                        "\n" +
                        "\n")
        self.name = Char_Texts.assassin
        self.side = Char_Texts.evil_side
        self.has_info = True


class Oberon():

    def __init__(self):

        self.message = 'You are the "Oberon".'
        self.name = Char_Texts.oberon
        self.side = Char_Texts.evil_side
        self.has_info = False


class Mordred():

    def __init__(self):

        self.message = ('You are the "Mordred".' +
                        "\n" + "Mafia Team:" +
                        "\n" +
                        "\n")
        self.name = Char_Texts.mordred
        self.side = Char_Texts.evil_side
        self.has_info = True
