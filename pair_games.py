#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 11-28-2018
# filename: pair_games.py
# author: brendan
# last modified: 12-06-2018 23:53
#-------------------------------------------------------------------------------
"""
Code to turn seasons into games with two teams represented.
"""
import os
import dateutil.relativedelta as rdelta
import datetime as dt
import csv

in_folder = 'data/accumulated-season'
out_folder = 'data'

# create the out folder if it doesn't exist
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# the first day of the season
earliest_date = dt.datetime.strptime('2018-03-29', '%Y-%m-%d')
last_date = dt.datetime.strptime('2018-10-01', '%Y-%m-%d')
test_date = dt.datetime.strptime('2018-04-01', '%Y-%m-%d')


def load_file_system(in_folder):
    """ Load up the file system to traverse over
    """
    load_directory = os.fsencode(in_folder)
    for my_file in os.listdir(load_directory):
        filename = os.fsdecode(my_file)
        yield filename


def get_day_info(date):
    """ Generate list of files with teams that played on the date we desire
    """
    teams_with_games = []
    for filename in load_file_system(in_folder):
         with open('{}/{}'.format(in_folder, filename), 'r') as csvfile:
            myreader = csv.reader(csvfile)
            # skip the header
            next(myreader)
            for row in myreader:
                filedate = dt.datetime.strptime(row[1], '%Y-%m-%d')
                if filedate == date:
                    teams_with_games.append((filename, row))
                    # pretty sure the break below was stopping doublheaders
                    # from being counted
                    # break

    return teams_with_games


def build_season(earliest_date, last_date):
    """ Construct the season of games played in between the dates given.
    Most likely the given dates will be the first and last games of the season.
    """
    current_date = earliest_date
    while current_date <= last_date:
        team_list = get_day_info(current_date)
        checked = []
        count = 0
        num_teams = len(team_list)
        for team, stats in team_list:
            if team not in checked:
                count += 1
                team = team.split('-')[0]
                date = stats[1]
                opponent = stats[2]
                
                for opp_team, opp_stats in team_list:
                    # iterate through the list until the opponent is found
                    if opponent == opp_team.split('-')[0]:
                        checked.append(opp_team)
                        break

                if int(stats[3]):
                    # target variable
                    home_win = stats[4]

                    home_team = team
                    home_runs_scored = stats[5]
                    home_runs_allowed = stats[6]
                    home_wins = stats[7]
                    home_losses = stats[8]
                    home_streak = stats[9]
                    
                    away_team = stats[2]
                    away_runs_scored = opp_stats[5]
                    away_runs_allowed = opp_stats[6]
                    away_wins = opp_stats[7]
                    away_losses = opp_stats[8]
                    away_streak = opp_stats[9]

                else:
                    # target variable
                    home_win = 1 - int(stats[4])

                    away_team = team
                    away_runs_scored = stats[5]
                    away_runs_allowed = stats[6]
                    away_wins = stats[7]
                    away_losses = stats[8]
                    away_streak = stats[9]
                    
                    home_team = stats[2]
                    home_runs_scored = opp_stats[5]
                    home_runs_allowed = opp_stats[6]
                    home_wins = opp_stats[7]
                    home_losses = opp_stats[8]
                    home_streak = opp_stats[9]

                
                yield (date, home_team, away_team, home_runs_scored, 
                      home_runs_allowed, away_runs_scored, away_runs_allowed, 
                      home_wins, home_losses, away_wins, away_losses, 
                      home_streak, away_streak, home_win)
        
        # quick check to see that all the games are indeed being counted
        if count != num_teams / 2:
            print(current_date)
            print('Number of teams: {}'.format(num_teams))
            print('Number of games: {}'.format(count))
        
        current_date += rdelta.relativedelta(days=1)   


# now that we have the earliest date, we will begin creating game by game
with open('{}/2018-just-baseball.csv'.format(out_folder), 'w') as csvfile:
    mywriter = csv.writer(csvfile)
    mywriter.writerow(['Date', 'Home_Team', 'Away_Team', 'Home_RS', 'Home_RA',
                      'Away_RS', 'Away_RA', 'Home_W', 'Home_L', 'Away_W', 
                       'Away_L', 'Home_Streak', 'Away_Streak', 'Home_Win'])
    for bundle in build_season(earliest_date, last_date):
        mywriter.writerow(bundle)


