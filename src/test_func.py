import json

def character_vote(mission_characters):

    vote = []

    for character in mission_characters:

        current_vote = 0 if character.side == "Evil" else 1
        vote.append(current_vote)

    return vote
