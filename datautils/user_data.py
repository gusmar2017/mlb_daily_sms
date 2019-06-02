import yaml

import sys
#sys.path.append("/users/gustavomarquez/Desktop/rays_updates")
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# can grab user_data but also has a tool to load yaml files
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def get_user_data():
    # Gets the users.yaml file that has information for how to handle search
    #   user
    user_data = get_yaml_data('/datautils/users.yaml')

    return user_data


def _extract_user_interest_teams(all=True,**kwarg):
    # this is used for getting a string of intersted teams
    # example: "Rays,Yankees,Twins"
    interest_teams = []

    if not all:
        user_data = get_user_data()[kwarg['user']]
        interest_teams += user_data['teams'].split(',')
    else:
        user_data = get_user_data()
        for user in user_data:
            interest_teams += user_data[user]['teams'].split(',')

    interest_teams = list(dict.fromkeys(interest_teams))

    return interest_teams


def get_yaml_data(file_name):
    # loads yaml data for any subdirectory and file.yaml
    yam_data = open(sys.path[-1] + file_name,'r')
    loaded_data = yaml.safe_load(yam_data)

    return loaded_data
