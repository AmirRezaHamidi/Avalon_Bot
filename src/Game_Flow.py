from Engines import Avalon_Engine
import random
from test_func import character_vote

# Should be received from the bot
names = ["Fateme", "ali", "hasan", "hossein", "sajad", "bagher", "sadegh",
         "jafar", "reza"]
optional_characters = ["Mordred", "King"]
# Should be received from the bot

# Night Phase
Game = Avalon_Engine(names, optional_characters=optional_characters)

# should send the information to players
# should send the information to players

while Game.continues:

    while True:

        # Should be received from the bot

        n_committee = Game.all_round[Game.round]
        random.shuffle(names)
        committee_names = names[0:n_committee]
        # Should be received from the bot

        Game.check_committee(committee_names)

        if Game.acceptable_round:

            Game.acceptable_round = False
            break

        else:
            # Should be sent to bot
            Message = f"You should pick exactly {n_committee} person "\
                       "for this round."
            # Should be sent to bot

    # Should be received from the bot
    committee_votes = random.choices([0, 1], weights=[20, 80], k=len(names))
    # Should be received from the bot
    print('-' * 15)
    print("Committee Votes")
    print('-' * 15)
    # should be sent to bot
    for i, name in enumerate(names):
        print("Positive" if committee_votes[i] == 1 else "negative",  name)
    print('-' * 15)
    # should be sent to bot
    Game.count_committee_vote(committee_votes=committee_votes)

    if Game.committee_accept:

        # Should be sent to bot
        Messsage = "please choose between Fail and Success"
        # Should be sent to bot

        # Should be received from the bot
        mission_characters = []

        for name in committee_names:
            mission_characters.append(Game.assigned_character[name])

        mission_votes = character_vote(mission_characters)
        random.shuffle(mission_votes)
        # Should be received from the bot

        # Should sent the mission vote result
        Game.mission_result(mission_votes=mission_votes)
        Game.round += 1
        message = f"you have {Game.fail_count} "\
                  f"fail votes and {Game.success_count} success votes"
        # Should sent the mission vote result

    else:

        if Game.reject_count == 5:

            Game.continues = False
            Game.win_side = "Evil"

    if Game.evil_wins == 3 or Game.city_wins == 3:

        Game.continues = False

if "King" in Game.string_character:

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

        Game.win_side = "Evil"

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
