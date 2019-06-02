#import sys
#sys.path.append("/users/gustavomarquez/Desktop/rays_updates")
from datetime import datetime

from datautils.user_data import _extract_user_interest_teams,\
                                get_user_data

import statsapi

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Extract all team details for mlb teams of interest
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def grab_active_teams(season=datetime.now().year,activeStatus='Y',
                sportIds=1):
    params = {'activeStatus':activeStatus,
        'season':season,
        'sportIds':sportIds,
        'fields':'teams,id,name,abbreviation,\
                teamName,locationName,league,division,venue'}
    active_teams = statsapi.get('teams',params)

    return active_teams['teams']


def pull_interest_teamInfo():
    team_names = _extract_user_interest_teams()
    error_msg = 'Teams not found'
    all_teams = grab_active_teams()
    key_teams = _extract_team_from_team_list(all_teams,team_names)
    if key_teams:
        return key_teams

    return error_msg


def user_data_team_details():
    user_data = get_user_data()
    all_teams = pull_interest_teamInfo()

    if all_teams != 'Teams not found':
        for user in user_data:
            teams = user_data[user]['teams'].split(',')
            team_match = _extract_team_from_team_list(all_teams,teams)
            user_data[user]['team_details'] = team_match

        return user_data

    return print('Something is wrong')


def _extract_team_from_team_list(all_teams,values):
    """
    Output: subset list from larger list of Teams
    input:
        all_teams: larger list of Teams
        values = values to match for
            example: ['Yankees','NYY','Rays']
    """
    key_fields = ['id','name','abbreviation','teamName',
                    'locationName']
    key_teams = []
    for team in all_teams:
        for field in team:
            if field in key_fields:
                if str(team[field]).lower() in [str(x).lower() for x in values]:
                    key_teams.append(team)

    return key_teams


def _extract_aggregate_teampk(all=True,**kwargs):

    if not all:
        team_list = kwargs['user']
    else:
        team_list = pull_interest_teamInfo()
    teampk = []
    if team_list != 'Teams not found':
        for team in team_list:
            teampk.append(team['id'])
            teampk = list(dict.fromkeys(teampk))
        output_str = ''
        for item in teampk:
            if output_str == '':
                output_str += str(item)
            else:
                output_str += ','+str(item)

        return output_str

    return team_list
