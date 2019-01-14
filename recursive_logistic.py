#!/usr/bin/env python3
# -*- coding: utf8 -*-
#-------------------------------------------------------------------------------
# created on: 12-05-2018
# filename: recursive_logistic.py
# author: brendan
# last modified: 12-06-2018 10:27
#-------------------------------------------------------------------------------
"""
File to perform recursive logistic regression on the variables. For every day,
a logistic classifier will be trained on previous games played, then the
classifier will be used to predict the games that day. Then the day will
progess, and the true values of the previous day will be used to further train
the classifier.
"""
import ds1_project_helper_functions as hf
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import LogisticRegression
import numpy as np
import matplotlib.pyplot as plt

# boolean to include the weather data
weather = True

# run on full season for testing
full_df = pd.read_csv('data/2018-combined.csv', index_col=False, header=0)
# full_df = pd.read_csv('data/simulated-2018/002.csv', index_col=False, header=0)
# change dates to datetime
full_df['Date'] = pd.to_datetime(full_df.Date)
full_df = hf.calc_wp_ps(full_df)

features = ['Away_PS', 'TMAX', 'Home_PS', 'TMIN', 'Home_WP', 'Away_WP']
# loop through the dates to, can't predict the first day of the season
complete_test_Y = np.array([])
complete_pred_Y = np.array([])

for date in full_df.Date.unique()[1:]:
    # make training data
    train_df= full_df[full_df['Date'] < date]
    train_X = train_df.drop(['Date', 'Home_Team', 'Away_Team', 'Home_Win'],
                           axis=1)
    # train_X = train_X[features]
    train_Y = train_df["Home_Win"]
    
    # make testing data
    test_df = full_df[full_df['Date'] == date]
    test_X = test_df.drop(['Date', 'Home_Team', 'Away_Team', 'Home_Win'],
                           axis=1)
    # test_X = test_X[features]
    test_Y = test_df['Home_Win']
    
    complete_test_Y = np.concatenate((complete_test_Y, test_Y.as_matrix()))

    clf = LogisticRegression()
    clf.fit(train_X, train_Y)
    pred_Y = clf.predict(test_X)
    
    """
    # use probabilities and random coin flips to choose winner of game
    prob_losses = clf.predict_proba(test_X)[:, 0]
    flips = np.random.rand(*prob_losses.shape)
    # new prediction value is based on the random coin flips
    pred_Y = np.where(prob_losses < flips, 1, 0)
    """
    complete_pred_Y = np.concatenate((complete_pred_Y, pred_Y))

results = confusion_matrix(complete_test_Y, complete_pred_Y)
print(results)
print((results[0,0] + results[1,1]) / np.sum(results))

    
# run for the samples
sample_folder = 'data/simulated-2018'
sample_accuracies = []
for filename in hf.load_file_system(sample_folder):
    sample_df = pd.read_csv('{}/{}'.format(sample_folder, filename),
                            index_col=False, header=0)
    
    # change dates to datetime
    sample_df['Date'] = pd.to_datetime(sample_df.Date)
    sample_df = hf.calc_wp_ps(sample_df)

    # parse out the features
    features = ['Away_PS', 'TMAX', 'Home_PS', 'TMIN', 'Home_WP', 'Away_WP']
    # loop through the dates to, can't predict the first day of the season
    complete_test_Y = np.array([])
    complete_pred_Y = np.array([])

    for date in sample_df.Date.unique()[1:]:
        # make training data
        train_df= sample_df[sample_df['Date'] < date]
        train_X = train_df.drop(['Date', 'Home_Team', 'Away_Team', 'Home_Win'],
                               axis=1)
        # train_X = train_X[features]
        train_Y = train_df["Home_Win"]
        
        # make testing data
        test_df = sample_df[sample_df['Date'] == date]
        test_X = test_df.drop(['Date', 'Home_Team', 'Away_Team', 'Home_Win'],
                               axis=1)
        # test_X = test_X[features]
        test_Y = test_df['Home_Win']
        
        clf = LogisticRegression()
        try:
            clf.fit(train_X, train_Y)
        except ValueError:
            # if there is only one class for fitting skip this date, with
            # enough samples skipping won't hurt us in the end
            continue
        
        pred_Y = clf.predict(test_X)
        
        """
        # use probabilities and random coin flips to choose winner of game
        prob_losses = clf.predict_proba(test_X)[:, 0]
        flips = np.random.rand(*prob_losses.shape)
        # new prediction value is based on the random coin flips
        pred_Y = np.where(prob_losses < flips, 1, 0)
        """
        complete_pred_Y = np.concatenate((complete_pred_Y, pred_Y))
        complete_test_Y = np.concatenate((complete_test_Y, test_Y.as_matrix()))

    results = confusion_matrix(complete_test_Y, complete_pred_Y)
    accuracy = (results[0,0] + results[1,1]) / np.sum(results)
    sample_accuracies.append(accuracy)
    print('{}...'.format(filename))

acc_mean = np.mean(sample_accuracies)
acc_std = np.std(sample_accuracies)
print(acc_mean)
print(acc_std)

# plot out the distribution
fig, ax = plt.subplots()

ax.hist(sample_accuracies, bins=30)
ax.set_xlabel('Regression Accuracy')
ax.set_ylabel('Count')
fig.suptitle('Histogram of Regression Accuracy on Sampled Seasons')
fig.savefig('plots/hist_acc.jpg')
plt.close(fig)


