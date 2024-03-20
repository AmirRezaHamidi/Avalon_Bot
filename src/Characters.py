# Arthur Side
class Servant():

    def __init__(self):
        self.message = 'Character: Loyal Servant of Arthur\n'\
                       'Side: City\n'\
                       'Weakness: You do not know the identity of anyone '\
                       'except for yourself.\n'\
                       'Guide: Try to finds the "Merlin" and and help him/her'\
                       ' win the game.'

        self.name = "Servant"
        self.side = "City"
        self.has_info = False


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
        self.has_info = True


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
        self.has_info = True


# Mordered Side
class Minion():

    def __init__(self):

        self.message = 'Character: Minion of Mordred\n'\
                       'Side: Evil\n'\
                       'Power: You know all other evils '\
                       '(Except for the Oberon).\n'\
                       'Weakness: "Merlin" knows your identity.\n'\
                       'Here are your teammate(s) inlcuding you:\n'

        self.name = "Minion"
        self.side = "Evil"
        self.has_info = True


class Morgana():

    def __init__(self):

        self.message = 'Character: Morgana\n'\
                       'Side: Evil\n'\
                       'Power Number 1: You know all other Evils '\
                       '(Except for the Oberon).\n'\
                       'Power Number 2: You can confuse '\
                       '"Persival" by acting as "Merlin".\n'\
                       'Weakness: "Merlin" knows your identity.\n'\
                       'Here are your teammate(s) inlcuding you:\n'

        self.name = "Morgana"
        self.side = "Evil"
        self.has_info = True


class Assassin():

    def __init__(self):

        self.message = 'Character: Assassin\n'\
                       'Side: Evil\n'\
                       'Power Number 1: You know all other Evils '\
                       '(Except for the "Oberon").\n'\
                       'Power Number 2: You can shoot one of the '\
                       'players. If you shoot "Merlin", '\
                       'evil will win the game.\n'\
                       'Weakness: "Merlin" knows your identity.\n'\
                       'Here are your teammate(s) inlcuding you:\n'

        self.name = "Assassin"
        self.side = "Evil"
        self.has_info = True


class Oberon():

    def __init__(self):

        self.message = 'Character: Oberon\n'\
                       'Side: Evil\n'\
                       'Weakness Number 1: You do not know the '\
                       'identity of anyone except for yourself.\n'\
                       'Weakness Number 2: "Merlin" knows your identity.\n'\
                       'Guide: Try to find the other evil(s) and '\
                       'help them win the game.'

        self.name = "Oberon"
        self.side = "Evil"
        self.has_info = False

class Mordred():

    def __init__(self):

        self.message = 'Character: Mordred\n'\
                       'Side: Evil\n'\
                       'Power Number 1: You know all other Evils '\
                       '(Except for the Oberon).\n'\
                       'Power Number 2: "Merlin" does not '\
                       'know you identity.\n'\
                       'Here are your teammate(s) inlcuding you:\n'

        self.name = "Mordred"
        self.side = "Evil"
        self.has_info = True
