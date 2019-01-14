#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 11-28-2018
# filename: initial_models.py
# author: brendan
# last modified: 12-07-2018 00:09
#-------------------------------------------------------------------------------
"""
File to run the initial naive models of the predictive analysis
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ds1_project_helper_functions as hf
# import warnings
# warnings.simplefilter(action='ignore', category='SettingWithCopy')

out_folder = 'plots/desc-stats/'

def plot_correct_percentage(df, method, game_hist=False, sample=False):
    """ Plot the correct daily percentage and weekly percentage for the method
    given. Method must be 'home' (home field advantage), 'wp' (win percentage),
    'ps' (pythagorean score). Also, includes a flag to produce a histogram of
    the number of games played per day.
    """
    if method == 'home':
        title = 'Home Field Advantage'
    elif method == 'wp':
        title = 'Win Percentage'
    elif method == 'ps':
        title = 'Pythagorean Score'
    else:
        raise ValueError('{} is not a valid method. Must be one of [home, wp,'\
                         'ps]'.format(method))

    if sample:
        dest_folder = out_folder+'samples/'.format(sample)
    else:
        dest_folder = out_folder

    # create the out folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # group the correct guesses by date
    sum_group = df.groupby('Date').sum()
    count_group = df.groupby('Date').count()
    group = sum_group / count_group

    dayfig, dayax = plt.subplots()
    # change dates to datetime format for plotting
    dates = pd.to_datetime(group.index, format='%Y-%m-%d')
    dayax.bar(dates, group.Correct * 100)
    dayax.axhline(group.Correct.sum() / group.Correct.count() * 100, color='r',
                linestyle='--')
    dayax.set_ylabel('% Correct')
    dayax.xaxis_date()
    dayax.set_title('Percentage of Correct Guesses using {} \n'\
                'by Date for 2018 season'.format(title))
    if sample:
        dayfig.savefig('{}{}-{}-correctness.png'.format(dest_folder, sample,
                                                        method))
    else:
        dayfig.savefig('{}{}-correctness.png'.format(dest_folder, method))
    plt.close(dayfig)

    if game_hist:
        histfig, hax = plt.subplots()
        
        # make a histogram of the number of games played per day, knowing that
        # the highest number of games per day is 15, and there can't be less
        # than zero games played
        hax.hist(count_group.Correct, bins=range(max(count_group.Correct)+1),
                 align='left')
        hax.set_xlabel('Number of Games')
        hax.set_ylabel('Count')
        hax.set_title('Histogram of the Number of Games per Day')
        histfig.savefig('{}num-games-hist.png'.format(dest_folder))
        plt.close(histfig)


def calc_predictions(df, method, plot=True, game_hist=False, sample=False):
    """ Calculate the prediction accuracy for three key variable indicators.
    The three inidcators are 'home' (Home field advantage), 'wp' (Win
    Percentage), and 'ps' (Pythagorean Score). Default to creating a plot,
    while not creating a hist of the distribution of number of games per day.
    Finally, default that the given predictor is not a sample
    """
    # the home method is much simpler to calculate predicted values, they are
    # all 1
    if method == 'home':
        df['Predicted'] = 1
    else:
        # the other two methods are similar, which is why they are grouped
        # inside this else clause
        if method == 'wp':
            # calculate the statistic from win percentage
            df['H_stat'] = df.Home_W / (df.Home_W + df.Home_L)
            df['A_stat'] = df.Away_W / (df.Away_W + df.Away_L)
        elif method == 'ps':
            # calculate the statistic from the pythagorean score
            gamma = 1.79
            df['H_stat'] = df.Home_RS ** gamma / (df.Home_RS ** gamma +
                                                  df.Home_RA ** gamma)
            df['A_stat'] = df.Away_RS ** gamma / (df.Away_RS ** gamma + 
                                                  df.Away_RA ** gamma)

        # fill missing values caused by 0 division
        df = df.fillna(0)
        # if the teams have the same statistic score, the home team wins
        df['Predicted'] = np.where(abs(df.H_stat - df.A_stat) > 0, 
                                   df.H_stat - df.A_stat, 1)
        
        # if the home team has a larger stat, they win, otherwise the away
        # team wins
        df['Predicted'] = np.where(df.Predicted > 0, 1, 0)
    
    # calculate correct predictions
    df['Correct'] = np.where(df.Predicted - df.Home_Win == 0, 1, 0)
    

    # group the correct guesses by date
    sum_group = df.groupby('Date').sum()
    count_group = df.groupby('Date').count()
    group = sum_group / count_group
    print(sum_group.Correct.sum())
    print(count_group.Correct.sum())
    print(group.Correct.sum())
    print(group.Correct.count())
    accuracy = group.Correct.sum() / group.Correct.count()

    print('\nAccuracy of method {} is {:.4f}'.format(method, accuracy))
    # use group by to get day by day accuracy and variance metrics of daily 
    # accuracy
    print('Standard Deviation of daily accuracy: {:.4f}'.format(
        group.Correct.std()))


    if plot:
        plot_correct_percentage(df, method, game_hist, sample)


season_df = pd.read_csv('data/2018-combined.csv', index_col=False,
                        header=0)

calc_predictions(season_df, 'home', game_hist=True)
calc_predictions(season_df, 'wp')
calc_predictions(season_df, 'ps')

"""
sample_folder = 'data/simulated-2018'
for filename in hf.load_file_system(sample_folder):
    sample_df = pd.read_csv('{}/{}'.format(sample_folder, filename),
                            index_col=False, header=0)
    sample = filename.split('.')[0]
    print(sample)
    calc_predictions(sample_df, 'home', plot=False, sample=sample)
    calc_predictions(sample_df, 'wp', plot=False, sample=sample)
    calc_predictions(sample_df, 'ps', plot=False, sample=sample)
"""
