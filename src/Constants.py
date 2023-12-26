from types import SimpleNamespace
from emoji import emojize


keys = SimpleNamespace(

    accept = emojize(":check_mark_button: Accept"),
    decline = emojize(":cross_mark: Decline"),
    bot_status=emojize(':white_exclamation_mark: Bot Status'),
    i_am_admin=emojize(':smiling_face_with_sunglasses: I Am an Admin'),
    new_game=emojize(':plus: Creat a new Game'),
    join_game=emojize(':plus: Joing the game'),
    choose_character=emojize(':performing_arts: Lets choose characters'),
    Persival_Morgana='Persival_Morgana',
    King='King Arthur',
    Mordred='Mordred',
    Oberon='Oberon',
    finished_choosing=emojize(':check_mark_button: Finished Choosing'),
    fail=emojize(':red_circle: Fail'),
    success=emojize(':green_circle: success'),
    propose=emojize(':loudspeaker: Propose'),
    final=emojize(':hundred_points: Final Decision'),
    check_box=emojize(':check_box_with_check:'),
    agree=emojize(':thumbs_up:Agree'),
    disagree=emojize(':thumbs_down: Disagree'),
    assassin_shoots=emojize(':gun: Shoot'),
    kings_guess=emojize(':dice:Guess')
)

States = SimpleNamespace(
    no_game='no_game',
    starting='starting',
    ongoing='ongoing',
    choose_characters='choose_characters',
    committee_choose='committee_choose',
    committee_voting='committee_voting',
    mission_voting='mission_voting',
    kings_guess='king_guess',
    assassin_shoots='assassin_shoots'
)
