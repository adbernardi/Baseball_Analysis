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

# we'll want to look at all pitchers, all outfielders, to get a sense of the distribution and then 
# how our FA money can be best spent tomorrow 

# First, let's see the total points distribution for all players, of pitchers and outfielders for 2023 and 22 data 

# We'll start with pitchers 
# Active players first and then we'll check everyone 

# We'll start with 2023 data 
# Density plot of points for pitchers in 2023 
 
plt.figure(figsize = (10, 10)) 
plt.hist(pitchers['FPts_23'], bins = 50, alpha = 0.5, label = '2023') 
plt.hist(pitchers['FPts_22'], bins = 50, alpha = 0.5, label = '2022') 
plt.legend(loc = 'upper right') 
#plt.show() 

# Let's get some value counts 
print(pitchers.head())

print(pitchers['FPts_23'].describe())
print(pitchers['FPts_22'].describe())

# want to print the column names 
print(pitchers['Status_23'].value_counts())

# Let's try and find some targets that might be good for our team 
# We'll start with the 2023 data 
# We'll start with the top 10% of pitchers in 2023 
top_10_23 = pitchers[pitchers['Percentile_23'] > 0.9] 
 
# Let's try and get a distribution of the outfielders also 
print(outfielders['FPts_23'].describe())

# Plotting for the outfielders now 
plt.figure(figsize = (10, 10)) 
plt.hist(outfielders['FPts_23'], bins = 50, alpha = 0.5, label = '2023') 
plt.hist(outfielders['FPts_22'], bins = 50, alpha = 0.5, label = '2022') 
plt.legend(loc = 'upper right') 
#plt.show()

# Let's try and replot with a point cutoff 
outfielders_no_outliers = outfielders[outfielders['FPts_23'] > 150]

# replotting 
plt.figure(figsize = (10, 10)) 
plt.hist(outfielders_no_outliers['FPts_23'], bins = 50, alpha = 0.5, label = '2023') 
plt.hist(outfielders_no_outliers['FPts_22'], bins = 50, alpha = 0.5, label = '2022') 
plt.legend(loc = 'upper right') 
#plt.show()

# Let's try and get some names of the 350-400 point outfielders 

#print(outfielders_no_outliers[outfielders_no_outliers['FPts_23'] > 350])

# Let's get all of our helpful csv's out, pull in the 2024 projections, and then we can start to make decisions 

active_players_23.to_csv('/home/adbucks/Downloads/active_players_23.csv')


'''

4. The 2024 Projections 

'''

# we start by reading in projections, getting them for active players, and then joining to attempt to make some FA decisions 

# reading in the 24 projections 

league_24_projdf = pd.read_csv('/home/adbucks/Downloads/Fantrax-Players-SOBR FanTrax Mirror 2024_proj.csv')

print(league_24_projdf.head())

# drop the rostered column, and can get only the active players 
league_24_projdf.drop(columns = 'Ros', inplace = True)

# active players only 
active_players_24 = league_24_projdf[league_24_projdf['Status'] != 'FA'] 

# Let's try and get a sense of the distribution of points for all players, and then we can look at some targets, that sort of thing 

plt.figure(figsize = (10, 10))
plt.hist(active_players_24['FPts'], bins = 50, alpha = 0.5, label = '2024')
plt.legend(loc = 'upper right')
#plt.show()

print(active_players_24['Status'].value_counts())

# let's just pull out the 0's as this is surely minor leaguers and injured pitchers 
active_players_24 = active_players_24[active_players_24['FPts'] > 0] 

# try taking another look at the distribution 
plt.figure(figsize = (10, 10))
plt.hist(active_players_24['FPts'], bins = 50, alpha = 0.5, label = '2024') 
plt.legend(loc = 'upper right') 
#plt.show()

# Looks slightly bi-modal, but let's try and zero in on an outfielder and a pitcher 
# Focus on free agents that are projected to score real points (i.e. not minor leaguers)

fa_targets = league_24_projdf[league_24_projdf['Status'] == 'FA']

# Let's take a look at the data 

print(fa_targets.head()) 

# Cut out the minor leaguers and the injured arms 

fa_targets = fa_targets[fa_targets['FPts'] > 0] 

# Let's zero in on an outfielder 
# We'll re-use the primary position code to just get the one position 

fa_targets['Primary Position'] = fa_targets['Position'].apply(lambda x: left(x, 2)) 

# Let's take a look at the data 

print(fa_targets.head()) 
print(fa_targets['Primary Position'].value_counts())

of_fa = fa_targets[fa_targets['Primary Position'] == 'OF'] 

# Let's take a look at the data 

print(of_fa.head()) 

# Let's try and get a sense of the distribution of points for outfielders 

plt.figure(figsize = (10, 10)) 
plt.hist(of_fa['FPts'], bins = 50, alpha = 0.5, label = '2024') 
plt.legend(loc = 'upper right') 
#plt.show()

# Want to grab some summary statistics 
print(of_fa['FPts'].describe())
 
# Out of a regular starter we should want at least 300 points, so let's try and get some names of those that are projected to score at least 300 points 

print(of_fa[of_fa['FPts'] > 300]) 

# Variance is huge for all outfielders, so maybe if we narrow the targets down somewhat that might change 

of_targets = of_fa[of_fa['FPts'] > 300] 

# Let's take a look at the data 

print(of_targets['FPts'].describe())

# seems a bit more promising, let's plot and then export to a csv 

plt.figure(figsize = (10, 10)) 
plt.hist(of_targets['FPts'], bins = 50, alpha = 0.5, label = '2024') 
plt.legend(loc = 'upper right') 
# plt.show() 

# Let's get a csv of the outfield targets 
of_targets.to_csv('/home/adbucks/Downloads/of_targets.csv') 

# we'll pull in past data and then can manually input their current price on the market to try and find a deal 
# And then can recycle all of the code for pitchers 

# left join with the 2023 and 22 points with the 24 projections 

of_targets_test = pd.merge(of_targets, league_2223_df, on = 'ID', how = 'left')

# Let's take a look at the data 

print(of_targets_test.head()) 

print(of_targets.shape)
print(of_targets_test.shape)

of_targets_test.to_csv('/home/adbucks/Downloads/of_targets_test.csv')

# Now let's do the same for pitchers 

sp_fa = fa_targets[fa_targets['Primary Position'] == 'SP'] 

# Let's take a look at the data 

print(sp_fa['FPts'].describe())

# Let's try and get a sense of the distribution of points for starting pitchers 

plt.figure(figsize = (10, 10))
plt.hist(sp_fa['FPts'], bins = 50, alpha = 0.5, label = '2024') 
plt.legend(loc = 'upper right') 
# plt.show() 

# Pitchers might be harder, let's say we want at least 300 points for a regular starter 

sp_targets = sp_fa[sp_fa['FPts'] > 300] 

# Let's take a look at the data 

print(sp_targets['FPts'].describe())

print(sp_targets.head())

# Let's do the same join we did for the outfielders 

sp_targets_test = pd.merge(sp_targets, league_2223_df, on = 'ID', how = 'left') 

print(sp_targets_test.head())
print(sp_targets.shape)
print(sp_targets_test.shape)

sp_targets_test.to_csv('/home/adbucks/Downloads/sp_targets_test.csv')


'''

print(of_targets_test.head()) 

print(of_targets.shape)
print(of_targets_test.shape)

of_targets_test.to_csv('/home/adbucks/Downloads/of_targets_test.csv')

'''

# Side project -- What is a 400 point pitcher worth?

league_2223_df.to_csv('/home/adbucks/Downloads/league_2223.csv')


