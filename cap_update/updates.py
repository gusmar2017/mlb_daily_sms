
import sys
sys.path.append("/users/gustavomarquez/Desktop/rays_updates")
sys.path.append("/home/gusmar/rays_updates/mlb_daily_sms")

import datetime

from datautils.game_details import get_teams_games

from datautils.alerter import send_sms

from datautils.team_details import user_data_team_details

from datautils.message_creater import create_all_msgs

# Documentation: https://toddrob99.github.io/MLB-StatsAPI/#statsapi.game_pace
#github: https://github.com/toddrob99/MLB-StatsAPI


class GameToday():

    def __init__(self):
        self.user_data = user_data_team_details()
        self.today_date = datetime.datetime.now()
        self.all_games = get_teams_games(self.user_data)
        #self.run_all_jobs()


    def run_all_jobs(self):
        msg = create_all_msgs(self.user_data,self.all_games)

        for user in msg:
            send_sms(msg[user],self.user_data[user]['phone_number'])

        return print(msg)

def main():
    game = GameToday()

if __name__=='__main__':
	main()
