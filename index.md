---
title: Predicting Baseball Game Outcomes
subtitle: With Weather Data and Recursive Logistic Regression
author: Brendan Whitney
---

_This paper attempts to build a regression model to predict the winner of 
baseball games for the 2018 MLB season.
The regression model is built from two disjoint datasets:
baseball statistics from baseball-reference.com
and weather data from the Global Historical Climatology Network.
The text presents initial results from an exploration of the data combined 
to create the full dataset.
Then the regression model is created and analyzed using recursive models
that are trained on the previous games before predicting the games for 
each day of the season.
The model had a predictive power of 55.77\%,
which is more predictive than coin flips.
However,
the model did not have more predictive power than just simply choosing
the team with the highest win percentange or Pythagorean score._

### Introduction

Predicting the outcome of sports games is a very difficult problem,
and has been studied for a while now.
There are many factors that go into the outcome of a game,
and what appears to be a lot of luck involved as well.
Additionally,
many factors that affect the outcome of a game are often not reflected in the
pure statistics of the teams entering the contest.
Considering just statistics of the two teams does not include other potentially
important information,
such as injuries to important players,
or the atmosphere of the team \cite{Boulier}.
That extraneous information has long been believed to play a role in the
results of contests.
This manifests itself in what we would consider to be luck,
and plays into the notion that everytime two teams play each other "its
anyones game".
Perhaps what we currently percieve as luck in sports games is instead simply
not having the vital data required to correctly predict outcomes.
