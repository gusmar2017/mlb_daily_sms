from datautils.alerter import send_sms

from datautils.game_details import get_today_yesterday_games,\
                                    _create_team_opponent

from datautils.datetime_help import _gametime_message_handler

def previous_game_msg(game,team_opponent):
    if team_opponent['team']['isWinner']:
        msg = 'Yesterday, the %s beat the %s %s to %s.'\
            % (team_opponent['team']['name'],
                team_opponent['opponent']['name'],
                team_opponent['team']['score'],
                team_opponent['opponent']['score'])
    else:
        msg = 'Yesterday, the %s lost to the %s %s to %s.'\
            % (team_opponent['team']['name'],
                team_opponent['opponent']['name'],
                team_opponent['team']['score'],
                team_opponent['opponent']['score'])

    return msg


def next_game_alert_setup(game,user_data,team_opponent):
    """
    provides the final message that will go out via twilia
    input:
        game_details: dictionary
        user: dictionary of user information
        int_both: boolean flag for when both teams are interest teams
    """
    intro_msg = set_intro_msg(game,team_opponent)

    starter_msg = set_probable_starter_msg(game,
                            team_opponent,
                            user_data['Pitcher_Notes'])

    msg = intro_msg + starter_msg['team_pitcher'] +\
        starter_msg['opp_pitcher']

    return msg


def set_intro_msg(game_details,team_opponent):
    # where opponent and team will be the team details
    team_dir = team_opponent['team']['HomeAway']
    intro_msg = """ Today, the %s (%s-%s) will be %s to%s against the %s (%s-%s): %s at %s. """ %\
        (team_opponent['team']['name'],
            team_opponent['team']['wins'],
            team_opponent['team']['losses'],
            team_opponent['team']['HomeAway'],
            game_details['dayNight'],
            team_opponent['opponent']['name'],
            team_opponent['opponent']['wins'],
            team_opponent['opponent']['losses'],
            _gametime_message_handler(game_details['gametime']),
            game_details['venue']
        )

    return intro_msg


def set_probable_starter_msg(game_details,team_opponent,notes_bool):
    probablePitcher_msg = {
        'opp_pitcher':'',
        'team_pitcher':''
    }

    if team_opponent['opponent']['probable_pitcher']:
        probablePitcher_msg['opp_pitcher'] = """The %s have %s on the hill""" %\
            (team_opponent['opponent']['name'],
            team_opponent['opponent']['probable_pitcher']
            )
        if notes_bool:
            probablePitcher_msg['opp_pitcher'] += ": %s" %\
                (team_opponent['opponent']['pitcher_notes'])
        else:
            probablePitcher_msg['opp_pitcher'] += "."

    if team_opponent['team']['probable_pitcher']:
        probablePitcher_msg['team_pitcher'] = """The %s will throw %s""" %\
            (team_opponent['team']['name'],
            team_opponent['team']['probable_pitcher'])

        if notes_bool:
            probablePitcher_msg['team_pitcher'] += ": %s" %\
                (team_opponent['team']['pitcher_notes'])
        else:
            probablePitcher_msg['team_pitcher'] += "."

    return probablePitcher_msg


def create_all_msgs(user_data,all_games):
    msg = {}
    games = get_today_yesterday_games(all_games)

    for user in user_data:
        team_list = user_data[user]['team_details']
        msg[user] = {}
        if games:
            for item in games:
                if games[item]:
                    for game in games[item]:
                        team_opponent = _create_team_opponent(game,user)
                        if team_opponent:
                            if item == 'yesterday':
                                if user_data[user]['Previous_game']:
                                    msg[user].update(
                                            {item:previous_game_msg(game,
                                                        team_opponent)})
                            elif item =='today':
                                msg[user].update(
                                        {item:\
                                        next_game_alert_setup(game,
                                                        user_data[user],
                                                        team_opponent)})

    return_msg = final_msg(msg)

    return return_msg


def final_msg(msg):
    msg_final = {}
    for user in msg:
        msg_final[user] = ''
        for dt in msg[user]:
            msg_final[user] += msg[user][dt]

    return msg_final
