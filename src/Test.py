from Characters import Servant, Persival, Merlin, King, Minion, Morgana, Assassin, Oberon, Mordred
# from Engine import Game_Engine
import random

from Engine import Game_Engine

names = ["Fateme", "ali", "hasan", "hossein", "sajad", "bagher", "sadegh", "jafar", 'reza']
prefered_characters = ["King Arthur"]


new_game = Game_Engine(names, prefered_characters=prefered_characters )
for item in new_game.assigned_character.items():

    print(item)