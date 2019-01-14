#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 12-04-2018
# filename: series_detector.py
# author: brendan
# last modified: 12-04-2018 22:26
#-------------------------------------------------------------------------------
"""
Organize the seasons into series for faster sampling of random games, which
will hopefully remove the collinearity of teams playing multiple games in a row
together
"""
import os
import csv

in_folder = 'data/accumulated-season'
out_folder = 'data/series'
teams = ['BOS', 'TBR', 'MIA', 'NYY', 'LAA', 'OAK', 'BAL', 'KCR', 'TEX', 'TOR',
         'ATL', 'SEA', 'CHW', 'DET', 'HOU', 'WSN', 'MIN', 'CLE', 'PHI', 'CIN',
         'NYM', 'COL', 'LAD', 'ARI', 'SFG', 'PIT', 'SDP', 'CHC', 'STL', 'MIL']

# create the out folder if it doesn't exist
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

def save_series(team, opponent, date, series):
    """ Save the series in a file for later acquisition
    """
    with open('{}/{}-{}-{}.csv'.format(out_folder, team, opponent, date), 'w') \
        as csvfile:
        mywriter = csv.writer(csvfile)
        for row in series:
            mywriter.writerow(row)


def accumulate_series(team):
    """ Break the season for a single team into the series that they play, and
    save them accordingly into files
    """
    with open('{}/{}-2018.csv'.format(in_folder, team), 'r') as csvfile:
        myreader = csv.reader(csvfile)
        # skip header
        next(myreader)
        # the games are in date order, so we will keep track of that
        # load the first game as the first series
        # make series a dictionary to work around writing issues
        i = 1
        data = next(myreader)
        series = {i: data}
        opponent = data[2]
        date = data[1]
        home = int(data[3])
        for row in myreader:
            if row[2] == opponent:
                i += 1
                series[i] = row
            else:
                if home:
                    write_data = list(series.values())
                    # only save the series if the team is home
                    save_series(team, opponent, date, write_data)
                # initialize new dictionary and counter
                i = 1
                series = {}
                series[i] = row
                opponent = row[2]
                date = row[1]
                home = int(row[3])


# save the games played in series chunks
for team in teams:
    accumulate_series(team)
