#!/usr/bin/env python
# coding: utf-8

# # An Exploratory Analysis of NYC Yellow Taxis (June 2017)

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv('yellow_tripdata_2017-06.csv')
df.head()


# In[3]:


df.describe()


# In[4]:


#Datatype of each column
#df.info()


# In[5]:


#If any, how many fields with missing data in each column
#df.isnull().sum() 


# In[6]:


#Read in taxi zone lookup table
zone_df = pd.read_csv('taxi+_zone_lookup.csv')
zone_df.head()


# ## Imagine that you decide to drive a taxi for 10 hours each week to earn a little extra money. Explain how you would approach maximizing your income as a taxi driver.
# 
# To maximize my income considering limited time, I will opt to drive at a location and time with high demand. This is to ensure that occupancy of my taxi is almost guaranteed for the time I drive.

# In[7]:


#Convert the datatime columns from string to datatime data type to allow for aggregation by days and hours
df["pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
df["dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])

df["pickup_day"] = df["pickup_datetime"].dt.weekday_name
df["pickup_hour"] = df["pickup_datetime"].dt.hour

df["dropoff_day"] = df["dropoff_datetime"].dt.weekday_name
df["dropoff_hour"] = df["dropoff_datetime"].dt.hour


# In[8]:


#Trip data with new columns
df.head()


# In[9]:


#Number of pickups and dropoffs per day of the week to enable me decide which day will be best for work
PU_day_agg = df[["pickup_datetime", "pickup_day"]].groupby("pickup_day").count()
DO_day_agg = df[["dropoff_datetime", "dropoff_day"]].groupby("dropoff_day").count()
daily_agg = pd.concat([PU_day_agg, DO_day_agg], axis = 1).reset_index()


ax = daily_agg.plot(x='index', y=['pickup_datetime', 'dropoff_datetime'], kind='bar', style="-o", figsize=(15,5))
ax.set_ylabel("Number of trips")
ax.set_xlabel("Day of Week")
plt.show()


# In[10]:


#Number of pickups and dropoffs per hour of the day to enable me decide which hours are best on the days I decide to 
#work based on the plot above

PU_hr_agg = df[["pickup_datetime", "pickup_hour"]].groupby("pickup_hour").count()
DO_hr_agg = df[["dropoff_datetime", "dropoff_hour"]].groupby("dropoff_hour").count()
hr_agg = pd.concat([PU_hr_agg, DO_hr_agg], axis = 1).reset_index()

ax = hr_agg.plot(x='index', y=['pickup_datetime', 'dropoff_datetime'], kind='line', style="-*", figsize=(15,5))
ax.set_ylabel("Number of trips")
ax.set_xticks(hr_agg["index"].values) 
ax.set_xlabel("Hour of Day")
plt.show()


# In[11]:


#Location with most pickups
PU_Loc_agg = df[["pickup_datetime", "PULocationID"]].groupby("PULocationID").count()
PU_Loc_agg = PU_Loc_agg.reset_index().sort_values('pickup_datetime', ascending=False).head(10)
top_pickup_loc = zone_df.loc[zone_df['LocationID'].isin(PU_Loc_agg["PULocationID"])]


# In[12]:


#Top 10 Locations with high demand
top_pickup_loc


# With a limited 10 hours per week, my goal with be to work when the demand for taxia is high. This is so that there will be no extended periods with a passenger in the taxi. From the analysis above, it can be seen that Thurdays and Fridays are the days with the most demand. Demand for taxis are highest between 5pm and 10pm and the location 

# In[13]:


"""
#Select the top 10 pick up zones using SQL subquery
SELECT * 
FROM zone_df
WHERE LocationID IN (
        SELECT count(pickup_datetime)
        FROM df
        GROUP BY PULocationID
        ORDER BY count(pickup_datetime)
        LIMIT 10;
);
"""


# ## If you could enrich the dataset, what would you add? Is there anything in the dataset that you don’t find especially useful?

# Attempts at enriching the dataset can include:
#     - Identifying and removing outliers as necessary
#     - Checking for and handling missing values
#     - Find other data sources with data such such as longitide and latitude for pickup and dropoff zones to allow more pinpoint description.
#     - Differentiate FHV rides YT rides
#         
# I find all variables in the data set to be useful in someway, although not all were useful for this task. For example, tip amount and payment type. However, a closer look at tip amount can tell what time of the day passengers tend to tip more. Is it during commutes to work or during happy hours after relaxing with friends?

# In[ ]:




