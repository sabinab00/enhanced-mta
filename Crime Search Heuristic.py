#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd
crime = pd.read_csv(r'NYPD dataset.csv', index_col=False)

#preprocessing 
crime = crime[crime.BORO_NM != 'BRONX']
crime = crime[crime.BORO_NM != 'BROOKLYN']
crime = crime[crime.BORO_NM != 'QUEENS']
crime = crime[crime.BORO_NM != 'STATEN ISLAND']
crime = crime.dropna()

#rename to geocode
crime = crime.rename(columns = {'Lat_Lon':'Geocode'})
crime



# In[33]:


#checks to see if given geocode matches with crime geocode
code = '(40.77950599700006, -73.95558550399994)'
for i in crime.Geocode:
    if code == i:
        print("not safe")
        break


# In[ ]:


def crime_check(curr_stop:Node):
    ''' 
    Checks if location is safe given geocode of stop
    '''
    
    heuristic = 0
    
    if curr_stop.geocode == crime.Geocode:
        # checks for the same geocode id
        for i in crime.Geocode:
            if code == i:
            print("Not safe")
            break
        heuristic += .025
    return heuristic

