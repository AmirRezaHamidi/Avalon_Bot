# Arthur Side
class Servant():

    def __init__(self):
        self.message = 'Character: Loyal Servant of Author\n'\
                       'Side: City\n'\
                       'Weakness: You do not know the identity of anyone '\
                       'except for yourself.\n'\
                       'Guide: Try to finds the "Merlin" and and help him/her'\
                       ' win the game.'

        self.name = "Servant"
        self.side = "City"


class Persival():

    def __init__(self):

        self.message = 'Character: Persival\n'\
                       'Side: City\n'\
                       'Power: You will be given two names,'\
                       'one of them is "Merlin" and one of the is "Morgana". '\
                       'Weakness: Out of the two names, you do not know '\
                       'Which one is Merlin and which one is "Morgana".'\
                       'Here are your 2 Names:\n'

        self.name = "Persival"
        self.side = "City"


class Merlin():

    def __init__(self):

        self.message = 'Character: Merlin\n' \
                       'Side: City\n'\
                       'Power: You know all the members of evils except for '\
                       'the "Mordered".\n'\
                       'Note: If "Assassins" finds out your identity, '\
                       'he/she can shoot you and the game will be lost for '\
                       'City Side.\n'\
                       'Here are the members of the evil:\n'

        self.name = "Merlin"
        self.side = "City"


class King():
    def __init__(self):

        self.message = 'Character: King Arthor\n'\
                       'Side: City\n'\
                       'Power: If you lose the game in rounds, you '\
                       'have a last chance to gauss the members '\
                       'of the evil at the end of the game. If you '\
                       'gauss "ALL" the names right '\
                       'including but not limited to Oberan and Mordered,'\
                       'You will win the game.\n'\
                       'Note 1: If you win the game by guessing all '\
                       'the names right, '\
                       'Assassin will still have the chance to '\
                       'shoot the "Merlin" and you will lose.\n'\
                       'Note 2: Your identity as "King Aurthor" '\
                       'will be revealed '\
                       'to everyone while you are gussing the names.'

        self.name = "King"
        self.side = "City"


# Mordered Side
class Minion():

    def __init__(self):

        self.message = 'Character: Minion of Mordred\n'\
                       'Side: Evil\n'\
                       'Power: You know all other evils '\
                       '(Except for the Oberon).\n'\
                       'Weakness: "Merlin" knows your identity.\n'\
                       'Here are your teammate(s):\n'
        self.side = "Evil"
        self.name = "Minion"


class Morgana():

    def __init__(self):

        self.Message = 'Character: Morgana\n'\
                       'Side: Evil\n'\
                       'Power Number 1: You know all other Evils '\
                       '(Except for the Oberon).\n'\
                       'Power Number 2: You can confuse '\
                       '"Persival" by acting as "Merlin".\n'\
                       'Weakness: "Merlin" knows your identity.\n'\
                       'Here are your teammate(s):\n'

        self.side = "Evil"
        self.name = "Morgana"


class Assassin():

    def __init__(self):

        self.Message = 'Character: Assassin'\
                       'Side: Evil\n'\
                       'Power Number 1: You know all other Evils '\
                       '(Except for the "Oberon").\n'\
                       'Power Number 2: You can shoot one of the '\
                       'players. If you shoot "Merlin", '\
                       'evil will win the game.\n'\
                       'Weakness: "Merlin" knows your identity.\n'\
                       'Here are your teammate(s):\n'

        self.side = "Evil"
        self.name = "Assassin"


class Oberon():

    def __init__(self):

        self.Message = 'Character: Oberon\n'\
                       'Side: Evil\n'\
                       'Weakness Number 1: You do not know the '\
                       'identity of anyone except for yourself.\n'\
                       'Weakness Number 2: "Merlin" knows your identity.\n'\
                       'Guide: Try to find the other evil(s) and '\
                       'help them win the game.'
        self.side = "Evil"
        self.name = "Oberon"


class Mordred():

    def __init__(self):

        self.Message = 'Character: Mordred\n'\
                       'Side: Evil\n'\
                       'Power Number 1: You know all other Evils '\
                       '(Except for the Oberon).\n'\
                       'Power Number 2: "Merlin" does not '\
                       'know you identity.\n'\
                       'Here are your teammate(s):\n'
        self.side = "Evil"
        self.name = "Mordred"
