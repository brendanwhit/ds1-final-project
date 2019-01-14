#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 12-05-2018
# filename: feature_selection.py
# author: brendan
# last modified: 12-05-2018 15:59
#-------------------------------------------------------------------------------
"""
This file uses a random forest classifier to pick important features for
predicting the winner of games. I will use both a full season of data and a
sampled season of data.
"""
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
import numpy as np
import ds1_project_helper_functions as hf

# run on full season for feature extraction
full_df = pd.read_csv('data/2018-combined.csv', index_col=False, header=0)
# change dates to datetime
full_df['Date'] = pd.to_datetime(full_df.Date)
full_df = hf.calc_wp_ps(full_df)
# loop through the dates to get different regression values
features2importances = {}
for date in full_df.Date.unique():
    date_df = full_df[full_df['Date'] <= date]
    sX = date_df.drop(['Date', 'Home_Team', 'Away_Team', 'Home_Win'], axis=1)
    sY = date_df["Home_Win"]
    names = sX.columns
    rf = RandomForestRegressor()
    rf.fit(sX, sY)
    features = zip(rf.feature_importances_, names)
    for score, feature in features:
        try:
            features2importances[feature].append(score)
        except KeyError:
            features2importances[feature] = [score]

# analyze the features2importances
print('Full Data')
# keep track of mean feature score to rank them for plots
features = []
for feature, importances in features2importances.items():
    mean_importance = np.mean(importances)
    std_importance = np.std(importances)
    print('{} has a mean importance {:.4f}'\
          ' with std {:.4f}'.format(feature, mean_importance, std_importance))
    features.append((mean_importance, feature))

features = sorted(features, reverse=True)
print(features)
# keep the top 5 for analysis by date
plot_features = features[:6]

fig, ax = plt.subplots()
dates = full_df.Date.unique()
for score, feature in plot_features:
    ax.plot(dates, features2importances[feature], label=feature, linewidth=1)
ax.legend()
ax.xaxis_date()
ax.set_label('Date of Training')
ax.set_ylabel('Importance Score')
fig.suptitle('Importance of Features as Season Progresses')
fig.savefig('plots/feature-importance.jpg')
plt.close(fig)
