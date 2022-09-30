This is my capstone project for Misk Data Science Intensive bootcamp. This project focuses on the real estate market in Riyadh. More specifically, the apartments for sale, which are posted on Aqar (Saudi Arabia's leading real estate market).  We aim to help home buyers make better purchases, which is achieved through providing two main deliverables. First, an analytical dashboard, which provides insight into the real estate market and how it's been developing. Second, a feature I call "Good Deal Indicator," which empowers the home buyer providing them an educated opinion on whether the asking price for an apartment is fair. All the user needs to do is provide the post ID of the apartment he or she is interested in (which is easily accessable on Aqar), and we will take care of web-scraping the website to find the relevent post, clean the data of the apartment, predict a fair asking price for the apartment, and finally, report whether the actual asking price constitutes a fair, good, or bad deal.

[:link: Click here to view a *very* breif exploratory data analysis](https://mo-salamah.github.io/Aqar_Capstone/)


# Data Dictionary


Attribute| Description
-----|------|
user_id| id of the user who created the listing
id| listing id
title| of the listing
price| in Riyals
content| the text description of the property
imgs| list of urls where the images are accessable
beds| number of bedrooms
livings| number of living rooms
wc| number of bathrooms
area| in m^2
street_width| in m
age| of property in years
last_update| date of latest refresh to the listing
street_direction|
kitchen| {0, 1}
ac| {0, 1}
furnished| {0, 1}
latitude| latitude coordinate of the property
longitude| longitude coordinate of the property 
path| duplicate (with some differences)
user| dictionary containing rating of user and verification status
district| where the property is located
width| of property, in meteres
length| of property, in meters
advertiser_type| {'exclusive_marketer', 'normal_marketer', 'owner', 'agent'}
create_time| date of post creation
time_on_market| in days
