#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 11-28-2018
# filename: plot_corr_mat.py
# author: brendan
# last modified: 12-07-2018 16:54
#-------------------------------------------------------------------------------
"""
A File to run exploratory statistics on the 2018 season for my DS1 Final
Project
"""
import ds1_project_helper_functions as hf
import pandas as pd
import matplotlib.pyplot as plt

master_dir = 'plots/corr-mats'

def plot_corr_mat(df, df_type, full_season=True):
    """ Plot the correlation matrix of the variables of interest.  We record
    the df type to indicate the values being plotted. 
    Acceptable types:
        'jb' = just baseball stats
        'jw' = just weather stats
        'comb' = combined weather and baseball stats
    Also, boolean indicating if the season plotted is the full season or a
    series sampled season
    """
    if df_type == 'jb':
        filename = 'baseball'
    elif df_type == 'jw':
        filename = 'weather'
    elif df_type == 'comb':
        filename = 'combined'
    else:
        raise ValueError('{} is not a valid df_type. Choose from ["jb", "jw",'\
                         '"comb"]'.format(df_type))
    
    if full_season:
        folder = '{}/full-season'.format(master_dir)
    else:
        folder = '{}/sampled-season'.format(master_dir)

    hf.create_folder(folder)

    # get the correlation matrix between the variables
    fig, ax = plt.subplots()
    corr = df.corr()
    # plot the absolute value of the correaltion matrix
    im = ax.matshow(abs(corr), cmap='Reds', vmin=0, vmax=1)
    fig.colorbar(im)
    plt.xticks(range(len(corr.columns)), corr.columns)
    plt.yticks(range(len(corr.columns)), corr.columns)
    # rotate the x labels
    plt.xticks(rotation=90)
    fig.subplots_adjust(left=0.2, top=0.75)
    plt.savefig('{}/{}-stats-corr-mat.jpg'.format(folder, filename))
    plt.close()


def prepare_df(df, df_type, full_season=True):
    """ Prepare the data frame for consistent plotting of the correlation
    matrix
    """
    if df_type == 'jw':
        column_order = ['Date', 'Home_Team', 'TMAX', 'TMIN', 'PRCP',
                        'Home_Win']
    else:
        # if it includes baseball stats, calculate win percentage and
        # pythagorean score
        df = hf.calc_wp_ps(df)
        if df_type == 'jb':
            column_order = ['Date', 'Home_Team', 'Away_Team', 'Home_RS', 
                            'Home_RA', 'Home_PS', 'Away_RS', 'Away_RA',
                            'Away_PS', 'Home_W', 'Home_L', 'Home_WP', 'Away_W',
                            'Away_L', 'Away_WP', 'Home_Streak', 'Away_Streak',
                            'Home_Win']
        elif df_type == 'comb':
            column_order = ['Date', 'Home_Team', 'Away_Team', 'Home_RS', 
                            'Home_RA', 'Home_PS', 'Away_RS', 'Away_RA',
                            'Away_PS', 'Home_W', 'Home_L', 'Home_WP', 'Away_W',
                            'Away_L', 'Away_WP', 'Home_Streak', 'Away_Streak',
                            'TMAX', 'TMIN', 'PRCP', 'Home_Win']
    
    # reorder the dataframe for better plotting
    df = df[column_order]
    print(df.count())
    # plot the correlation matrix
    if full_season:
        plot_corr_mat(df, df_type)
    else:
        plot_corr_mat(df, df_type, False)


# plot of full season data
full_df = pd.read_csv('data/2018-combined.csv', index_col=False,
                        header=0)
prepare_df(full_df, 'jb')
prepare_df(full_df, 'jw')
prepare_df(full_df, 'comb')

# plot of a sampled season data
sim_df = pd.read_csv('data/simulated-2018/000.csv', index_col=False,
                          header=0)
prepare_df(sim_df, 'jb', False)
prepare_df(sim_df, 'jw', False)
prepare_df(sim_df, 'comb', False)
