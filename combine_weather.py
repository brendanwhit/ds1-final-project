#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 12-04-2018
# filename: combine_weather.py
# author: brendan
# last modified: 12-04-2018 19:51
#-------------------------------------------------------------------------------
"""
Combine the weather data with the game data
"""
import csv

data_folder = 'data'
weather_folder = 'data/weather-data'

# create data from the weather data and the full season on the home team and
# the date
data = []
# focus on just weather and if the home team won
just_weather = []
with open('{}/2018-just-baseball.csv'.format(data_folder), 'r') as csvfile:
    myreader = csv.reader(csvfile)
    # skip the header
    header  = next(myreader)
    # add the three new column headers for weather
    weather_header = ['TMAX', 'TMIN', 'PRCP']
    data.append(header + weather_header)
    just_weather.append(['Date', 'Home_Team', 'Home_Win'] + weather_header)
    for row in myreader:
        # get the home team and date
        date = row[0]
        home_team = row[1]
        win = row[-1]
        # keep track of limited info, just date and win
        limit_packet = [date, home_team, win]
        with open('{}/{}-2018.csv'.format(weather_folder, home_team), 'r') \
                as weatherfile:
            weather_reader = csv.reader(weatherfile)
            # skip the header
            next(weather_reader)
            for wrow in weather_reader:
                wdate = wrow[-1]
                if date == wdate:
                    tmax = wrow[4]
                    tmin = wrow[6]
                    prcp = wrow[8]
                    weather = [tmax, tmin, prcp]
                    break
        
        data.append(row + weather)
        just_weather.append(limit_packet + weather)


# save the combined season
with open('{}/2018-combined.csv'.format(data_folder), 'w') \
        as fullfile:
    mywriter = csv.writer(fullfile)
    for row in data:
        mywriter.writerow(row)

# save the just weather data
with open('{}/2018-just-weather.csv'.format(data_folder), 'w') as weatherfile:
    mywriter = csv.writer(weatherfile)
    for row in just_weather:
        mywriter.writerow(row)
