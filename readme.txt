Code files and descriptions:

accumulate_stats.py
    - Load data from data/season-overview/ and shift the stats down one game.
    Keep a running tally to represent the accumulation
    of knowledge as the season progresses.  Save the accumulated seasons into
    data/accumulated-season/

combine_weather.py
    - Add the weather data to the baseball stats by location and date.  This
    code creates the complete dataset for analysis.

ds1_project_helper_functions.py
    - Common functions used in multiple code files, to reduce redundant code

feature_selection.py
    - Run a Random Forest Regressor by date to pull out the most important
    features as the season progresses.

get_station_by_distance.sql
    - SQL code used to grab the closest weather station to a baseball stadium
    that has records for TMAX, TMIN, and PRCP with no missing values from
    March 1st to October 31st.
        - Requires manually entering the lat long of each stadium

get_weather_data.sql
    - SQL code used to grab the weather date from the station that is given
    from the get_station_by_distance.sql

intial_models.py
    - Run the initial models as baselines to compare the success of the
    logistic regression against.

pair_games.py
    - Pair the games together into the almost complete dataset used for
    analysis.

plot_corr_mat.py
    - Plot the correlation matrices for the complete season and an example
    sample season based on desired variables

plot_weather_example.py
    - Create a plot as an example of what the weather data looks like for each
    stadium, and how the weather is incorporated into the dataset.

recursive_logistic.py
    - Run the recursive logistic regressor for the complete 2018 season, and 
    the 1000 sample seasons

sample_season.py
    - Generate the 1000 sample seasons from the series data located in
    data/series/.  Then select each sampled game from data/2018_combined.csv to
    get the full stats, and save the resulting sampled season into 
    data/simulated-2018/

scrape_season.py
    - Scrape the baseball statistics from baseball-reference.com, and save each
    schedule to data/season-overview/ to be further manipulated

series_detector.py
    - Locate each series and save them in the data/series/ for future use
