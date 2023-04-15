#%%
import requests
import numpy as np
import pandas as pd
from time import sleep
import warnings 
import datetime
import time
import json
from ml_models import train_and_predict
#%%



def find_post(apartments, desired_post_id):
    """ collects data associated with the apartment
    with the given post ID

    Args:
        apartments (pd.DataFrame): contains all apartments 
        desired_post_id (int): the post ID

    Returns:
        pd.DataFrame or string: dataframe of the apartment or 'Search failed'
    """
    if desired_post_id in list(apartments.id):
        # desired_apartment = pd.DataFrame(apartments.loc[apartments.id == desired_post_id].iloc[0],
        #                                  columns=apartments.columns)
        desired_apartment = apartments.loc[apartments.id == desired_post_id]
        
        
        # drop to_be_predicted apartment from apartments dataset to avoid data leak
        apartments.drop(apartments[apartments.id == desired_post_id].index, inplace=True)
        clean = True
        # assert desired_apartment.shape[0] == 1
        return desired_apartment, clean
    
    FIRST_PAGE = 0
    i = FIRST_PAGE
    all_listings = pd.DataFrame([])

    cookies = {
        '_ga': 'GA1.2.1278248909.1659285193',
        '_gid': 'GA1.2.1862803336.1660289756',
        '_gac_UA-52229618-6': '1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE',
        'AWSALBTG': 'foXxUgV+1XpnEh3LXPIBZKVqV79Hq8jAoJivEyXBOOSvjJ7MK+zmtK1lQIJytYj1EKSPIJ929+d3tGcGdWuNJOrER8dKWLVkMmK3v5O676cCWsNfG6cFysFFlcir8pWC8xVAEwGkMftQeGMusLU/Iquea5yHLazpr/MKeTd7HPUadu7xDNg=',
        'AWSALBTGCORS': 'foXxUgV+1XpnEh3LXPIBZKVqV79Hq8jAoJivEyXBOOSvjJ7MK+zmtK1lQIJytYj1EKSPIJ929+d3tGcGdWuNJOrER8dKWLVkMmK3v5O676cCWsNfG6cFysFFlcir8pWC8xVAEwGkMftQeGMusLU/Iquea5yHLazpr/MKeTd7HPUadu7xDNg=',
    }

    headers = {
        'authority': 'sa.aqar.fm',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,hmn;q=0.8,ar;q=0.7,nl;q=0.6',
        'app-version': '0.16.18',
        'dpr': '0.666667',
        'origin': 'https://sa.aqar.fm',
        'referer': 'https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/1',
        'req-app': 'web',
        'req-device-token': '33e28a14-0941-41b1-b2a1-68e1304e76d8',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'viewport-width': '1257',
    }
    while True:
        try:
            json_data = {
                'operationName': 'findListings',
                'variables': {
                    'size': 20,
                    'from': i, # where to search
                    'sort': {
                        'create_time': 'desc',
                        'has_img': 'desc',
                    },
                    'where': {
                        'category': {
                            'eq': 6, # 6: 'for sale', Aqar encoding
                        },
                        'city_id': {
                            'eq': 21,  # 21: 'Riyadh', Aqar encoding
                        },
                    },
                },
                'query': 'query findListings($size: Int, $from: Int, $sort: SortInput, $where: WhereInput, $polygon: [LocationInput!]) {\n  Web {\n    find(size: $size, from: $from, sort: $sort, where: $where, polygon: $polygon) {\n      ...WebResults\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WebResults on WebResults {\n  listings {\n    user_id\n    id\n    uri\n    title\n    price\n    content\n    imgs\n    refresh\n    category\n    beds\n    livings\n    wc\n    area\n    type\n    street_width\n    age\n    last_update\n    street_direction\n    ketchen\n    ac\n    furnished\n    location {\n      lat\n      lng\n      __typename\n    }\n    path\n    user {\n      review\n      img\n      name\n      phone\n      iam_verified\n      rega_id\n      __typename\n    }\n    native {\n      logo\n      title\n      image\n      description\n      external_url\n      __typename\n    }\n    rent_period\n    city\n    district\n    width\n    length\n    advertiser_type\n    create_time\n    __typename\n  }\n  total\n  __typename\n}\n',
            }

            response = requests.post('https://sa.aqar.fm/graphql', cookies=cookies, headers=headers, json=json_data)
            clean = False
            
            # a webpage containing 20 apartment listings and other elements
            response_json = response.json()
            # getting relevant information
            listings_list = response_json.get('data').get('Web').get('find').get('listings')

            listings_list = pd.DataFrame(listings_list)
            # print(listings_list.shape)
            # print(f"i = {i}")
            # appending listings from different pages to one dataframe
            if i != 0:
                if list(all_listings.iloc[0])[1] ==list(listings_list.iloc[0])[1]:
                    print("here is the problem")
                    mesege = i 
                    break
                        
            all_listings = all_listings.append(listings_list, ignore_index=True)
            if desired_post_id in list(listings_list['id']):
                return pd.DataFrame(listings_list.loc[listings_list['id'] == desired_post_id], columns=apartments.columns), clean
            elif i >= 500:
                return "Search failed", clean
            
            sleep(0.5)
            i+=20
        except:
            return "Search failed", clean
        


#%%
def clean_post(to_predict:pd.DataFrame, district_city_part:pd.DataFrame):
    """
    cleans a raw web-scraped dataframe to a clean dataframe
    with the same features as apartments

    Args:
        to_predict (pd.DataFrame): the dataframe that will be cleaned
        district_city_part (pd.DataFrame): dataframe with districts 
                                in a city and the city parts they are located

    Returns:
        pd.DataFrame: cleaned to_predict dataframe
    """
    
    
    to_predict = to_predict.drop(columns=['rent_period', 'type',
                                          'native', 'ac', 'city', '__typename',
                                          'category', 'refresh', 'user'], inplace=False)
    
    to_predict[['livings', 'street_width', 'age', 'ketchen', 'furnished', 
                'length', 'width']] = to_predict[['livings', 'street_width', 
                                                  'age', 'ketchen', 'furnished',
                                                  'length', 'width']].apply(
                                                      lambda ser: ser.astype('Int64', errors='ignore'))
    
    

    # get the city side of the district the apartment is in 
    to_predict = to_predict.merge(district_city_part, left_on="district", right_on="district")
    try:
        to_predict['city_side'] = district_city_part.loc[district_city_part.district
                                                         == to_predict.district.iloc[0]].iloc[0]['city_side']
    except:
        print("The district was not found!")
        to_predict['city_side'] = np.nan
    
    # district_english 
    to_predict = get_district_english(to_predict)
    
    # create additional time featuers and fix existing ones
    to_predict = create_time_features(to_predict)
    
    # longitude and latitude  
    to_predict = extract_coordinates(to_predict)

    # additional length and width-related features
    to_predict = create_squareness_and_regular_shapeness(to_predict)
    
    needless_features = ['uri', 'title', 'content', 'imgs', 'path']
    to_predict = to_predict.drop(columns=needless_features)
    
    return to_predict



def get_district_english(apartments):
    # getting English district names from neighborhood file
    with open(r"../data/riyadh_districts.json", 'r', encoding='utf8', errors='ignore') as file:
        neighborhood = json.load(file)
        
    ar_name = []
    en_name = []
    for i in range(len(neighborhood)):
        ar_name.append(neighborhood[i]["name_ar"])
        en_name.append(neighborhood[i]["name_en"])

    # add districts not in neighborhood file
    ar_name = ar_name + ['حي ظهرة نمار', 'حي عرقة', 'حي مطار الملك خالد الدولي',
                        'حي جامعة الملك سعود', 'حي خشم العان']

    en_name = en_name + ['Dahrat Nimar Dist.', 'Arga Dist.', 
                        'King Khalid International Airport Dist.',
                        'King Saud University Dist.', 'Khashm Alan']

    district_dict = dict(zip(ar_name, en_name))

    apartments['district_en'] = apartments['district'].apply(
        lambda dstrct: district_dict[dstrct] if dstrct in district_dict.keys() else None)
    
    return apartments
                                                  
                                                  
# create "year", "month", and "day" features for each datetime feature
def extract_time(datetime_ser:pd.Series, name):
    # datetime_ser = pd.Series(pd.DatetimeIndex(datetime_ser))
    
    year = datetime_ser.apply(lambda x: x.year)
    month =datetime_ser.apply(lambda x: x.month)
    day = datetime_ser.apply(lambda x: x.day)
    hour = datetime_ser.apply(lambda x: x.hour)
        
    return pd.DataFrame({f'{name}_year':year,
                         f"{name}_month":month,
                         f"{name}_day":day,
                         f"{name}_hour":hour})                                
                                
                                
def create_time_features(apartments):
    # transform ['last_update', 'create_time'] from int to datetime 
    date_col = ['last_update', 'create_time']
    for col in date_col:
        apartments[col] = apartments[col].apply(datetime.datetime.fromtimestamp)
    
    # create an attribute for the time the apartment has been on the market
    time_now = time.time()
    apartments['time_on_market'] = apartments.apply(lambda row: 
        datetime.datetime.fromtimestamp(time_now) - row['create_time'], axis=1)   

    # create an attribute for the time since the apartment post was last updated
    apartments['time_since_update'] = apartments.apply(lambda row: 
        datetime.datetime.fromtimestamp(time_now) - row['last_update'], axis=1)   


    apartments = pd.concat([apartments, extract_time(apartments.last_update, 'last_update')], axis=1)
    apartments = pd.concat([apartments, extract_time(apartments.create_time, 'create_time')], axis=1)

    apartments['time_on_market'] = apartments.time_on_market.apply(lambda x: x.days)
    apartments['time_since_update'] = apartments.time_since_update.apply(lambda x: x.days)

    apartments.drop(columns=['last_update', 'create_time'], inplace=True)
    
    return apartments


def extract_coordinates(apartments):
    # extract latitude and longitude from location 
    # apartments['location'] = apartments.location.apply(lambda s: json.loads(s.replace("\'", "\""))) 

    latitude = []
    longitude = []

    for location in apartments.location:
        latitude.append(location['lat'])
        longitude.append(location['lng'])

    apartments['latitude'] = latitude
    apartments['longitude'] = longitude

    # drop duplicate columns
    apartments.drop(columns="location", inplace=True)
    
    return apartments

def create_squareness_and_regular_shapeness(apartments):
    # create an attribute for the ratio between the length and width of the apartment
    try:
        apartments['squareness'] = apartments.apply(lambda row: 
            row['width'] / row['length'] if (row['width'] < row['length'])
            else row['length'] / row['width'], axis=1) 


        # create an attribute for how close the shape of the apartment is to a rectangular shape
        apartments['regular_shapeness'] = apartments.apply(lambda row: 
            row['area'] / (row['width'] * row['length']), axis=1) 

        return apartments 
    except:
        apartments['regular_shapeness'] = np.nan
        apartments['squareness'] = np.nan
        return apartments
    
    
    return apartments
def get_deal_goodness(predicted_price, real_price):   
    """
    returns an assessment of the goodness of a deal based
    on the ratio of predicted_price to real_price

    Args:
        predicted_price (integer): the price as predicted by ML model
        real_price (integer): the price as posted on Aqar

    Returns:
        string: one of {'great deal','good deal', 'fair deal',
        'bad deal', 'terrible deal'}
    """
    price_ratio = real_price / predicted_price   

    if price_ratio < 0.8:
        deal_goodness = "Greate Deal"
    elif price_ratio < 0.9:
        deal_goodness = "Good Deal"
    elif price_ratio > 0.9 and price_ratio < 1.1:
        deal_goodness = "Fair Deal"
    elif price_ratio > 1.2:
        deal_goodness = "Terrible Deal"
    elif price_ratio > 1.1:
        deal_goodness = "Poor Deal"
        
    return deal_goodness
        

#%%
def good_deal_indicator(apartments, desired_post_id):
    """
    determines whether the stated price of an apartment is
    higher than the ML model predicts

    Args:
        apartments (pd.DataFrame): contains all apartments in dataset
        desired_post_id (integer): the post ID that can be found in Aqar

    Returns:
        string: one of {'great deal','good deal', 'fair deal', 'bad deal', 'terrible deal'}
        if search for apartment with specified post ID can be found, or 'Search failed'
    """
    apartments_copy = apartments.copy()
    to_predict_raw, clean = find_post(apartments, desired_post_id)
    
    if type(to_predict_raw) == str and to_predict_raw == "Search failed":
        return "Post could not be found"
    elif clean:
        to_predict_clean = to_predict_raw
    else:
        to_predict_clean = clean_post(to_predict_raw, apartments_copy[['district', 'city_side']])
        
    # drop district names in Arabic and post ID
    apartments_copy.drop(columns=["district", 'id'], inplace=True)
    to_predict_clean.drop(columns=["district", 'id'], inplace=True)   
        
    predicted_price, asking_price = train_and_predict(apartments_copy, to_predict_clean)

    deal_goodness = get_deal_goodness(predicted_price, asking_price)
    
    return deal_goodness, asking_price, predicted_price

# %%
# apartments = pd.read_csv("../data/apartments_sale_riyadh_cleaned.csv")
# print(good_deal_indicator(apartments, 4403633))