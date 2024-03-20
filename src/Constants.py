from types import SimpleNamespace
from emoji import emojize

keys = SimpleNamespace(

    start_game=emojize(':check_mark_button: Start Game'), 
    join_game=emojize(':plus: Joing the game'),
    choose_character=emojize(':performing_arts: Lets choose characters'),
    persival_morgana='Persival_Morgana',
    king='King Arthur',
    mordred='Mordred',
    oberon='Oberon',
    finished_choosing=emojize(':check_mark_button: Finished Choosing'),
    success=emojize(':green_circle: success'),
    fail=emojize(':red_circle: Fail'),
    propose=emojize(':loudspeaker: Propose'),
    final=emojize(':hundred_points: Final Decision'),
    check_box=emojize(':check_box_with_check:'),
    agree=emojize(':thumbs_up:Agree'),
    disagree=emojize(':thumbs_down: Disagree'),
    assassin_shoots=emojize(':water_pistol: Shoot'),
    kings_guess=emojize(':dice: Guess')
)

States = SimpleNamespace(
    no_game='no_game',
    starting='starting',
    ongoing='ongoing'
)

Sub_States = SimpleNamespace(
    character_choosing='character_choosing',
    committee_choose='committee_choose',
    committee_voting='committee_voting',
    mission_voting='mission_voting',
    kings_guessing='kings_guessing',
    assassin_shooting='assassin_shooting',
    assassin_shooted = "assassin_shooted"
)
