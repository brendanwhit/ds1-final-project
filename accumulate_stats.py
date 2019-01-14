#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 11-28-2018
# filename: accumulate_stats.py
# author: brendan
# last modified: 11-28-2018 20:59
#-------------------------------------------------------------------------------
"""
Accumulate the basic stats as the season progresses,
the accumulated stats will be used to drive the projection of game winners.
"""
import os
import pandas as pd

in_folder = 'data/season-overview'
out_folder = 'data/accumulated-season'
# create the out folder if it doesn't exist
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

load_directory = os.fsencode(in_folder)

for my_file in os.listdir(load_directory):
    filename = os.fsdecode(my_file)
    print(filename)
    team_df = pd.read_csv('{}/{}'.format(in_folder, filename), index_col=0,
                          header=0)
    shift_cols = ['Runs_For', 'Runs_Against', 'Wins', 'Losses', 'Streak']
    for column in shift_cols:
        # shift the columns down one and put zeros where the nans appear.
        # now all information is consistent with coming into the game
        team_df[column] = team_df[column].shift(1)
        team_df.loc[1, column] = 0
    
    # cumulatively sum up the runs for and runs against columns
    team_df.Runs_For = team_df.Runs_For.cumsum()
    team_df.Runs_Against = team_df.Runs_Against.cumsum()
    print(team_df.head())
    print(team_df.tail())

    # write the accumulated stats to a new csv
    team_df.to_csv('{}/{}'.format(out_folder, filename))
