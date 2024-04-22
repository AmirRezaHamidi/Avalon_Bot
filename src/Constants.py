from types import SimpleNamespace
from emoji import emojize
import os

current_working_directory = os.getcwd()
Directories = SimpleNamespace(

    Token=f"{current_working_directory}\\src\\Data\\Bot_Token.txt",
)

Commands = SimpleNamespace(

    start="start",
    creategame="creategame",
    searchgame="searchgame",
    uselady="uselady",
    assassinshoot="assassinshoot"
)

Keys = SimpleNamespace(

    create_game=emojize(':plus: Create Game'),

    join_game=emojize(':plus: Join Game'),

    start_game=emojize(':check_mark_button: Start Game'),

    choose_character=emojize(':performing_arts: Lets choose characters'),

    finished_choosing=emojize(':check_mark_button: Finished Choosing'),

    final=emojize(':hundred_points: Final Decision'),

    success=emojize(':green_square: Success'),

    fail=emojize(':red_square: Fail'),

    check_box=emojize(':check_box_with_check:'),

    agree=emojize(':thumbs_up:Agree'),

    disagree=emojize(':thumbs_down: Disagree'),

    assassin_shoots=emojize(':water_pistol: Shoot'),

    accept=emojize(":check_mark_button: Accept"),

    declined=emojize(":prohibited: Declined"),

    evil_win=emojize(":red_circle:"),

    city_win=emojize(":green_circle:"),
)

States = SimpleNamespace(

    no_game='no_game',

    created='created',

    started='started'
)

Sub_States = SimpleNamespace(

    character_choosing='character_choosing',

    committee_choosing='committee_choosing',

    committee_voting='committee_voting',

    mission_voting='mission_voting',

    assassin_shooting='assassin_shooting',

    assassin_shooted="assassin_shooted"
)

Char_T = SimpleNamespace(

    city_side="City",

    evil_side="Evil",

    khiar="Khiar",

    persival="Persival",

    merlin="Merlin",

    mafia="Mafia-e-Mamooli",

    morgana="Morgana",

    assassin="Assassin",

    oberon='Oberon',

    mordred='Mordred',

    lady="Lady",

    persival_morgana='Persival/Morgana',
)

GaS_T = SimpleNamespace(

    SC=("Welcome. Create a new game or join an already existed game."),

    CG="The game was created."
       "\nAsk your friends to join the game."
       "\nYour name in the game is: ",

    PSF="\n\nPlayers in Game: \n\n",

    YN="Your name in the game is: ",

    GOG="A game already exists."
        "\nJoin it using the join button.",

    CHC="Choose you prefered character in the game.",

    SFG="Searching ...",

    NGSC="No Game exist. Creat one first.",

    GESC="1 Game found.",

    GIOG="Game has already started. Join the next round",

    YSCG="You should create a game first ",

    GOSC="A game is ongoing. Try again later ...",

    YAJ="you have already joined the game.",

    YJGS="You have joined the game sucessfuly.",

    GAJG=" has joined the game.",

    TGHS="The game has already started.",

    RFG=" was removed from the game.",

    ATG=" was add to the game.",

    IGI="Game Information:",

    YR="Your Role:",

    PINF="Players info:",

    NOM="Number of Evils:",

    CIG="Characters in the game:",

    big_sep="-" * 45,

    small_sep="-" * 15,
)

CharM_T = SimpleNamespace(

    khiar=f'You are a {Char_T.khiar}.',

    persival=(f'You are the {Char_T.persival}.'
              f'\n{GaS_T.small_sep}'
              f'\n{Char_T.persival} Information:'),

    merlin=(f'You are the {Char_T.merlin}.'
            f'\n{GaS_T.small_sep}'
            f'\n{Char_T.merlin} Information:'),

    mafia=(f'You are a {Char_T.mafia}.'
           f'\n{GaS_T.small_sep}'
           f'\n{Char_T.mafia} Information:'),

    morgana=(f'You are the "{Char_T.morgana}.'
             f'\n{GaS_T.small_sep}'
             f'\n{Char_T.morgana} Information:'),

    assassin=(f'You are the {Char_T.assassin}.'
              f'\n{GaS_T.small_sep}'
              f'\n{Char_T.assassin} Information:'),

    mordred=(f'You are the {Char_T.mordred}.'
             f'\n{GaS_T.small_sep}'
             f'\n{Char_T.mordred} Information:'),

    oberon=f'You are the {Char_T.oberon}.'
)

Err_T = SimpleNamespace(

    PCE="There are too many characters.",

    PNEL="Not Enough players, there should be atleast 5 players.",

    PNEH="Too many Players. The maximum number of players is 10."
)

Co_T = SimpleNamespace(

    CO="Commander's order:",

    CCN1="You are the commander in this round.",

    CCN2_1="You should pick ",
    CCN2_2=" players.",

    ATC=" was add to the committee.",

    RFC=" was removed from the committee.",

    PCC='Proposed committee by commander:',
)

GaSi_T = SimpleNamespace(

    CW3R="City won 3 rounds, it's time for assassin to shoot.",
    CW="City Won.",
    RCW="\nReason: Assassin guessed the wrong person as Merlin.",

    EW="Evil Won.",
    REW1="\nReason: The Committee was rejected 5 times in a row.",
    REW2="\nReason: Assassin Shooted the Merlin.",
    REW3="\nReason: Evil won three rounds.",
)

Vote_T = SimpleNamespace(

    SFV="Your vote has been received.",

    CV="Your vote: ",

    MV='Choose between "Fail" and "Success".',

    YVB=":slightly_smiling_face: you have voted before",
    PTV="Remaining voters \n"
)

Ass_T = SimpleNamespace(

    ASS1="Who do you want to shoot?",

    ASS2_1="You chose ",
    ASS2_2=" as the Merlin.",

    ASS3="You should choose someone !!",
)

Summ_T = SimpleNamespace(

    CCIG="City Characters",
    ECIG="Evil Characters"
)

Oth_T = SimpleNamespace(

    TA="Please Try again ...",
    NAVC="Not a valid command."
)

Panel_Keys = SimpleNamespace(

    game_info=emojize(":performing_arts: Game Information"),
    commander_order=emojize(":fleur-de-lis: commander's order"),
    assassin_shoot=emojize(":water_pistol: Assassin Shoot"),
    lady=emojize(":woman_elf: Lady Token"),
    Cancle=":cross_mark: Cancle"
)

PanelM_T = SimpleNamespace(

    RHNRY="Round has not reached yet !!",
    NCHBCY="No committee has been created yet !!",
    LC="This is the last committee yet !!",
    FC="This is the first committee !!",
    AR="Already Requested",
    ASE="NOT Allowed",
    CS="Comming Soon ... "
)
