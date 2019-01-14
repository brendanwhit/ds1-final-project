#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 12-04-2018
# filename: plot_weather_example.py
# author: brendan
# last modified: 12-05-2018 12:56
#-------------------------------------------------------------------------------
"""
File to plot the weather data for BOS
"""
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import datetime as dt
import csv
import ds1_project_helper_functions as hf

weather_folder = 'data/weather-data'
game_folder = 'data/series'
team = 'BOS'

# load the weather data
weather_data = []
with open('{}/{}-2018.csv'.format(weather_folder, team), 'r') as wfile:
    wreader = csv.reader(wfile)
    header = next(wreader)
    for row in wreader:
        date = dt.datetime.strptime(row[-1], '%Y-%m-%d')
        tmax = float(row[4])
        tmin = float(row[6])
        prcp = float(row[8])
        # make packets of weather data per date
        weather_data.append((date, tmax, tmin, prcp))

# load the game data
game_dates = []
for filename in hf.load_file_system(game_folder):
    home_team = filename.split('-')[0]
    if home_team == team:
        with open('{}/{}'.format(game_folder, filename), 'r') as gfile:
            greader = csv.reader(gfile)
            for row in greader:
                date = dt.datetime.strptime(row[1], '%Y-%m-%d')
                game_dates.append(date)

# line up weather and game dates to make a color list
wdates, tmax, tmin, prcp = zip(*sorted(weather_data))
# make a boolean mask for game dates
date_bools = [wdate in game_dates for wdate in wdates]

# generate packets of games played in a row
home_stretches = []
# placeholder for end of last home stretch
k = 0
for i in range(len(date_bools)):
    if date_bools[i] and i > k:
        start = i
        j = start
        while date_bools[j+1]:
            j += 1
        end = j
        k = end
        home_stretches.append((start, end))



# make the plot
fig, ax = plt.subplots()
loc = dts.MonthLocator()
myFmt = dts.DateFormatter('%m')

ax.plot(wdates, tmax, 'r', linewidth=0.75)
ax.plot(wdates, tmin, 'b', linewidth=0.75)
# highlight games that were played at home
for i, j in home_stretches:
    ax.axvspan(wdates[i], wdates[j+1], color='y', alpha=0.25)
ax.xaxis_date()
ax.set_ylabel('Temp ($^\circ$C)')
# make a second axis that twins the first
ax2 = ax.twinx()
ax2.bar(wdates, prcp, color='k')
ax2.set_ylabel('Precipitation (mm)')
ax2.set_xlabel('Month')
# plot just the months to clean up plot
ax2.xaxis.set_major_formatter(myFmt)

fig.suptitle('Weather Data for Fenway for 2018 Season')
fig.savefig('plots/weather-example.jpg')
plt.close(fig)

