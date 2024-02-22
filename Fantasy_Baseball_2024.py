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



