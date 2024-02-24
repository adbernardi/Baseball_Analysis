'''

Making a fantasy baseball database and script to effectively cost cut and manage a team.

'''
'''

1. Data Importing and Cleaning

'''

# Importing the necessary libraries

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

# Reading in the data for both our team and the league as a whole 
# we'll read in 2023 data and then eventually 2024 projections 

mof_23_df = pd.read_csv('/home/adbucks/Downloads/cin_mof_roster_23pts.csv' , header = 1) 
league_23_df = pd.read_csv('/home/adbucks/Downloads/all_players_universe.csv')

# Let's take a look at the data 
# we actually want to drop the first row as it is not necessary 
mof_23_df = mof_23_df.iloc[1:,:]

print(mof_23_df.head())
print(league_23_df.head())

# Let's first just get our major leaguers from our team into one data frame, can deal 
# with minor leaguers as a separate problem 

# get a quick value count for the status column 
# print column names for our df 
print(mof_23_df.columns)
mof_majors_df = mof_23_df[mof_23_df['Status'] != 'Min']

# Let's take a look at the data 
print(mof_majors_df.head())
print(mof_majors_df.tail())

# now can test the value counts to see that it actually worked 
print(mof_majors_df['Status'].value_counts())

# last thing we want to do is to get a dataframe that just have active players, rather than a 
# bunch of free agents that aren't added to rosters 
print(league_23_df['Status'].value_counts())

# just want to get those that are not free agents 
active_players_df = league_23_df[league_23_df['Status'] != 'FA']

# printing test 
print(active_players_df.head())
print(active_players_df['Status'].value_counts())

# Let's try and implement the past 22 data, and then we can work into the 2024 projection data to get the most wholistic possible picture

# We'll try and import the 22 data now 
# This should be the 22 stats for the entire league 
league_22_df = pd.read_csv('/home/adbucks/Downloads/Fantrax-Players-SOBR FanTrax Mirror 22 Season.csv')

# can try and do the same for the 23 data now 
league_23_df = pd.read_csv('/home/adbucks/Downloads/Fantrax-Players-SOBR FanTrax Mirror 23 Season.csv')

# Taking a look to make sure the import worked 

print(league_22_df.head())
print(league_23_df.head())

'''

2. Data Analysis and Initial Feature Engineering

'''

# we'll start by getting a simple points per dollar metric 

# let's check the data types for our team and hten later the active players 

print(mof_majors_df.dtypes)
print(active_players_df.dtypes)

# Looks fine and we can start convering 
# We'll just do it raw and then can round later 

mof_majors_df['Points Per Dollar'] = mof_majors_df['fant_pts'] / mof_majors_df['Salary']
active_players_df['Points Per Dollar'] = active_players_df['FPts'] / active_players_df['Salary']

# Let's take a look at the data 

print(mof_majors_df.head())
print(active_players_df.head())

# we can also try and figure out what the distribution of active player points might be 
# and cna import the 2024 projection data to make this same determination re: point distribution 

# Now with our past data imported, we can work on joins and then feature Engineering 
# to get a more comprhehensive picture of the league and our team

# We can really trim these down to make the joins easier, there's also quite a bit of superfluous information in these prior csv's 

# We'll start by just getting the columns we need for the 22 and 23 data 
# Probably just want ID, name, overall rank, points, and team ownership 

league_22_df = league_22_df[['ID', 'Player', 'Team', 'Position', 'RkOv', 'Status',  'Age', 
                             'Salary', 'FPts', 'FP/G', 'ADP']]

# have to rename a few columns to make sure they are 22 points data 
league_22_df = league_22_df.rename(columns = {'FPts': 'FPts_22', 'FP/G': 'FP/G_22'})

# can do the same for the 23 data now 
league_23_df = league_23_df[['ID', 'Player', 'Team', 'Position', 'RkOv', 'Status',  'Age', 
                             'Salary', 'FPts', 'FP/G', 'ADP']]

# doing the same renaming to ensure they're included in the join 
league_23_df = league_23_df.rename(columns = {'FPts': 'FPts_23', 'FP/G': 'FP/G_23'})

# Let's take a look at the data 
print(league_22_df.head()) 
print(league_23_df.head()) 

# Now can join this to our original data 
# Left join to all players universe on the ID column should work 
# we'll do this for both the 22 and 23 data 
league_2223_df = pd.merge(league_23_df, league_22_df, on = 'ID', how = 'left')

# Let's take a look at the data now to make sure this worked 
print(league_2223_df.head())

# let's try and export to csv to quickly look at this data 
league_2223_df.to_csv('/home/adbucks/Downloads/league_2223.csv')

# we see there is some trimming we can do for the data 
# we'll do some renaming for the year-specific columns 
# we'll re-do the rank, ADP, and status columns to make sure they're year year-specific

league_2223_df = league_2223_df.rename(columns = {'RkOv_x': 'RkOv_23', 'Status_x': 'Status_23', 'ADP_x': 'ADP_23', 'RkOv_y': 'RkOv_22' ,'Status_y':'Status_22', 'ADP_y':'ADP_22'})

# Let's take a look at the data 
print(league_2223_df.head())
# check the dimension real quick 
print(league_2223_df.shape)

# taking another csv look 
league_2223_df.to_csv('/home/adbucks/Downloads/league_2223.csv')

# Now we'll get into columns that we can drop 
drop_columns = ['Team_x', 'Position_x', 'Age_x', 'Salary_x', 
                'Player_y', 'Team_y', 'Age_y', 'Salary_y']

# we'll drop these columns 
league_2223_df = league_2223_df.drop(columns = drop_columns)

# Let's take a look at the data 
print(league_2223_df.head())

league_2223_df.to_csv('/home/adbucks/Downloads/league_2223.csv')

# We can filter this points-centric data to just our team, and then active players 

# we'll start with our team 
mof_hist_data = league_2223_df[league_2223_df['Status_23'] == 'MOF']

# Let's take a look at the data 
print(mof_hist_data.head())

# Want to make sure these dimensions look right 
print(mof_hist_data.shape)

# We can now filter this for players that are on a roster as of 2023 
# just for fidelity to a distribution shape 
print(league_2223_df['Status_23'].value_counts())
active_players_23 = league_2223_df[league_2223_df['Status_23'] != 'FA']

# Let's take a look at the data 
print(active_players_23.head())

# Let's take a csv look for some roster cutting 
active_players_23.to_csv('/home/adbucks/Downloads/active_players_23.csv') 
mof_hist_data.to_csv('/home/adbucks/Downloads/mof_hist_data.csv')

'''

3. The Replacement Project

'''

# Let's first start by getting a position percentile for all players, so we can see how our team does and how "rare" each player is in terms of percentage 

# We'll start by getting the percentiles for each position 
# Let's start by renaming the position column, and then pull out the first position as 
# the primary position 

active_players_23 = active_players_23.rename(columns = {'Position_y': 'Position'}) 

# Let's take a look at the data 

print(active_players_23.head()) 

# Now we want to get the primary position 

#active_players_23['Primary Position'] = active_players_23['Position'].str.split('/').str[0] 
# trying another method 
def left(s, amount):
    return s[:amount]

# trying to make a left equivalent to redshift/SQL
# Trying this with our column now 
active_players_23['Primary Position'] = active_players_23['Position'].apply(lambda x: left(x, 2))

# Let's take a look at the data 
print(active_players_23.head()) 
print(active_players_23['Primary Position'].value_counts())

# Let's look at our catchers and test that this works as intended 
# Seems to work! 

# Now we can work on getting our percentiles by position 
# For our team specifically, let's look at starting pitchers and outfielders 
# We'll start with starting pitchers 

pitchers = active_players_23[active_players_23['Primary Position'] == 'SP'] 

# We'll try and get a percentile for '23 points scored now 

pitchers['Percentile_23'] = pitchers['FPts_23'].rank(pct = True) 
pitchers['Percentile_22'] = pitchers['FPts_22'].rank(pct = True)

# Let's take a look at the new column 
print(pitchers.head())
print(pitchers['Percentile_23'].describe())
print(pitchers['Percentile_23'].head())
print(pitchers['Percentile_23'].value_counts())

# Let's look at Yu Darvish 
print(pitchers[pitchers['Player_x'] == 'Yu Darvish'])

# Let's get a pitchers csv before moving to outfielders 

pitchers.to_csv('/home/adbucks/Downloads/pitchers.csv') 

# Now we can do the same for outfielders 

outfielders = active_players_23[active_players_23['Primary Position'] == 'OF'] 

# We'll try and get a percentile for '23 points scored now 

outfielders['Percentile_23'] = outfielders['FPts_23'].rank(pct = True) 
outfielders['Percentile_22'] = outfielders['FPts_22'].rank(pct = True) 

# Let's take a look at the new column 
print(outfielders.head()) 
print(outfielders['Percentile_23'].describe()) 
print(outfielders['Percentile_23'].head()) 
print(outfielders['Percentile_23'].value_counts()) 

# Let's look at Cedric Mullins 
print(outfielders[outfielders['Player_x'] == 'Cedric Mullins'])

# Let's get an outfielders csv before moving to the next position 

outfielders.to_csv('/home/adbucks/Downloads/outfielders.csv') 



