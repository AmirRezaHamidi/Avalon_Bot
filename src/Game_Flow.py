from Engines import Avalon_Engine
import random
from test_func import character_vote

# Should be received from the bot
names = ["Fateme", "ali", "hasan", "hossein", "sajad", "bagher", "sadegh",
         "jafar", 'reza']
prefered_characters = ["Mordred", "King", "Oberon"]
# Should be received from the bot

# Night Phase
Game = Avalon_Engine(names, prefered_characters=prefered_characters)


while Game.continues:

    while True:

        # Should be received from the bot
        current_round = Game.round
        n_committee = Game.all_round(current_round)
        random.shuffle(names)
        committee_names = names[0:n_committee]
        # Should be received from the bot

        Game.check_committee(committee_names)

        if Game.acceptable_round:

            Game.acceptable_round = False
            break

        else:

            # Should be sent to bot
            Message = f"You should pick exactly {n_committee} person for this round."
            # Should be sent to bot

        # Should be received from the bot
        committee_votes = [random.randint(0, 1) for _ in names]
        # Should be received from the bot

        Game.count_committee_vote(committee_votes=committee_votes)

        if Game.committee_accept:
            
            # Should be sent to bot
            Messsage = f"please choose between Fail and Success"
            # Should be sent to bot

            # Should be received from the bot
            mission_characters = []

            for name in committee_names:
                mission_characters.append(Game.assigned_characters[name])
            
            mission_votes = character_vote(mission_characters)
            # Should be received from the bot

            Game.mission_result(mission_votes=mission_votes)
    
    if Game.evil_wins == 3 or Game.city_wins == 3:

        Game.continues = False 

if "king" in Game.string_character:

    if Game.evil_wins == 3:

        # Should be received from the bot
        n_evils = len(Game.all_info["King"])
        random.shuffle(names)
        guesses = names[0:n_evils]
        # Should be received from the bot

        Game.king_guess(guesses)
            
        if not Game.king_guessed_right:

            Game.win_side = "Evil"

        elif Game.king_guessed_right:

            # Should be received from the bot
            random.shuffle(names)
            shooted_name = names[0]
            # Should be received from the bot

            Game.assassin_shoot(shooted_name)

            if Game.assassin_shooted_right:

                Game.win_side = "Evil"

            else:

                Game.win_side = "City"

    elif Game.city_wins == 3:

        # Should be received from the bot
        random.shuffle(names)
        shooted_name = names[0]
        # Should be received from the bot

        Game.assassin_shoot(shooted_name)

        if Game.assassin_shooted_right:

            Game.win_side = "Evil"

        else:
            Game.win_side = "City"
    
else:

    if Game.evil_wins == 3:

        Game.win_side = "evil"

    elif Game.city_wins == 3:

        # Should be received from the bot
        random.shuffle(names)
        shooted_name = names[0]
        # Should be received from the bot

        Game.assassin_shoot(shooted_name)

        if Game.assassin_shooted_right:

            Game.win_side = "Evil"

        else:
            Game.win_side = "City"