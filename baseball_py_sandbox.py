'''

Making a sandbox code file just to play around with pybaseball package and other baseball data sources.

'''
'''

1. Data Importing and Cleaning

'''

# Importing necessary packages 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from pybaseball import statcast 

# Time to do some looking around
# I wonder, what makes a good reliever? What makes a good pitcher, in general? 
# Let's take a look. 
# We'll look at May, enough time to get warmed up, but lower chances of arm injuries, as might be common later in the season 

pitching_data = statcast(start_dt = '2023-05-01', end_dt = '2023-05-31')
print(pitching_data.head())
print(pitching_data.shape)
print(pitching_data.columns) 

# Just trying to get a better sense of how this data works and how it is structured. 
print(pitching_data['pitch_type'].value_counts())
print(pitching_data['player_name'].value_counts())

# It seems like we can do some unsupervised learning and clustering stuff, along with some 
# PCA stuff, see what makes pitchers elite, and if anything stands out about 'non-obvious' pitchers (i.e. Not Spencer Strider or Gerrit Cole)





