#%%
import numpy as np
import pandas as pd
import datetime
import json
from pandas_profiling import ProfileReport
import time
from sklearn.impute import KNNImputer
import os


#%%
# load data
os.chdir("/Users/mo/Desktop/DSI/Aqar_Capstone/src")

apartments_east = pd.read_csv("../data/apartments_sale_east_riyadh.csv")
apartments_middle = pd.read_csv("../data/apartments_sale_middle_riyadh.csv")
apartments_west = pd.read_csv("../data/apartments_sale_west_riyadh.csv")
apartments_north = pd.read_csv("../data/apartments_sale_north_riyadh.csv")
apartments_south = pd.read_csv("../data/apartments_sale_south_riyadh.csv")

# a column to encode where the apartment is located
apartments_east['city_side'] = "east"
apartments_middle['city_side'] = "middle"
apartments_west['city_side'] = "west"
apartments_north['city_side'] = "north"
apartments_south['city_side'] = "south"

dataframes_list = [apartments_north, apartments_south,
                   apartments_east, apartments_west, 
                   apartments_middle]

# combine the dataframes
apartments = pd.concat(dataframes_list, axis=0, ignore_index=True)

# drop duplicates
apartments.drop_duplicates(inplace=True)

#%%
# drop old index
apartments.drop(columns=['Unnamed: 0'], inplace=True)
# drop attribute with all na values
apartments.drop(columns=['rent_period', 'type', 'native', 'ac'], inplace=True)
# drop attributes with 0 variability
apartments.drop(columns=['city', '__typename', 'category'], inplace=True)
# drop duplicate attribute
apartments.drop(columns=['refresh', 'user'], inplace=True)


#%%

apartments[['livings', 'street_width', 'age', 'ketchen', 'furnished', 'length', 'width']] = apartments[['livings', 'street_width', 'age', 'ketchen', 'furnished', 'length', 'width']].apply(lambda ser: 
    np.floor(pd.to_numeric(ser, errors='coerce')).astype('Int64'))


#%%
# add district English names

# getting English district names from neighborhood file
with open(r"../data/riyadh_districts.json", 'r', encoding='utf8', errors='ignore') as file:
    neighborhood = json.load(file)
    
ar_name = []
en_name = []
for i in range(len(neighborhood)):
    ar_name.append(neighborhood[i]["name_ar"])
    en_name.append(neighborhood[i]["name_en"])

# district_df = pd.DataFrame(ar_name, columns=['name_ar'])
# district_df["name_en"] = en_name

# add districts not in neighborhood file
ar_name = ar_name + ['حي ظهرة نمار', 'حي عرقة', 'حي مطار الملك خالد الدولي',
                     'حي جامعة الملك سعود', 'حي خشم العان']

en_name = en_name + ['Dahrat Nimar Dist.', 'Arga Dist.', 
                     'King Khalid International Airport Dist.',
                     'King Saud University Dist.', 'Khashm Alan']

district_dict = dict(zip(ar_name, en_name))

apartments['district_en'] = apartments['district'].apply(lambda dstrct: district_dict[dstrct] if dstrct in district_dict.keys() else None)



#%%
# transform ['last_update', 'create_time'] from int to datetime 
date_col = ['last_update', 'create_time']
for col in date_col:
    apartments[col] = apartments[col].apply(datetime.datetime.fromtimestamp)

#%%
# create an attribute for the time the apartment has been on the market
time_now = time.time()
apartments['time_on_market'] = apartments.apply(lambda row: 
    datetime.datetime.fromtimestamp(time_now) - row['create_time'], axis=1)   

# create an attribute for the time since the apartment post was last updated
apartments['time_since_update'] = apartments.apply(lambda row: 
    datetime.datetime.fromtimestamp(time_now) - row['last_update'], axis=1)   


#%%
# create "year", "month", and "day" features for each datetime feature
    
def extract_time(datetime_ser:pd.Series, name):
    year = datetime_ser.apply(lambda x: x.year)
    month =datetime_ser.apply(lambda x: x.month)
    day = datetime_ser.apply(lambda x: x.day)
    hour = datetime_ser.apply(lambda x: x.hour)
        
    return pd.DataFrame({f'{name}_year':year,
                         f"{name}_month":month,
                         f"{name}_day":day,
                         f"{name}_hour":hour})

apartments = pd.concat([apartments, extract_time(apartments.last_update, 'last_update')], axis=1)
apartments = pd.concat([apartments, extract_time(apartments.create_time, 'create_time')], axis=1)

apartments['time_on_market'] = apartments.time_on_market.apply(lambda x: x.days)
apartments['time_since_update'] = apartments.time_since_update.apply(lambda x: x.days)

apartments.drop(columns=['last_update', 'create_time'], inplace=True)




#%%
# extract latitude and longitude from location 
apartments['location'] = apartments.location.apply(lambda s: json.loads(s.replace("\'", "\""))) 

latitude = []
longitude = []

for location in apartments.location:
    latitude.append(location['lat'])
    longitude.append(location['lng'])

apartments['latitude'] = latitude
apartments['longitude'] = longitude

# drop duplicate columns
apartments.drop(columns="location", inplace=True)

#%% 
# create an attribute for the ratio between the length and width of the apartment
apartments['squareness'] = apartments.apply(lambda row: 
    row['width'] / row['length'] if (row['width'] < row['length'])
    else row['length'] / row['width'], axis=1) 


# create an attribute for how close the shape of the apartment is to a rectangular shape
apartments['regular_shapeness'] = apartments.apply(lambda row: 
    row['area'] / (row['width'] * row['length']), axis=1) 

#%%
# apartments['num_imgs'] = apartments.apply(lambda row: len(list(row['imgs'])) if type(row['imgs']) == str else 0, axis=1)
needless_features = ['uri', 'title', 'content', 'imgs', 'path']
apartments.drop(columns=needless_features, inplace=True)
#%%
# drop the apartment with the highest price value
# because it appears not to be a genueine ad 
apartments.drop(apartments.price.idxmax(), axis=0, inplace=True)

# drop the apartment with the lowest price value
# an apartment for sale for 600 SR?
apartments.drop(apartments.price.idxmin(), axis=0, inplace=True)

percentile_99th = apartments.price.quantile(0.99)
apartments_exc = apartments.loc[apartments.price < percentile_99th]



#%%
# write csv files
# apartments.to_csv("../data/apartments_sale_riyadh_cleaned.csv", index=False)
# apartments_exc.to_csv("../data/apartments_sale_riyadh_cleaned_exclusive.csv", index=False)


