#import sys
#sys.path.append("/users/gustavomarquez/Desktop/rays_updates")

import statsapi
from datetime import datetime

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


def get_teams_games_today():
    """
    Returns a list of games
    """
    # hits the endpoint for game today
    params = {'date':datetime.now().strftime('%Y-%m-%d'),
                'teamId':_extract_aggregate_teampk(),
                'sportId':'1',
                'hydrate':'probablePitcher(note)'
                }
    game_obj = statsapi.get(
        'schedule',params)

    return game_obj['dates'][0]['games']


def get_game_details(game,user_team_list):
    game_details = {
        'gamePk':game['gamePk'],
        'gametime':_convert_timestamp_datetime(game['gameDate']),
        'venue':game['venue']['name'],
        'doubleHeader':game['doubleHeader'],
        'dayNight':game['dayNight'],
        'seriesGameNumber':game['seriesGameNumber'],
        'gamesInSeries':game['gamesInSeries'],
        'home_team':get_game_team_data(game,'home',user_team_list),
        'away_team':get_game_team_data(game,'away',user_team_list)
    }

    return game_details


def get_game_team_data(game,team_dir,user_team_list):
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
        'HomeAway':team_dir,
        'probable_pitcher':_parse_pitcher_fullname(
                            details['probablePitcher']['fullName']),
        'pitcher_notes':_check_probable_pitcher_note(
                            details['probablePitcher'])
    }

    data_points['interest_team'] = _check_interested_team(data_points['id'],
                                        user_team_list)

    return data_points


def _check_probable_pitcher_note(pp_details):
    try:
        return pp_details['note']
    except:
        return '.'


def _check_interested_team(teampk,user_team_list):
    interest_teampk_list = _extract_aggregate_teampk(all=False,
                                user=user_team_list).split(',')
    if str(teampk) in interest_teampk_list:
        return True
    return False


def game_venue_detail(game):
    return game['venue']


def _parse_pitcher_fullname(fullname):
    name_lst = fullname.split(', ')
    name = "%s %s" % (name_lst[1],name_lst[0])

    return name
