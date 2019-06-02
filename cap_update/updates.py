
import sys
sys.path.append("/users/gustavomarquez/Desktop/rays_updates")

import datetime

from datautils.datetime_help import _convert_timestamp_datetime,\
                                    _convert_datestr_datetime,\
                                    _convert_to_est

from datautils.game_details import get_teams_games_today

from datautils.alerter import send_sms

from datautils.team_details import user_data_team_details

from datautils.message_creater import create_all_msgs

# Documentation: https://toddrob99.github.io/MLB-StatsAPI/#statsapi.game_pace
#github: https://github.com/toddrob99/MLB-StatsAPI


class GameToday():

    def __init__(self):
        self.user_data = user_data_team_details()
        self.today_date = datetime.datetime.now()
        self.all_games = get_teams_games_today()
        self.game_count = len(self.all_games)
        self.run_all_jobs()


    def run_all_jobs(self):
        msg = create_all_msgs(self.user_data,self.all_games)

        for user in msg:
            for game_msg in msg[user]:
                send_sms(game_msg,self.user_data[user]['phone_number'])

        return print(msg)

def main():
    game = GameToday()

    print(user_data)

if __name__=='__main__':
	main()
