#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 12-05-2018
# filename: ds1-project-helper-functions.py
# author: brendan
# last modified: 12-05-2018 13:05
#-------------------------------------------------------------------------------
"""
Some helper functions to reduce code redundancy across the board. Mostly to do
with file management  and loading
"""
import os

def load_file_system(directory):
    """ Load up the file system to traverse over
    """
    load_directory = os.fsencode(directory)
    for my_file in os.listdir(load_directory):
        filename = os.fsdecode(my_file)
        yield filename


def create_folder(directory):
    """ Create the folder  if it doesn't already exist
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


def calc_wp_ps(df):
    """ calculate the win percentage and pythagorean score for a baseball
    dataframe
    """
    # adding Win percentages and Pythagorean scores
    df['Home_WP'] = df.Home_W / (df.Home_W + df.Home_L)
    df['Away_WP'] = df.Away_W / (df.Away_W + df.Away_L)

    gamma = 1.79
    df['Home_PS'] = df.Home_RS ** gamma / (df.Home_RS ** gamma +
                                                df.Home_RA ** gamma)
    df['Away_PS'] = df.Away_RS ** gamma / (df.Away_RS ** gamma +
                                                df.Away_RA ** gamma)
    # fill in nans created by zero division
    df = df.fillna(0)
    return df
