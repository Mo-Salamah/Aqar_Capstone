# Data Dictionary

Attribute| Description
-----|------|
neighborhood| the name of the neighborhood
neighborhood_location| north-east, north-west, etc.
contract_length| anually, monthly, weekly, daily
price| price to sign a contract of the specified length
family| managment rents to families only [1, 0]
room| number of bedrooms 
living_room| number of livingrooms
bathroom| number of bathrooms
floor| where the apartment is located
property_age| in years
kitchen| the apartment contains a kitchen [1, 0]
elevator| the building contains an elevator [1, 0]
ac| the apartment includes preinstalled air conditioning [1, 0]
dimensions_length| in meters
dimensions_width| in meters
ad_number| on Aqar
post_date| year-month-day
latest_update| {"few days ago", "a week ago", etc.}
views| on Aqar 
location| (longitude, latitude)
advertiser_name| provided by the advertiser
advertiser_verified| [1, 0]
advertiser_rating| [0, 10]
number_ratings| number of ratings given to the advertiser



Attribute| Description
-----|------|
user_id| id of the user who created the past
id| post id
uri| url of the post
title| of the post
price| in Riyals
content| the text description of the property
imgs| list of urls where the images are saved
beds| number of bedrooms
livings| number of living rooms
wc| number of bathrooms
area| in m^2
street_width| in m
age| of property in years
last_update| date of latest refresh to the post
street_direction|
ketchen| {0, 1}
ac| {0, 1}
furnished| {0, 1}
latitude| latitude coordinate of the property
longitude| longitude coordinate of the property 
path| duplicate (with some differences)
user| ******change to multiple attributes***
district| where the property is located
width| of property, in meteres
length| of property, in meters
advertiser_type| {'exclusive_marketer', 'normal_marketer', 'owner', 'agent'}
create_time| date of post creation



new attributes:

street| use path to search for the word "شارع" and copy everything up until a /
