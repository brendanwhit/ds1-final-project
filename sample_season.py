#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 12-04-2018
# filename: sample_season.py
# author: brendan
# last modified: 12-06-2018 10:00
#-------------------------------------------------------------------------------
"""
File to randomly sample games from each series for a random season.
"""
import csv
import random
import ds1_project_helper_functions as hf

series_folder = 'data/series'
fulldata_folder = 'data'
out_folder = 'data/simulated-2018'

hf.create_folder(out_folder)

def generate_season():
    """ Generate a sample season from the random single games from each series
    """
    # games will hold the date and home team of each game chosen randomly from
    # the series
    games = []
    for filename in hf.load_file_system(series_folder):
        home_team = filename.split('-')[0]
        with open('{}/{}'.format(series_folder, filename), 'r') as sfile:
            sreader = csv.reader(sfile)
            dates = []
            for row in sreader:
                dates.append(row[1])
        date = random.choice(dates)
        games.append((home_team, date))
    
    sim_season = []
    with open('{}/2018-combined.csv'.format(fulldata_folder), 'r') as cfile:
        creader = csv.reader(cfile)
        header = next(creader)
        sim_season.append(header)
        for row in creader:
            gdate = row[0]
            ht_check = row[1]
            if (ht_check, gdate) in games:
                sim_season.append(row)
    
    return sim_season


for i in range(1000):
    sim_season = generate_season()
    with open('{}/{:03}.csv'.format(out_folder, i), 'w') as ssfile:
        sswriter = csv.writer(ssfile)
        sswriter.writerows(sim_season)

