#import sys
#sys.path.append("/users/gustavomarquez/Desktop/rays_updates")

import statsapi
from datetime import datetime,timedelta

from datautils.team_details import _extract_aggregate_teampk

from datautils.datetime_help import _convert_timestamp_datetime,\
                                    _convert_datestr_datetime,\
                                    _convert_to_est

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# This will hold all of the tools needed to extract game details
#   from any stack of games. We particularly want to handle the
#   ability to do multiple games at one retreival and send  a text
#   out.
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


def get_teams_games(user_data,days_back=15):
    """
    Returns a list of games for the past 15 days
    """
    # hits the endpoint for game today
    params = {'startDate':(_convert_to_est(datetime.now()) -\
                            timedelta(days=days_back)
                            ).strftime('%Y-%m-%d'),
                'endDate':_convert_to_est(datetime.now()).strftime('%Y-%m-%d'),
                'teamId':_extract_aggregate_teampk(),
                'sportId':'1',
                'hydrate':'probablePitcher(note)'
                }
    game_obj = statsapi.get('schedule',params)

    games = _convert_game_obj(game_obj['dates'],user_data)

    return games


def get_game_details(game,user_data):
    game_details = {
        'gamePk':game['gamePk'],
        'gametime':_convert_timestamp_datetime(game['gameDate']),
        'gametype':game['gameType'],
        'venue':game['venue']['name'],
        'status':game['status']['detailedState'],
        'doubleHeader':game['doubleHeader'],
        'dayNight':game['dayNight'],
        'seriesGameNumber':game['seriesGameNumber'],
        'gamesInSeries':game['gamesInSeries'],
    }

    game_details['home_team'] =\
        get_game_team_data(game,'home',user_data,game_details['status'])
    game_details['away_team'] =\
        get_game_team_data(game,'away',user_data,game_details['status'])

    return game_details


def get_game_team_data(game,team_dir,user_data,status):
    """
    extract some of the team data depending on team directions
    Output:
        below dictionary data_points
    Input:
        game: game dictionary
        team_dir: 'away' or 'home' flag
    """
    details = game['teams'][team_dir]
    data_points = {
        'id':details['team']['id'],
        'name':details['team']['name'],
        'wins':details['leagueRecord']['wins'],
        'losses':details['leagueRecord']['losses'],
        'games_played': details['leagueRecord']['wins'] +\
            details['leagueRecord']['losses'],
        'HomeAway':team_dir
    }

    # handles issues when probable pitcher missing
    data_points.update(_check_probable_pitcher(details))

    data_points['users_interested'] = _interested_users(data_points['id'],
                                        user_data)

    #check to capture specific information if game is final
    if status == 'Final':
        data_points['score'] = details['score']
        data_points['isWinner'] = details['isWinner']

    return data_points


def get_today_yesterday_games(games,
                            yesterday=(datetime.now() -\
                                timedelta(days=1)
                                ).date(),
                            today_dt = datetime.now().date()):
    return_dict = {}
    for date in games:
        if _convert_datestr_datetime(date) == today_dt:
            return_dict['today'] = games[date]
        elif _convert_datestr_datetime(date) == yesterday:
            return_dict['yesterday'] = games[date]

    return return_dict


def _convert_game_obj(game_obj,user_data):
    final_obj = {}
    for dates in game_obj:
        final_obj[dates['date']] = []
        #print(dates['date'])
        for gam in dates['games']:
            #print(gam['gamePk'])
            final_obj[dates['date']].append(get_game_details(gam,user_data))

    return final_obj


def _check_probable_pitcher(details):
    data_points = {}
    #check to make sure there was a probable pitcher
    try:
        data_points['probable_pitcher'] = _parse_pitcher_fullname(
                            details['probablePitcher']['fullName'])
    except:
        data_points['probable_pitcher'] = ''

    # check to make sure there are notes
    try:
        data_points['pitcher_notes'] = details['probablePitcher']['note']
    except:
        data_points['pitcher_notes'] = ''

    return data_points


def _interested_users(teampk,user_data):
    users = []
    for user in user_data:
        for team in user_data[user]['team_details']:
            if team['id'] == teampk:
                users.append(user)

    return users


def _parse_pitcher_fullname(fullname):
    name_lst = fullname.split(', ')
    name = "%s %s" % (name_lst[1],name_lst[0])

    return name


def _create_team_opponent(game,user):
    dict_returned = {}
    if user not in game['home_team']['users_interested'] and\
        user not in game['away_team']['users_interested']:
        return False

    elif user in game['home_team']['users_interested'] or\
        (user in game['home_team']['users_interested'] and\
        user in game['away_team']['users_interested']):

        dict_returned['team'] = game['home_team']
        dict_returned['opponent'] = game['away_team']
    else:
        dict_returned['team'] = game['away_team']
        dict_returned['opponent'] = game['home_team']

    return dict_returned
