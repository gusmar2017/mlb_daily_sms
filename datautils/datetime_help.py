
#================================================================#
#
# This will be used for all conversion of timestamps and datetimes
# to python versions that can be used.
#
#================================================================#

#import sys
#sys.path.append("/users/gustavomarquez/Desktop/rays_updates")
import datetime
from dateutil import tz



def _convert_timestamp_datetime(game_datetime):
    try:
        time_convert = _convert_to_est(datetime.datetime.strptime(
            game_datetime,"%Y-%m-%dT%H:%M:%SZ"))
    except:
        time_convert = _convert_to_est(datetime.datetime.strptime(
            game_datetime,"%Y-%m-%d %H:%M:%S"))

    return time_convert

def _convert_datestr_datetime(game_date):
    game_date = datetime.datetime.strptime(
        game_date,"%Y-%m-%d"
    ).date()

    return game_date


def _convert_to_est(game_datetime):
    time_est = game_datetime.astimezone(tz.gettz('America/New_York'))

    return time_est


def _gametime_message_handler(gametime):
    if gametime.hour > 12:
        hour_str = str(gametime.hour - 12)
    else:
        hour_str = str(gametime.hour)

    if len(str(gametime.minute)) == 1:
        minute_str = '0' + str(gametime.minute)
    else:
        minute_str = str(gametime.minute)

    string_gametime = hour_str + ':' + minute_str + ' ET'

    return string_gametime
