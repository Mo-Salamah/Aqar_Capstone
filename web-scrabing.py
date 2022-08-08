#%%
from bs4 import BeautifulSoup 
import requests
import numpy as np
import pandas as pd


#%%
AVAILABLE_PAGES = 345
soup = []
html = []
for i in range(1, AVAILABLE_PAGES):
    html_text = requests.get(f'https://sa.aqar.fm/%D8%B4%D9%82%D9%82-%D9%84%D9%84%D8%A5%D9%8A%D8%AC%D8%A7%D8%B1/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6/{i}?rent_type=3').text
    html.append(html_text)
    # soup.append(BeautifulSoup(html_text, 'lxml'))


# web_pages = soup.copy()
#%%

html_copy = html.copy()

for i, html_string in enumerate(html):
    with open(f"aqar_ads_pages/ad_page_{i}.html", "w") as file:
        file.write(html_string)

#%%
while !len(web_pages) == 0:
    page = web_pages.pop(index=0)
    ads = page.find_all('div', class_="listing_LinkedListingCard__5SRvZ")
    for ad in ads:
        url = "https://sa.aqar.fm" + ad['href']
        html_text = requests.get(url).text
        ad_soup = BeautifulSoup(html_text, 'lxml')
        
        title = get_title(ad_soup)
        #images = # ask Lujain how to do it. The problem is that the html tag classes 
        # change depending on how many images there are 
        # tag enclosing all images: "Gallery-module_imagesWrapper__weNHz"
        
        neighborhood, neighborhood_location = get_neighborhod_and_location(ad_soup)
        price = get_price(ad_soup)
        family = 
        room = 
        living_room = 
        bathroom = 
        floor = 
        property_age = 
        kitchen = 
        elevator = 
        ac = 
        dimensions = 
        ad_number = 
        post_date = 
        latest_update =
        views = 
        location = 
        advertiser_name = 
        advertiser_verified =
        advertiser_rating =
        number_ratings = 
        






# %%

def get_title(soup):
    temp = soup.find('div', id='__next')
    temp = temp.find('div', class_='layouts_layoutWrapper__eSdLv')
    temp = temp.find('div', class_='listingScreen_listingScreen__TWzQJ')
    title = temp.find('div', class_='listingScreen_header__QY76T').text
    return title


def get_neighborhod_and_location(soup):
    
    temp = soup.find('div', id='__next')
    temp = temp.find('div', class_="layouts_layoutWrapper__eSdLv")
    temp = temp.find('div', class_="listings_container__lmOqZ")
    temp = temp.find('div', class_="listings_breadcrumbContainer__AxNZj") # OR class_="listings_breadcrumbContainer__AxNZj listings_hidden__pyiaB"
    if temp == None:
        temp = temp.find('div', class_="listings_breadcrumbContainer__AxNZj listings_hidden__pyiaB")

    if temp == None:
        return None

    temp = temp.find('nav', class_="breadcrumb-module_breadcrumb__ovTaG breadcrumb-module_rtl__B7ER5")
    temp = temp.find('ol', class_="breadcrumb-module_list__BmcYf")
    temp_list = temp.find_all('li', class_="breadcrumb-module_item__ZLYPz")
    if len(temp_list) == 0: 
        return None

    if len(temp_list) == 1:
        print("something went wrong")

    return temp_list.pop().text, temp_list.pop().text


def get_price(soup):
    temp = soup.find('div', id='__next')
    temp = temp.find('div', class_='layouts_layoutWrapper__eSdLv')
    temp = temp.find('div', class_='listingScreen_listingScreen__TWzQJ')
    temp = temp.find('div', class_='listingScreen_container__iD5EV')
    temp = temp.find('div', class_='listingScreen_detailsSection__TjbgF')
    price = temp.find('div', class_='listingScreen_price__Z5pxE').text.split()[0]
    price = price.replace(',', '')
    price = int(price)
    
    return price








def main():
    

if __name__ == '__main__':
    main()



