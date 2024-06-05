import pandas as pd 
import numpy as np 

# We are going to take in 'scraped' rest of season pitcher ranking data and try and 
# present it in a more readable format.

# Read in the data  

df_raw = pd.read_csv('/home/adbucks/Downloads/PitcherRankTest.csv' , header = None)

# we want to just grab the even numbered rows as the names of the pitchers as its 
# own new column 

df_raw['Pitcher'] = df_raw.iloc[::2]
# now we want the odd numbered rows as the descriptions of the pitchers 

#df_raw['Pitcher Notes'] = df_raw.iloc[1::2]

print(df_raw.head())

# maybe can try to build a new data frame like this 
df_clean = pd.DataFrame(columns = ['Pitcher'] , data = df_raw['Pitcher'])

print(df_clean.head())

# now we ought to drop every other row 

df_clean = df_clean.drop(df_clean.index[1::2])

print(df_clean.head())

# now we want to reset the index

df_clean = df_clean.reset_index(drop = True)

print(df_clean.head())

# this now gives what we want in terms of the pitcher names, we can now add a rank column 
# and then finally Sarris' notes 

df_clean['Sarris RoS Rank'] = np.arange(1, len(df_clean) + 1) 

print(df_clean.head())

# we can try and pull the previous rank as well to get a rank delta and then that should be 
# enough 

print(df_raw.head(15))

# the previous rank is the number before 'Last' in each case, so we can try and extract the 
# number knowing that 

df_raw['Notes'] = df_raw.iloc[1::2, 0]

print(df_raw.head())

# let's just get this in a csv and look at it in excel 

df_raw.to_csv('/home/adbucks/Downloads/Pitcher_clean_test.csv')

# This seems to work now we just need to yank out the first 1-3 digits as a new column 

# just do as a separate array for now 

print(df_raw['Notes'].head())

# we just waant at first every other row, and then we can extract the string

prev_rank = df_raw['Notes'].iloc[1::2]

print(prev_rank.head())

# now we just want everything before 'last'

prev_rank_test = prev_rank.str.extract(r'(\d+)') 

print(prev_rank_test.head())

# maybe need to reset the index 

prev_rank_test = prev_rank_test.reset_index(drop = True)

print(prev_rank_test.head())

# think we might be able to slap this on our new data frame and call it a day 

df_clean['Previous Rank'] = prev_rank_test 

print(df_clean.head()) 

print(len(prev_rank_test))
print(len(df_clean.iloc[:, 0]))

# now we can calculate the rank delta
# some quick data coercion 
df_clean['Previous Rank'] = df_clean['Previous Rank'].astype(int)
df_clean['Sarris RoS Rank'] = df_clean['Sarris RoS Rank'].astype(int)

df_clean['Rank Delta'] = df_clean['Previous Rank'] - df_clean['Sarris RoS Rank']

print(df_clean.head())

# now we can just write this to a csv and call it a day 

df_clean.to_csv('/home/adbucks/Downloads/Pitcher_clean.csv')



