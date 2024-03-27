from types import SimpleNamespace
from emoji import emojize

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

Char_Texts = SimpleNamespace(

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

Texts = SimpleNamespace(

    CG="The game was created."
    "\nAsk your friends to join the game."
    "\nYour name in the game is: ",
    YN="Your name in the game is: ",
    RFG=" was removed from the game.",
    ATG=" was add to the game.",
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
    PCE="There are too many characters.",
    PNE="Not Enough players, there should be atleast 5 players.",
    YR="We are preparing roles for you ...",
    CO="Commander's order:",
    CCN1="You are the commander in this round.",
    CCN2_1="You should pick ",
    CCN2_2=" players.",
    TGHS="The game has already started.",
    SFV="Your vote has been received.",
    PCC='Proposed committee by commander:',
    FCC='Final committee by commander:',
    CV="Your vote: ",
    CM='Choose between "Fail" and "Success".',
    RFC=" was removed from the committee.",
    ATC=" was add to the committee.",
    YVB=":slightly_smiling_face: you have voted before",
    EW="Evil Won.",
    REW1="\nReason: The Committee was rejected 5 times in a row.",
    REW2="\nReason: Assassin Shooted the Merlin.",
    REW3="\nReason: Evil won three rounds.",
    CW3R="City won 3 rounds, it's time for assassin to shoot.",
    CW="City Won.",
    RCW="\nReason: Assassin guessed the wrong person as Merlin.",
    ASS1="Who do you want to shoot?",
    ASS2_1="You chose ",
    ASS2_2=" as the Merlin.",
    ASSE_3="You should choose someone !!",
)
