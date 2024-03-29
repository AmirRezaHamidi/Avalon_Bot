from types import SimpleNamespace
from emoji import emojize
import os

current_working_directory = os.getcwd()
Directories = SimpleNamespace(

    Token=f"{current_working_directory}\\src\\Data\\Bot_Token.txt",
    CGW=f"{current_working_directory}\\src\\Data\\creating_game_word.txt",
    TGW=f"{current_working_directory}\\src\\Data\\terminating_game_word.txt",
)

Keys = SimpleNamespace(

    start_game=emojize(':check_mark_button: Start Game'),
    join_game=emojize(':plus: Join the Game'),
    choose_character=emojize(':performing_arts: Lets choose characters'),
    finished_choosing=emojize(':check_mark_button: Finished Choosing'),
    propose=emojize(':loudspeaker: Propose'),
    final=emojize(':hundred_points: Final Decision'),
    success=emojize(':green_circle: Success'),
    fail=emojize(':red_circle: Fail'),
    check_box=emojize(':check_box_with_check:'),
    agree=emojize(':thumbs_up:Agree'),
    disagree=emojize(':thumbs_down: Disagree'),
    assassin_shoots=emojize(':water_pistol: Shoot'),
    accept=emojize(":check_mark_button: Accept"),
    declined=emojize(":prohibited: Declined"),
    natural=emojize(":white_small_square:"),
    evil_win=emojize(":red_square:"),
    city_win=(emojize(":green_square:"))
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
    mafia="Mafia",
    morgana="Morgana",
    assassin="Assassin",
    oberon='Oberon',
    mordred='Mordred',
    lady="Lady",
    persival_morgana='Persival/Morgana',
)

CharM_T = SimpleNamespace(

    khiar='You are a "Khiar".',
    persival='You are the "Persival".\nMerlin and Morgana: \n\n\n',
    merlin='You are the "Merlin".\nMafia Team: \n\n\n',
    mafia='You are a "Mafia-e-Mamooli".\nMafia Team: \n\n\n',
    morgana='You are the "Morgana".\nMafia Team: \n\n\n',
    assassin='You are the "Assassin".\nMafia Team: \n\n\n',
    mordred='You are the "Moredred".\nMafia Team: \n\n\n',
    oberon='You are the "Oberon"'
)

Err_T = SimpleNamespace(

    PCE="There are too many characters.",
    PNE="Not Enough players, there should be atleast 5 players.",
)

GaS_T = SimpleNamespace(

    CG="The game was created."
    "\nAsk your friends to join the game."
    "\nYour name in the game is: ",
    YN="Your name in the game is: ",
    GOG="A game already exists."
    "\nFind it using the search command.",
    NGET="No game exists.",
    TGT="The game was terminated.",
    SFG="Searching ...",
    NGSC="No game exist. Try again ...",
    GOSC="A game is ongoing. Try again later ...",
    YAJ="you have already joined the game.",
    GESC="A game already exists and you can join it.",
    YJGS="You have joined the game sucessfuly.",
    GAJG=" has joined the game.",
    TGHS="The game has already started.",
    RFG=" was removed from the game.",
    ATG=" was add to the game.",
)


Co_T = SimpleNamespace(

    CO="Commander's order:",
    CCN1="You are the commander in this round.",
    CCN2_1="You should pick ",
    CCN2_2=" players.",
    ATC=" was add to the committee.",
    RFC=" was removed from the committee.",
    PCC='Proposed committee by commander:',
    FCC='Final committee by commander:',
)

GaSi_T = SimpleNamespace(

    CW3R="City won 3 rounds, it's time for assassin to shoot.",
    RCW="\nReason: Assassin guessed the wrong person as Merlin.",
    CW="City Won.",
    REW1="\nReason: The Committee was rejected 5 times in a row.",
    REW2="\nReason: Assassin Shooted the Merlin.",
    REW3="\nReason: Evil won three rounds.",
    EW="Evil Won.",
)

Oth_T = SimpleNamespace(

    YR="We are preparing roles for you ...",
    SFV="Your vote has been received.",
    CV="Your vote: ",
    MV='Choose between "Fail" and "Success".',
    YVB=":slightly_smiling_face: you have voted before",
    CNF="Not Valid !!!"
)

Ass_T = SimpleNamespace(

    ASS1="Who do you want to shoot?",
    ASS2_1="You chose ",
    ASS2_2=" as the Merlin.",
    ASSE_3="You should choose someone !!",
)
