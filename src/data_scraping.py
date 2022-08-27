#%%
import requests
import numpy as np
import pandas as pd
from time import sleep
import warnings 



#%%

FIRST_PAGE = 0
i = FIRST_PAGE
all_listings = pd.DataFrame([])

cookies = {
    '_ga': 'GA1.2.1278248909.1659285193',
    # non-necessary cookies
    # 'webapp_token': '%22XxqIK06Y9vCRR8X1hW67BstH4AnxbYHCYOT-OxHGn2IOSNlGpoBVdBEK2QvgIa15GhF7-mJCh1jPaajA-4LNyvZtDeI6Gm1o44uZ3zFddU6q3uw-BnSeubhozpF73Lpq1233PquYQEZT2uofoylOlmVChki0kQlQZIkI6nuBuegH%22',
    # 'user_phone': '555011215',
    # 'user_about': '%22%22',
    # 'user_id': '2678888',
    # 'user_img': '%22%22',
    # 'user_iam_verified': '%22%22',
    # 'user_rega_approved': '%22%22',
    # 'user_listings': '%22%22',
    # 'user_type': 'null',
    # 'user_name': '%22%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%85%D9%86%D8%B5%D9%88%D8%B1%22',
    # 'user_email': '%22mms.alsalamah@gmail.com%22',
    # 'user_chosen_user_type': '%22seeker%22',
    # 'user_favs': 'undefined',
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
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_ga=GA1.2.1278248909.1659285193; webapp_token=%22XxqIK06Y9vCRR8X1hW67BstH4AnxbYHCYOT-OxHGn2IOSNlGpoBVdBEK2QvgIa15GhF7-mJCh1jPaajA-4LNyvZtDeI6Gm1o44uZ3zFddU6q3uw-BnSeubhozpF73Lpq1233PquYQEZT2uofoylOlmVChki0kQlQZIkI6nuBuegH%22; user_phone=555011215; user_about=%22%22; user_id=2678888; user_img=%22%22; user_iam_verified=%22%22; user_rega_approved=%22%22; user_listings=%22%22; user_type=null; user_name=%22%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%85%D9%86%D8%B5%D9%88%D8%B1%22; user_email=%22mms.alsalamah@gmail.com%22; user_chosen_user_type=%22seeker%22; user_favs=undefined; _gid=GA1.2.1862803336.1660289756; _gac_UA-52229618-6=1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE; AWSALBTG=foXxUgV+1XpnEh3LXPIBZKVqV79Hq8jAoJivEyXBOOSvjJ7MK+zmtK1lQIJytYj1EKSPIJ929+d3tGcGdWuNJOrER8dKWLVkMmK3v5O676cCWsNfG6cFysFFlcir8pWC8xVAEwGkMftQeGMusLU/Iquea5yHLazpr/MKeTd7HPUadu7xDNg=; AWSALBTGCORS=foXxUgV+1XpnEh3LXPIBZKVqV79Hq8jAoJivEyXBOOSvjJ7MK+zmtK1lQIJytYj1EKSPIJ929+d3tGcGdWuNJOrER8dKWLVkMmK3v5O676cCWsNfG6cFysFFlcir8pWC8xVAEwGkMftQeGMusLU/Iquea5yHLazpr/MKeTd7HPUadu7xDNg=',
    'dpr': '0.666667',
    'origin': 'https://sa.aqar.fm',
    'referer': 'https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/4',
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

        
        # a webpage containing 20 apartment listings and other elements
        response_json = response.json()
        # getting relevant information
        listings_list = response_json.get('data').get('Web').get('find').get('listings')

        listings_list = pd.DataFrame(listings_list)
        # appending listings from different pages to one dataframe
        if i != 0:
            if list(all_listings.iloc[0])[1] ==list(listings_list.iloc[0])[1]:
                mesege = i 
                break
                    
        all_listings = all_listings.append(listings_list, ignore_index=True)
        sleep(1)
        i+=20
    except:
        break
    
    
    
#%%
print(f"i at the end of looping is equal to: {i}")
print(all_listings.head())

all_listings.to_csv("apartment_sale_data.csv", index=False)

#%%
# web scrape apartments for sale from east Riyadh
FIRST_PAGE = 0
i = FIRST_PAGE
all_listings_east = pd.DataFrame([])


cookies = {
    '_ga': 'GA1.2.1278248909.1659285193',
    # 'webapp_token': '%22XxqIK06Y9vCRR8X1hW67BstH4AnxbYHCYOT-OxHGn2IOSNlGpoBVdBEK2QvgIa15GhF7-mJCh1jPaajA-4LNyvZtDeI6Gm1o44uZ3zFddU6q3uw-BnSeubhozpF73Lpq1233PquYQEZT2uofoylOlmVChki0kQlQZIkI6nuBuegH%22',
    # 'user_phone': '555011215',
    # 'user_about': '%22%22',
    # 'user_id': '2678888',
    # 'user_img': '%22%22',
    # 'user_iam_verified': '%22%22',
    # 'user_rega_approved': '%22%22',
    # 'user_listings': '%22%22',
    # 'user_type': 'null',
    # 'user_name': '%22%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%85%D9%86%D8%B5%D9%88%D8%B1%22',
    # 'user_email': '%22mms.alsalamah@gmail.com%22',
    # 'user_chosen_user_type': '%22seeker%22',
    # 'user_favs': 'undefined',
    '_gid': 'GA1.2.1862803336.1660289756',
    '_gac_UA-52229618-6': '1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE',
    'AWSALBTG': 'ia+T2K6v1HRDnzAqNOXT9dOugEqqyIRDxiMbKPN0kt6Avnttc5b8VYLcvZeW8HCt1a8PWTfsUuvu192xqNYJvc/jU7nMBt+F3pLt3aqZt2Ldi7NZIRHpKMwswKrYh7Jd2AJ3rHTImmb6XWQqcDrIe/V/HhclBeLiUmCVN8Fiul1rRg5Wgzs=',
    'AWSALBTGCORS': 'ia+T2K6v1HRDnzAqNOXT9dOugEqqyIRDxiMbKPN0kt6Avnttc5b8VYLcvZeW8HCt1a8PWTfsUuvu192xqNYJvc/jU7nMBt+F3pLt3aqZt2Ldi7NZIRHpKMwswKrYh7Jd2AJ3rHTImmb6XWQqcDrIe/V/HhclBeLiUmCVN8Fiul1rRg5Wgzs=',
}

headers = {
    'authority': 'sa.aqar.fm',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hmn;q=0.8,ar;q=0.7,nl;q=0.6',
    'app-version': '0.16.18',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_ga=GA1.2.1278248909.1659285193; webapp_token=%22XxqIK06Y9vCRR8X1hW67BstH4AnxbYHCYOT-OxHGn2IOSNlGpoBVdBEK2QvgIa15GhF7-mJCh1jPaajA-4LNyvZtDeI6Gm1o44uZ3zFddU6q3uw-BnSeubhozpF73Lpq1233PquYQEZT2uofoylOlmVChki0kQlQZIkI6nuBuegH%22; user_phone=555011215; user_about=%22%22; user_id=2678888; user_img=%22%22; user_iam_verified=%22%22; user_rega_approved=%22%22; user_listings=%22%22; user_type=null; user_name=%22%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%85%D9%86%D8%B5%D9%88%D8%B1%22; user_email=%22mms.alsalamah@gmail.com%22; user_chosen_user_type=%22seeker%22; user_favs=undefined; _gid=GA1.2.1862803336.1660289756; _gac_UA-52229618-6=1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE; AWSALBTG=ia+T2K6v1HRDnzAqNOXT9dOugEqqyIRDxiMbKPN0kt6Avnttc5b8VYLcvZeW8HCt1a8PWTfsUuvu192xqNYJvc/jU7nMBt+F3pLt3aqZt2Ldi7NZIRHpKMwswKrYh7Jd2AJ3rHTImmb6XWQqcDrIe/V/HhclBeLiUmCVN8Fiul1rRg5Wgzs=; AWSALBTGCORS=ia+T2K6v1HRDnzAqNOXT9dOugEqqyIRDxiMbKPN0kt6Avnttc5b8VYLcvZeW8HCt1a8PWTfsUuvu192xqNYJvc/jU7nMBt+F3pLt3aqZt2Ldi7NZIRHpKMwswKrYh7Jd2AJ3rHTImmb6XWQqcDrIe/V/HhclBeLiUmCVN8Fiul1rRg5Wgzs=',
    'dpr': '1.33333',
    'origin': 'https://sa.aqar.fm',
    'referer': 'https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%B4%D8%B1%D9%82-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/3',
    'req-app': 'web',
    'req-device-token': '33e28a14-0941-41b1-b2a1-68e1304e76d8',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'viewport-width': '1050',
}


while True:
    try:
        json_data = {
        'operationName': 'findListings',
        'variables': {
            'size': 20,
            'from': i,
            'sort': {
                'create_time': 'desc',
                'has_img': 'desc',
            },
            'where': {
                'category': {
                    'eq': 6,
                },
                'city_id': {
                    'eq': 21,
                },
                'direction_id': {
                    'eq': 3,
                },
            },
        },
            'query': 'query findListings($size: Int, $from: Int, $sort: SortInput, $where: WhereInput, $polygon: [LocationInput!]) {\n  Web {\n    find(size: $size, from: $from, sort: $sort, where: $where, polygon: $polygon) {\n      ...WebResults\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WebResults on WebResults {\n  listings {\n    user_id\n    id\n    uri\n    title\n    price\n    content\n    imgs\n    refresh\n    category\n    beds\n    livings\n    wc\n    area\n    type\n    street_width\n    age\n    last_update\n    street_direction\n    ketchen\n    ac\n    furnished\n    location {\n      lat\n      lng\n      __typename\n    }\n    path\n    user {\n      review\n      img\n      name\n      phone\n      iam_verified\n      rega_id\n      __typename\n    }\n    native {\n      logo\n      title\n      image\n      description\n      external_url\n      __typename\n    }\n    rent_period\n    city\n    district\n    width\n    length\n    advertiser_type\n    create_time\n    __typename\n  }\n  total\n  __typename\n}\n',
        }

        response = requests.post('https://sa.aqar.fm/graphql', cookies=cookies, headers=headers, json=json_data)
        # a webpage containing 5 special listings and other elements
        
        response_json = response.json()
        # 
        listings_list = response_json.get('data').get('Web').get('find').get('listings')

        listings_list = pd.DataFrame(listings_list)
        if i != 0:
            if list(all_listings_east.iloc[0])[1] ==list(listings_list.iloc[0])[1]:
                mesege = i 
                break
                    
        all_listings_east = all_listings_east.append(listings_list, ignore_index=True)
        sleep(0.5)
        i+=20
    except:
        break
    
    
#%%
#%%
# web scrape apartments for sale from west Riyadh
FIRST_PAGE = 0
i = FIRST_PAGE
all_listings_west = pd.DataFrame([])



cookies = {
    '_ga': 'GA1.2.1278248909.1659285193',
    'webapp_token': '%22XxqIK06Y9vCRR8X1hW67BstH4AnxbYHCYOT-OxHGn2IOSNlGpoBVdBEK2QvgIa15GhF7-mJCh1jPaajA-4LNyvZtDeI6Gm1o44uZ3zFddU6q3uw-BnSeubhozpF73Lpq1233PquYQEZT2uofoylOlmVChki0kQlQZIkI6nuBuegH%22',
    'user_phone': '555011215',
    'user_about': '%22%22',
    'user_id': '2678888',
    'user_img': '%22%22',
    'user_iam_verified': '%22%22',
    'user_rega_approved': '%22%22',
    'user_listings': '%22%22',
    'user_type': 'null',
    'user_name': '%22%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%85%D9%86%D8%B5%D9%88%D8%B1%22',
    'user_email': '%22mms.alsalamah@gmail.com%22',
    'user_chosen_user_type': '%22seeker%22',
    'user_favs': 'undefined',
    '_gid': 'GA1.2.1862803336.1660289756',
    '_gac_UA-52229618-6': '1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE',
    'AWSALBTG': 'S/14jbqMXoofpt00JnL+NnocCLAVDd6HnZJ+5mGC/Univr2NS6RmZyl4ndH2dYrzzMcT68YGbwEKuFl4hT0ZoKfJCAyJjK9qU7MPiLc6DxuYlp1o9oRKB3ZYsTLhNDwD2xQsxSNWzcRh5lI6M4ToR5Rblu0C9wOs8tQTdxo2RqjHPdp843I=',
    'AWSALBTGCORS': 'S/14jbqMXoofpt00JnL+NnocCLAVDd6HnZJ+5mGC/Univr2NS6RmZyl4ndH2dYrzzMcT68YGbwEKuFl4hT0ZoKfJCAyJjK9qU7MPiLc6DxuYlp1o9oRKB3ZYsTLhNDwD2xQsxSNWzcRh5lI6M4ToR5Rblu0C9wOs8tQTdxo2RqjHPdp843I=',
    '_gat': '1',
}

headers = {
    'authority': 'sa.aqar.fm',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hmn;q=0.8,ar;q=0.7,nl;q=0.6',
    'app-version': '0.16.18',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_ga=GA1.2.1278248909.1659285193; webapp_token=%22XxqIK06Y9vCRR8X1hW67BstH4AnxbYHCYOT-OxHGn2IOSNlGpoBVdBEK2QvgIa15GhF7-mJCh1jPaajA-4LNyvZtDeI6Gm1o44uZ3zFddU6q3uw-BnSeubhozpF73Lpq1233PquYQEZT2uofoylOlmVChki0kQlQZIkI6nuBuegH%22; user_phone=555011215; user_about=%22%22; user_id=2678888; user_img=%22%22; user_iam_verified=%22%22; user_rega_approved=%22%22; user_listings=%22%22; user_type=null; user_name=%22%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%85%D9%86%D8%B5%D9%88%D8%B1%22; user_email=%22mms.alsalamah@gmail.com%22; user_chosen_user_type=%22seeker%22; user_favs=undefined; _gid=GA1.2.1862803336.1660289756; _gac_UA-52229618-6=1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE; AWSALBTG=S/14jbqMXoofpt00JnL+NnocCLAVDd6HnZJ+5mGC/Univr2NS6RmZyl4ndH2dYrzzMcT68YGbwEKuFl4hT0ZoKfJCAyJjK9qU7MPiLc6DxuYlp1o9oRKB3ZYsTLhNDwD2xQsxSNWzcRh5lI6M4ToR5Rblu0C9wOs8tQTdxo2RqjHPdp843I=; AWSALBTGCORS=S/14jbqMXoofpt00JnL+NnocCLAVDd6HnZJ+5mGC/Univr2NS6RmZyl4ndH2dYrzzMcT68YGbwEKuFl4hT0ZoKfJCAyJjK9qU7MPiLc6DxuYlp1o9oRKB3ZYsTLhNDwD2xQsxSNWzcRh5lI6M4ToR5Rblu0C9wOs8tQTdxo2RqjHPdp843I=; _gat=1',
    'dpr': '1.33333',
    'origin': 'https://sa.aqar.fm',
    'referer': 'https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%BA%D8%B1%D8%A8-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/4',
    'req-app': 'web',
    'req-device-token': '33e28a14-0941-41b1-b2a1-68e1304e76d8',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'viewport-width': '1050',
}



while True:
    try:
        json_data = {
            'operationName': 'findListings',
            'variables': {
                'size': 20,
                'from': i,
                'sort': {
                    'create_time': 'desc',
                    'has_img': 'desc',
                },
                'where': {
                    'category': {
                        'eq': 6,
                    },
                    'city_id': {
                        'eq': 21,
                    },
                    'direction_id': {
                        'eq': 6,
                    },
                },
            },
            'query': 'query findListings($size: Int, $from: Int, $sort: SortInput, $where: WhereInput, $polygon: [LocationInput!]) {\n  Web {\n    find(size: $size, from: $from, sort: $sort, where: $where, polygon: $polygon) {\n      ...WebResults\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WebResults on WebResults {\n  listings {\n    user_id\n    id\n    uri\n    title\n    price\n    content\n    imgs\n    refresh\n    category\n    beds\n    livings\n    wc\n    area\n    type\n    street_width\n    age\n    last_update\n    street_direction\n    ketchen\n    ac\n    furnished\n    location {\n      lat\n      lng\n      __typename\n    }\n    path\n    user {\n      review\n      img\n      name\n      phone\n      iam_verified\n      rega_id\n      __typename\n    }\n    native {\n      logo\n      title\n      image\n      description\n      external_url\n      __typename\n    }\n    rent_period\n    city\n    district\n    width\n    length\n    advertiser_type\n    create_time\n    __typename\n  }\n  total\n  __typename\n}\n',
        }


        response = requests.post('https://sa.aqar.fm/graphql', cookies=cookies, headers=headers, json=json_data)
        # a webpage containing 5 special listings and other elements
        
        response_json = response.json()
        # 
        listings_list = response_json.get('data').get('Web').get('find').get('listings')

        listings_list = pd.DataFrame(listings_list)
        if i != 0:
            if list(all_listings_west.iloc[0])[1] ==list(listings_list.iloc[0])[1]:
                mesege = i 
                break
                    
        all_listings_west = all_listings_west.append(listings_list, ignore_index=True)
        sleep(0.5)
        i+=20
    except:
        break
    

#%%
# web scrape apartments for sale from south Riyadh
FIRST_PAGE = 0
i = FIRST_PAGE
all_listings_south = pd.DataFrame([])


cookies = {
    '_ga': 'GA1.2.1278248909.1659285193',
    '_gid': 'GA1.2.1862803336.1660289756',
    '_gac_UA-52229618-6': '1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE',
    '_gat': '1',
    'AWSALBTG': 'YKGzHhGDjN/uo8GvjfJhScsisxqqxDPMIZo/6L+jEiJBriaSBlUMnDwlg+et5O2sPiXcOHdH9gTq6jE3k+CHZ4arwPg4645uCJ3skPc4x+yil+wmsJeB6FZ7b2DIrOjwa8+E4KAmDJ7hfDyRk7fG+f8M9amzXTD3BX/RwxpcftYuPMwxouo=',
    'AWSALBTGCORS': 'YKGzHhGDjN/uo8GvjfJhScsisxqqxDPMIZo/6L+jEiJBriaSBlUMnDwlg+et5O2sPiXcOHdH9gTq6jE3k+CHZ4arwPg4645uCJ3skPc4x+yil+wmsJeB6FZ7b2DIrOjwa8+E4KAmDJ7hfDyRk7fG+f8M9amzXTD3BX/RwxpcftYuPMwxouo=',
}

headers = {
    'authority': 'sa.aqar.fm',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hmn;q=0.8,ar;q=0.7,nl;q=0.6',
    'app-version': '0.16.18',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_ga=GA1.2.1278248909.1659285193; webapp_token=%22XxqIK06Y9vCRR8X1hW67BstH4AnxbYHCYOT-OxHGn2IOSNlGpoBVdBEK2QvgIa15GhF7-mJCh1jPaajA-4LNyvZtDeI6Gm1o44uZ3zFddU6q3uw-BnSeubhozpF73Lpq1233PquYQEZT2uofoylOlmVChki0kQlQZIkI6nuBuegH%22; user_phone=555011215; user_about=%22%22; user_id=2678888; user_img=%22%22; user_iam_verified=%22%22; user_rega_approved=%22%22; user_listings=%22%22; user_type=null; user_name=%22%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%85%D9%86%D8%B5%D9%88%D8%B1%22; user_email=%22mms.alsalamah@gmail.com%22; user_chosen_user_type=%22seeker%22; user_favs=undefined; _gid=GA1.2.1862803336.1660289756; _gac_UA-52229618-6=1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE; _gat=1; AWSALBTG=YKGzHhGDjN/uo8GvjfJhScsisxqqxDPMIZo/6L+jEiJBriaSBlUMnDwlg+et5O2sPiXcOHdH9gTq6jE3k+CHZ4arwPg4645uCJ3skPc4x+yil+wmsJeB6FZ7b2DIrOjwa8+E4KAmDJ7hfDyRk7fG+f8M9amzXTD3BX/RwxpcftYuPMwxouo=; AWSALBTGCORS=YKGzHhGDjN/uo8GvjfJhScsisxqqxDPMIZo/6L+jEiJBriaSBlUMnDwlg+et5O2sPiXcOHdH9gTq6jE3k+CHZ4arwPg4645uCJ3skPc4x+yil+wmsJeB6FZ7b2DIrOjwa8+E4KAmDJ7hfDyRk7fG+f8M9amzXTD3BX/RwxpcftYuPMwxouo=',
    'dpr': '1.33333',
    'origin': 'https://sa.aqar.fm',
    'referer': 'https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%AC%D9%86%D9%88%D8%A8-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/3',
    'req-app': 'web',
    'req-device-token': '33e28a14-0941-41b1-b2a1-68e1304e76d8',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'viewport-width': '1050',
}


while True:
    try:
        json_data = {
            'operationName': 'findListings',
            'variables': {
                'size': 20,
                'from': i,
                'sort': {
                    'create_time': 'desc',
                    'has_img': 'desc',
                },
                'where': {
                    'category': {
                        'eq': 6,
                    },
                    'city_id': {
                        'eq': 21,
                    },
                    'direction_id': {
                        'eq': 1,
                    },
                },
            },
            'query': 'query findListings($size: Int, $from: Int, $sort: SortInput, $where: WhereInput, $polygon: [LocationInput!]) {\n  Web {\n    find(size: $size, from: $from, sort: $sort, where: $where, polygon: $polygon) {\n      ...WebResults\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WebResults on WebResults {\n  listings {\n    user_id\n    id\n    uri\n    title\n    price\n    content\n    imgs\n    refresh\n    category\n    beds\n    livings\n    wc\n    area\n    type\n    street_width\n    age\n    last_update\n    street_direction\n    ketchen\n    ac\n    furnished\n    location {\n      lat\n      lng\n      __typename\n    }\n    path\n    user {\n      review\n      img\n      name\n      phone\n      iam_verified\n      rega_id\n      __typename\n    }\n    native {\n      logo\n      title\n      image\n      description\n      external_url\n      __typename\n    }\n    rent_period\n    city\n    district\n    width\n    length\n    advertiser_type\n    create_time\n    __typename\n  }\n  total\n  __typename\n}\n',
        }

        response = requests.post('https://sa.aqar.fm/graphql', cookies=cookies, headers=headers, json=json_data)
        # a webpage containing 5 special listings and other elements
        
        response_json = response.json()
        # 
        listings_list = response_json.get('data').get('Web').get('find').get('listings')

        listings_list = pd.DataFrame(listings_list)
        if i != 0:
            if list(all_listings_south.iloc[0])[1] ==list(listings_list.iloc[0])[1]:
                mesege = i 
                break
                    
        all_listings_south = all_listings_south.append(listings_list, ignore_index=True)
        sleep(0.5)
        i+=20
    except:
        break

#%%
# web scrape apartments for sale from north Riyadh
FIRST_PAGE = 0
i = FIRST_PAGE
all_listings_north = pd.DataFrame([])

cookies = {
    '_ga': 'GA1.2.1278248909.1659285193',
    '_gid': 'GA1.2.1862803336.1660289756',
    '_gac_UA-52229618-6': '1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE',
    '_gat': '1',
    'AWSALBTG': '/g7fqZRvzQlkVB2xLwbpJqSGD9/rPItk91qhsn8CWn+rC8K3fo9PZIL8lrN03fUGQqF6w5HAZphfY14eKwmCVmOo0CYe2hf1W2I5wGVqzeAIP9+y2XftjbJriPHfuAUiyS7oTux7kOiVi7pTRZDEXxcKpI1HRxKnvEivA3VzGm6NqKb4IDI=',
    'AWSALBTGCORS': '/g7fqZRvzQlkVB2xLwbpJqSGD9/rPItk91qhsn8CWn+rC8K3fo9PZIL8lrN03fUGQqF6w5HAZphfY14eKwmCVmOo0CYe2hf1W2I5wGVqzeAIP9+y2XftjbJriPHfuAUiyS7oTux7kOiVi7pTRZDEXxcKpI1HRxKnvEivA3VzGm6NqKb4IDI=',
}

headers = {
    'authority': 'sa.aqar.fm',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hmn;q=0.8,ar;q=0.7,nl;q=0.6',
    'app-version': '0.16.18',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_ga=GA1.2.1278248909.1659285193; webapp_token=%22XxqIK06Y9vCRR8X1hW67BstH4AnxbYHCYOT-OxHGn2IOSNlGpoBVdBEK2QvgIa15GhF7-mJCh1jPaajA-4LNyvZtDeI6Gm1o44uZ3zFddU6q3uw-BnSeubhozpF73Lpq1233PquYQEZT2uofoylOlmVChki0kQlQZIkI6nuBuegH%22; user_phone=555011215; user_about=%22%22; user_id=2678888; user_img=%22%22; user_iam_verified=%22%22; user_rega_approved=%22%22; user_listings=%22%22; user_type=null; user_name=%22%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%85%D9%86%D8%B5%D9%88%D8%B1%22; user_email=%22mms.alsalamah@gmail.com%22; user_chosen_user_type=%22seeker%22; user_favs=undefined; _gid=GA1.2.1862803336.1660289756; _gac_UA-52229618-6=1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE; _gat=1; AWSALBTG=/g7fqZRvzQlkVB2xLwbpJqSGD9/rPItk91qhsn8CWn+rC8K3fo9PZIL8lrN03fUGQqF6w5HAZphfY14eKwmCVmOo0CYe2hf1W2I5wGVqzeAIP9+y2XftjbJriPHfuAUiyS7oTux7kOiVi7pTRZDEXxcKpI1HRxKnvEivA3VzGm6NqKb4IDI=; AWSALBTGCORS=/g7fqZRvzQlkVB2xLwbpJqSGD9/rPItk91qhsn8CWn+rC8K3fo9PZIL8lrN03fUGQqF6w5HAZphfY14eKwmCVmOo0CYe2hf1W2I5wGVqzeAIP9+y2XftjbJriPHfuAUiyS7oTux7kOiVi7pTRZDEXxcKpI1HRxKnvEivA3VzGm6NqKb4IDI=',
    'dpr': '1.33333',
    'origin': 'https://sa.aqar.fm',
    'referer': 'https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D8%B4%D9%85%D8%A7%D9%84-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/3',
    'req-app': 'web',
    'req-device-token': '33e28a14-0941-41b1-b2a1-68e1304e76d8',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'viewport-width': '1050',
}

while True:
    try:
        json_data = {
            'operationName': 'findListings',
            'variables': {
                'size': 20,
                'from': i,
                'sort': {
                    'create_time': 'desc',
                    'has_img': 'desc',
                },
                'where': {
                    'category': {
                        'eq': 6,
                    },
                    'city_id': {
                        'eq': 21,
                    },
                    'direction_id': {
                        'eq': 4,
                    },
                },
            },
            'query': 'query findListings($size: Int, $from: Int, $sort: SortInput, $where: WhereInput, $polygon: [LocationInput!]) {\n  Web {\n    find(size: $size, from: $from, sort: $sort, where: $where, polygon: $polygon) {\n      ...WebResults\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WebResults on WebResults {\n  listings {\n    user_id\n    id\n    uri\n    title\n    price\n    content\n    imgs\n    refresh\n    category\n    beds\n    livings\n    wc\n    area\n    type\n    street_width\n    age\n    last_update\n    street_direction\n    ketchen\n    ac\n    furnished\n    location {\n      lat\n      lng\n      __typename\n    }\n    path\n    user {\n      review\n      img\n      name\n      phone\n      iam_verified\n      rega_id\n      __typename\n    }\n    native {\n      logo\n      title\n      image\n      description\n      external_url\n      __typename\n    }\n    rent_period\n    city\n    district\n    width\n    length\n    advertiser_type\n    create_time\n    __typename\n  }\n  total\n  __typename\n}\n',
        }

        response = requests.post('https://sa.aqar.fm/graphql', cookies=cookies, headers=headers, json=json_data)
        # a webpage containing 5 special listings and other elements
        
        response_json = response.json()
        # 
        listings_list = response_json.get('data').get('Web').get('find').get('listings')

        listings_list = pd.DataFrame(listings_list)
        if i != 0:
            if list(all_listings_north.iloc[0])[1] ==list(listings_list.iloc[0])[1]:
                mesege = i 
                break
                    
        all_listings_north = all_listings_north.append(listings_list, ignore_index=True)
        sleep(0.5)
        i+=20
    except:
        break

#%%
# web scrape apartments for sale from middle of Riyadh
FIRST_PAGE = 0
i = FIRST_PAGE
all_listings_middle = pd.DataFrame([])


cookies = {
    '_ga': 'GA1.2.1278248909.1659285193',
    'webapp_token': '%22XxqIK06Y9vCRR8X1hW67BstH4AnxbYHCYOT-OxHGn2IOSNlGpoBVdBEK2QvgIa15GhF7-mJCh1jPaajA-4LNyvZtDeI6Gm1o44uZ3zFddU6q3uw-BnSeubhozpF73Lpq1233PquYQEZT2uofoylOlmVChki0kQlQZIkI6nuBuegH%22',
    'user_phone': '555011215',
    'user_about': '%22%22',
    'user_id': '2678888',
    'user_img': '%22%22',
    'user_iam_verified': '%22%22',
    'user_rega_approved': '%22%22',
    'user_listings': '%22%22',
    'user_type': 'null',
    'user_name': '%22%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%85%D9%86%D8%B5%D9%88%D8%B1%22',
    'user_email': '%22mms.alsalamah@gmail.com%22',
    'user_chosen_user_type': '%22seeker%22',
    'user_favs': 'undefined',
    '_gid': 'GA1.2.1862803336.1660289756',
    '_gac_UA-52229618-6': '1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE',
    '_gat': '1',
    'AWSALBTG': '3WL6VYN0QXnIRrFm3aFrhG2vvHO8ka437mgBuNviCM5vAoC+jlr4/3wJ1DE0evqWJxtSAL/aQZaM6iB1dIHXjHnzbYoF5TWUMgo22h9PEOK2iQGP4oU2FE+VP3muwPnRaxs96QWzicmcZudDYfpUnPTxngvJF2CXi85+Z4nqdZjJ31o7KFE=',
    'AWSALBTGCORS': '3WL6VYN0QXnIRrFm3aFrhG2vvHO8ka437mgBuNviCM5vAoC+jlr4/3wJ1DE0evqWJxtSAL/aQZaM6iB1dIHXjHnzbYoF5TWUMgo22h9PEOK2iQGP4oU2FE+VP3muwPnRaxs96QWzicmcZudDYfpUnPTxngvJF2CXi85+Z4nqdZjJ31o7KFE=',
}

headers = {
    'authority': 'sa.aqar.fm',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,hmn;q=0.8,ar;q=0.7,nl;q=0.6',
    'app-version': '0.16.18',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_ga=GA1.2.1278248909.1659285193; webapp_token=%22XxqIK06Y9vCRR8X1hW67BstH4AnxbYHCYOT-OxHGn2IOSNlGpoBVdBEK2QvgIa15GhF7-mJCh1jPaajA-4LNyvZtDeI6Gm1o44uZ3zFddU6q3uw-BnSeubhozpF73Lpq1233PquYQEZT2uofoylOlmVChki0kQlQZIkI6nuBuegH%22; user_phone=555011215; user_about=%22%22; user_id=2678888; user_img=%22%22; user_iam_verified=%22%22; user_rega_approved=%22%22; user_listings=%22%22; user_type=null; user_name=%22%D9%85%D8%AD%D9%85%D8%AF%20%D8%A7%D9%84%D9%85%D9%86%D8%B5%D9%88%D8%B1%22; user_email=%22mms.alsalamah@gmail.com%22; user_chosen_user_type=%22seeker%22; user_favs=undefined; _gid=GA1.2.1862803336.1660289756; _gac_UA-52229618-6=1.1660301559.CjwKCAjw9NeXBhAMEiwAbaY4lj1eKkVdYvl2n7n-CsxVyhOK4UV5OkiNQY1L-CmZ2ROHmtbk-eKAhhoCpAwQAvD_BwE; _gat=1; AWSALBTG=3WL6VYN0QXnIRrFm3aFrhG2vvHO8ka437mgBuNviCM5vAoC+jlr4/3wJ1DE0evqWJxtSAL/aQZaM6iB1dIHXjHnzbYoF5TWUMgo22h9PEOK2iQGP4oU2FE+VP3muwPnRaxs96QWzicmcZudDYfpUnPTxngvJF2CXi85+Z4nqdZjJ31o7KFE=; AWSALBTGCORS=3WL6VYN0QXnIRrFm3aFrhG2vvHO8ka437mgBuNviCM5vAoC+jlr4/3wJ1DE0evqWJxtSAL/aQZaM6iB1dIHXjHnzbYoF5TWUMgo22h9PEOK2iQGP4oU2FE+VP3muwPnRaxs96QWzicmcZudDYfpUnPTxngvJF2CXi85+Z4nqdZjJ31o7KFE=',
    'dpr': '1.33333',
    'origin': 'https://sa.aqar.fm',
    'referer': 'https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A8%D9%8A%D8%B9/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/%D9%88%D8%B3%D8%B7-%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/2',
    'req-app': 'web',
    'req-device-token': '33e28a14-0941-41b1-b2a1-68e1304e76d8',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'viewport-width': '1050',
}


while True:
    try:
        json_data = {
            'operationName': 'findListings',
            'variables': {
                'size': 20,
                'from': i,
                'sort': {
                    'create_time': 'desc',
                    'has_img': 'desc',
                },
                'where': {
                    'category': {
                        'eq': 6,
                    },
                    'city_id': {
                        'eq': 21,
                    },
                    'direction_id': {
                        'eq': 7,
                    },
                },
            },
            'query': 'query findListings($size: Int, $from: Int, $sort: SortInput, $where: WhereInput, $polygon: [LocationInput!]) {\n  Web {\n    find(size: $size, from: $from, sort: $sort, where: $where, polygon: $polygon) {\n      ...WebResults\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WebResults on WebResults {\n  listings {\n    user_id\n    id\n    uri\n    title\n    price\n    content\n    imgs\n    refresh\n    category\n    beds\n    livings\n    wc\n    area\n    type\n    street_width\n    age\n    last_update\n    street_direction\n    ketchen\n    ac\n    furnished\n    location {\n      lat\n      lng\n      __typename\n    }\n    path\n    user {\n      review\n      img\n      name\n      phone\n      iam_verified\n      rega_id\n      __typename\n    }\n    native {\n      logo\n      title\n      image\n      description\n      external_url\n      __typename\n    }\n    rent_period\n    city\n    district\n    width\n    length\n    advertiser_type\n    create_time\n    __typename\n  }\n  total\n  __typename\n}\n',
        }

        response = requests.post('https://sa.aqar.fm/graphql', cookies=cookies, headers=headers, json=json_data)
        # a webpage containing 5 special listings and other elements
        
        response_json = response.json()
        # 
        listings_list = response_json.get('data').get('Web').get('find').get('listings')

        listings_list = pd.DataFrame(listings_list)
        if i != 0:
            if list(all_listings_middle.iloc[0])[1] ==list(listings_list.iloc[0])[1]:
                mesege = i 
                break
                    
        all_listings_middle = all_listings_middle.append(listings_list, ignore_index=True)
        sleep(0.5)
        i+=20
    except:
        break
    
    
# %%
all_listings_middle.to_csv("apartments_sale_middle_riyadh.csv")
all_listings_north.to_csv("apartments_sale_north_riyadh.csv")
all_listings_south.to_csv("apartments_sale_south_riyadh.csv")
all_listings_east.to_csv("apartments_sale_east_riyadh.csv")
all_listings_west.to_csv("apartments_sale_west_riyadh.csv")







# %%
