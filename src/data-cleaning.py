#%%
import numpy as np
import pandas as pd
import datetime
import json


#%%
apartments = pd.read_csv("../data/apartments_sale_east_riyadh.csv")
# drop old index
apartments.drop(columns=['Unnamed: 0'], inplace=True)
# drop attribute with all na values
apartments.drop(columns=['rent_period', 'type', 'native'], inplace=True)
# drop attributes with 0 variability
apartments.drop(columns=['city', '__typename', 'category'], inplace=True)
# drop duplicate attribute
apartments.drop(columns=['refresh'], inplace=True)


#%%
# transform ['last_update', 'create_time'] from int to datetime 
date_col = ['last_update', 'create_time']
for col in date_col:
    apartments[col] = apartments[col].apply(datetime.datetime.fromtimestamp)

#%%
# create an attribute for the time the apartment has been on the market
apartments['time_on_market'] = apartments.apply(lambda row: 
    row['last_update'] - row['create_time'], axis=1)   

#%%
apartments['location'] = apartments.location.apply(lambda s: json.loads(s.replace("\'", "\""))) 

latitude = []
longitude = []

for location in apartments.location:
    latitude.append(location['lat'])
    longitude.append(location['lng'])

apartments['latitude'] = latitude
apartments['longitude'] = longitude

# apartments.drop(columns="location")


#%%
apartments.to_csv("../data/apartments_sale_east_riyadh_cleaned.csv", index=False)





# %%
