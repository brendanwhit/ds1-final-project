#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 11-27-2018
# filename: scrape_season.py
# author: brendan
# last modified: 11-27-2018 12:31
#-------------------------------------------------------------------------------
"""
Code to scrape season games and results. Basic stats
"""
import requests
from bs4 import BeautifulSoup
from collections import Counter
import csv
import os
import time

data_folder = 'data/season-overview'
# create the data folder if it doesn't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)

year = '2018'
teams = ['BOS', 'TBR', 'MIA', 'NYY', 'LAA', 'OAK', 'BAL', 'KCR', 'TEX', 'TOR',
         'ATL', 'SEA', 'CHW', 'DET', 'HOU', 'WSN', 'MIN', 'CLE', 'PHI', 'CIN',
         'NYM', 'COL', 'LAD', 'ARI', 'SFG', 'PIT', 'SDP', 'CHC', 'STL', 'MIL']

for team in teams:
    print('Collecting for {}...'.format(team))

    url  = 'https://www.baseball-reference.com/teams/'\
            '{}/{}-schedule-scores.shtml'.format(team, year)

    soup = BeautifulSoup(requests.get(url).text, 'lxml')
    season_info = [['Game', 'Date', 'Opp', 'Home', 'Win', 'Runs_For',
                   'Runs_Against', 'Wins', 'Losses', 'Streak']]
    for item in soup.find_all('tr'):
        game = item.th.string
        if game == 'Gm#':
            # skip the strange game number info
            continue
        try:
            info = item.find_all('td')
            date = info[0]['csk']
            # check if the team played away or home
            home_game = 0 if info[3].string else 1
            opp_team = info[4].string
            win_loss = info[5].string.split('-')
            win = 1 if win_loss[0] == 'W' else 0
            runs_for = info[6].string
            runs_against = info[7].string
            record = info[9].string
            wins, losses = record.split('-')
            streak = info[18].string
            if '+' in streak:
                streak = len(streak)
            else:
                streak = -len(streak)

        except IndexError:
            pass
        try:
            season_info.append([game, date, opp_team, home_game, win, runs_for,
                            runs_against, wins, losses, streak])
        except NameError:
            print(info)


    with open('{}/{}-{}.csv'.format(data_folder, team, year), 'w',
              newline='') as write_file:
        write = csv.writer(write_file)
        write.writerows(season_info)

    # pause for 2 seconds so I don't make baseball reference mad
    time.sleep(2)
