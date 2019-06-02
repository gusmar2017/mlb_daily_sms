from datautils.alerter import send_sms

from datautils.game_details import get_game_details


def next_game_alert_setup(game,user):
    """
    provides the final message that will go out via twilia
    input:
        game_details: dictionary
        user: dictionary of user information
        int_both: boolean flag for when both teams are interest teams
    """
    if game['home_team']['interest_team'] or (game['home_team']['interest_team'] and\
        game['away_team']['interest_team']):

        team = game['home_team']
        opponent = game['away_team']
    else:
        team = game['away_team']
        opponent = game['home_team']

    intro_msg = set_intro_msg(game,opponent,team)

    pp_notes = user['Pitcher_Notes']
    if pp_notes == 'True':
        pp_notes = True
    else:
        pp_notes = False
    start_msgs = set_probable_starter_msg(game,opponent,team,pp_notes)

    message = intro_msg + start_msgs['team_pitcher'] +\
        start_msgs['opp_pitcher']

    return message


def set_intro_msg(game_details,opponent,team):
    # where opponent and team will be the team details
    team_dir = team['HomeAway']
    intro_msg = """The %s (%s-%s) will be %s to%s against the %s (%s-%s): %s:%s at %s. """ %\
        (team['name'],
            team['wins'],
            team['losses'],
            team_dir,
            game_details['dayNight'],
            opponent['name'],
            opponent['wins'],
            opponent['losses'],
            game_details['gametime'].hour,
            game_details['gametime'].minute,
            game_details['venue']
        )

    return intro_msg


def set_probable_starter_msg(game_details,opponent,team,notes_bool):
    probablePitcher_msg = {
        'opp_pitcher':'',
        'team_pitcher':''
    }

    if opponent['probable_pitcher']:
        probablePitcher_msg['opp_pitcher'] = """The %s have %s on the hill""" %\
            (opponent['name'],
            opponent['probable_pitcher']
            )
        if notes_bool:
            probablePitcher_msg['opp_pitcher'] += ": %s" % (opponent['pitcher_notes'])
        else:
            probablePitcher_msg['opp_pitcher'] += "."

    if team['probable_pitcher']:
        probablePitcher_msg['team_pitcher'] = """The %s will throw %s""" %\
            (team['name'],
            team['probable_pitcher'])

        if notes_bool:
            probablePitcher_msg['team_pitcher'] += ": %s" % (team['pitcher_notes'])
        else:
            probablePitcher_msg['team_pitcher'] += "."

    return probablePitcher_msg


def create_all_msgs(user_data,all_games):
    msg = {}
    for user in user_data:
        team_list = user_data[user]['team_details']
        msg[user] = []
        for game in all_games:
            game_details = get_game_details(game,team_list)

            if game_details:
                if game_details['home_team']['interest_team'] or\
                    game_details['away_team']['interest_team']:

                    msg[user].append(
                        next_game_alert_setup(game_details,user_data[user])
                    )
            else:
                msg[user].append()

    return msg
