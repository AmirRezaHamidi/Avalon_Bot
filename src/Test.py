from Characters import Servant, Persival, Merlin, King, Minion, Morgana, Oberon, Mordred
# from Engine import Game_Engine

from Engines import Game_Engine

names = ["Fateme", "ali", "hasan", "hossein", "sajad", "bagher", "sadegh",
         "jafar", 'reza']
prefered_characters = ["Mordred", "King", "Oberon"]


new_game = Game_Engine(names, prefered_characters=prefered_characters)
print("\n")
for item in new_game.assigned_character.items():

    print(item)
print("\n")
for item in new_game.all_info.items():
    print(item)
print("\n")