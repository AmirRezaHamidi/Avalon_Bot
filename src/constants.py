from types import SimpleNamespace
from emoji import emojize


keys = SimpleNamespace(
    bot_status=emojize(':white_exclamation_mark:Bot Status'
                       ':white_exclamation_mark:'),
    i_am_admin=emojize(':smiling_face_with_sunglasses:I Am an Admin'),
    new_game=emojize(':plus: Creat a new Game'),
    join_game=emojize(':plus: Joing the game'),
    start=emojize(":check_mark_button:START"),
    terminate=emojize(":cross_mark:TERMINATE"),
    Persival_Morgana="Persival_Morgana",
    King="King Arthur",
    Mordred="Mordred",
    Oberon="Oberon",
    full_Persival_Morgana=emojize(":check_box_with_check:Persival_Morgana"),
    full_King=emojize(":check_box_with_check:King Arthur"),
    full_Mordred=emojize(":check_box_with_check:Mordred"),
    full_Oberon=emojize(":check_box_with_check:Oberon"),
    finished_choosing=emojize(":check_mark_button:Finished Choosing"),
    fail = emojize(":red_circle:Fail"),
    success = emojize(":green_circle:success"),
    propose = emojize(":loudspeaker:Propose"),
    final_decision = emojize(":hundred_points:Final Decision")
)
