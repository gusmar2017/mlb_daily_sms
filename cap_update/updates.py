
import sys
sys.path.append("/users/gustavomarquez/Desktop/rays_updates")
import statsapi
import requests
import datetime
from dateutil import tz

from datautils.datetime_help import _convert_timestamp_datetime,\
                                    _convert_datestr_datetime,\
                                    _convert_to_est

from datautils.alerter import send_sms

# Documentation: https://toddrob99.github.io/MLB-StatsAPI/#statsapi.game_pace
#github: https://github.com/toddrob99/MLB-StatsAPI


class GameToday():

    def __init__(self,team_name):
        self.today_date = datetime.datetime.now()
        self.team_info = self._pull_interest_teamInfo(team_name)
        self.game_count, self.game_details = self.get_today_game()
        if self.game_count >= 1:
            self.home_team = self._get_team_details(
                self.game_details[0],'home')
            self.away_team = self._get_team_details(
                self.game_details[0],'away')
            self.interest_team_home = self._interst_team_home()


    def next_game_alert_setup(self):

        if self.game_count == 0:
            message = "The %s don't have a game today. Check back tomorrow!"\
                % (self.team_info['name'][-1])
            return message

        opponent,team, team_dir  = self._get_opp_team(
            self.away_team,self.home_team)
        intro_msg = self.set_intro_msg(self.game_details,
                                        opponent,team,team_dir)
        opp_pitcher, team_pitcher = self.set_probable_starter_msg(
                                self.game_details,opponent,team)
        message = intro_msg + team_pitcher + opp_pitcher

        twil_sid = send_sms(message)

        return twil_sid


    def set_intro_msg(self,game_details,opponent,team,team_dir):
        # where opponent and team will be the team details
        intro_msg = """The %s (%s-%s) will be %s to%s against the %s (%s-%s): %s:%s at %s. """ %\
            (team['name'],
                team['wins'],
                team['losses'],
                team_dir,
                game_details[0]['games'][0]['dayNight'],
                opponent['name'],
                opponent['wins'],
                opponent['losses'],
                _convert_timestamp_datetime(
                    game_details[0]['games'][0]['gameDate']).hour,
                _convert_timestamp_datetime(
                    game_details[0]['games'][0]['gameDate']).minute,
                self._get_venue_name(game_details[0])
            )

        return intro_msg


    def get_today_game(self):
        # hits the endpoint for game today
        game_obj = statsapi.get(
            'schedule',{'date':self.today_date.date(),
                        'teamId':self.team_info['id'],
                        'sportId':'1',
                        'hydrate':'probablePitcher(note)'
                        })
        game_today = []
        game_count = game_obj['totalGames']

        # confirms that there is in fact a game
        if game_count >= 1:
            game_today = game_obj['dates']

        return game_count, game_today


    def set_probable_starter_msg(self,game_details,opponent,team):
        opp_pitcher = ''
        team_pitcher = ''

        if opponent['probable_starter']:
            opp_pitcher = """The %s have %s on the hill: %s""" %\
                (opponent['name'],
                opponent['probable_starter'],
                opponent['starter_notes'])

        if team['probable_starter']:
            team_pitcher = """The %s will throw %s: %s """ %\
                (team['name'],
                team['probable_starter'],
                team['starter_notes'])

        return opp_pitcher, team_pitcher


    def _get_opp_team(self,away_team,home_team):
        #this will return an opponent, interst team and team_dir
        if self.interest_team_home:
            opponent = away_team
            team = home_team
            team_dir = 'home'
        else:
            opponent = home_team
            team = away_team
            team_dir = 'away'

        return opponent,team, team_dir


    def _get_venue_name(self,game_details):
        # captures the venue name
        venue_name = game_details['games'][0]['venue']['name']

        return venue_name


    def _get_team_details(self,game_details, dir):
        # this needs both the game details NOT the full list
        #   and the direction for team (home or away)
        team_details = {}
        team_details['id'] =\
            game_details['games'][0]['teams'][dir]['team']['id']
        team_details['name'] =\
            game_details['games'][0]['teams'][dir]['team']['name']
        team_details['wins'] =\
            game_details['games'][0]['teams'][dir]['leagueRecord']['wins']
        team_details['losses'] =\
            game_details['games'][0]['teams'][dir]['leagueRecord']['losses']
        team_details['probable_starter'] = self._parse_pitcher_fullname(
            game_details['games'][0]['teams'][dir]\
                ['probablePitcher']['fullName'])
        team_details['starter_notes'] =\
            game_details['games'][0]['teams'][dir]\
                ['probablePitcher']['note']

        return team_details


    def _pull_interest_teamInfo(self,team_name):
        error_msg = 'Team not found'
        team_info = statsapi.lookup_team(team_name,
            activeStatus='Y',
            season= self.today_date.year,
            sportIds=1)

        if len(team_info) == 1:
            return team_info[0]

        return error_msg


    def _interst_team_home(self):
        team_home = True
        if self.away_team['id'] == self.team_info['id']:
            team_home = False

        return team_home


    def _parse_pitcher_fullname(self,fullname):
        name_lst = fullname.split(', ')
        name = "%s %s" % (name_lst[1],name_lst[0])
        return name


def main():
    game = GameToday(team_name='Rays')
    game.next_game_alert_setup()

if __name__=='__main__':
	main()
