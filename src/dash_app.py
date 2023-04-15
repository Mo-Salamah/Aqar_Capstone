#%%
from re import X
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from dash import Dash, dcc, html, Input, Output, State
from sklearn.model_selection import train_test_split
import pandas as pd
import json
import geopandas as gpd
import os
from good_deal_indicator_scraping import good_deal_indicator

# =================================================================

# load data 
os.chdir("/Users/mo/Desktop/DSI/Aqar_Capstone/src")
print(os.getcwd())
map_df = gpd.read_file("../data/riyadh.geojson")

with open(r"../data/riyadh_districts.json", 'r', encoding='utf8', errors='ignore') as file:
    neighborhood = json.load(file)


# getting arabic district names from neighborhood file
ar_name = []
en_name = []
for i in range(len(neighborhood)):
    ar_name.append(neighborhood[i]["name_ar"])
    en_name.append(neighborhood[i]["name_en"])

district_df = pd.DataFrame(ar_name, columns=['name_ar'])
district_df["name_en"] = en_name

map_df = map_df.merge(district_df, left_on=["name"], right_on=["name_en"])

apartments = pd.read_csv("../data/apartments_sale_riyadh_cleaned.csv")

# apartments = apartments[['price', 'beds', 'livings', 'wc', 'area', 
#                'street_width', 'age', 'ketchen', 'ac', 
#                'furnished', 'location', 'district', 'width',
#                'length', 'advertiser_type', 'longitude', 'latitude']]
city_side_mapper = {'north': 1, 'south': 2, 'east': 3, 'west':4, 'middle':5}
apartments['city_side'] = apartments['city_side'].apply(lambda side: city_side_mapper[side])

# apartments = apartments.groupby(['district'], as_index=False).mean()
# apartments["district"] = apartments["district"].apply(lambda x: x.strip())



# merged_df = map_df.merge(apartments, left_on=["name_ar"], right_on=["district"])

# geo_df = merged_df.set_index("district")


def get_geo_df(price_slider=None, age_slider=None, area_slider=None, beds_slider=None, livings_slider=None, bathrooms_slider=None, furnished_slider=None):

    # Test access to apartments df
    # load data 
    os.chdir("/Users/mo/Desktop/DSI/Aqar_Capstone/src")
    print(os.getcwd())
    map_df = gpd.read_file("../data/riyadh.geojson")

    with open(r"../data/riyadh_districts.json", 'r', encoding='utf8', errors='ignore') as file:
        neighborhood = json.load(file)


    # getting arabic district names from neighborhood file
    ar_name = []
    en_name = []
    for i in range(len(neighborhood)):
        ar_name.append(neighborhood[i]["name_ar"])
        en_name.append(neighborhood[i]["name_en"])

    district_df = pd.DataFrame(ar_name, columns=['name_ar'])
    district_df["name_en"] = en_name

    map_df = map_df.merge(district_df, left_on=["name"], right_on=["name_en"])

    apartments = pd.read_csv("../data/apartments_sale_riyadh_cleaned.csv")

    # apartments = apartments[['price', 'beds', 'livings', 'wc', 'area', 
    #                'street_width', 'age', 'ketchen', 'ac', 
    #                'furnished', 'location', 'district', 'width',
    #                'length', 'advertiser_type', 'longitude', 'latitude']]
    city_side_mapper = {'north': 1, 'south': 2, 'east': 3, 'west':4, 'middle':5}
    apartments['city_side'] = apartments['city_side'].apply(lambda side: city_side_mapper[side])




    # Filter...


    filters = ['price_slider', 'area_slider', 
               'beds_slider', 'livings_slider', 'bathrooms_slider', 'furnished_slider']
    
    # Dictionary of this functions' parameter names and their values
    parameters = locals()
    
    for filter in filters:
        # Get the value associated with this filter
        filter_value = parameters.get(filter)    
        
        if filter_value is not None:    
            filter_min, filter_max = filter_value[0], filter_value[1]
            
            # If filter = 'price_slider', then filter_series = 'price'
            filter_series = filter.split('_')[0]
            
            apartments = apartments.loc[((apartments[filter_series] >= filter_min) & (apartments[filter_series] <= filter_max))] 

        shape = apartments.shape
        print(f'The shape of df: {shape}')
    
    # Remaining
    apartments = apartments.groupby(['district'], as_index=False).mean()

    apartments["district"] = apartments["district"].apply(lambda x: x.strip())



    merged_df = map_df.merge(apartments, left_on=["name_ar"], right_on=["district"])

    geo_df = merged_df.set_index("district")

    return geo_df
#%%
# ==================================================

# helper functions

def make_plot(df, plot_coloring):
    fig = px.choropleth_mapbox(df,
                            geojson=df.geometry,
                            locations=df.index,
                            color=plot_coloring,
                            center={"lat": 24.79, "lon":46.70},
                            opacity=0.3, 
                            color_continuous_scale='darkmint',
                            mapbox_style="carto-positron",
                            zoom=8,
                            # title="متوسط أسعار الشقق حسب الحي (الرياض)",
                            height=1000,
                            hover_data={'price_'})
    return fig



district_features = [{'label': 'price', 'value': 'price'}, 
                     {'label': 'age', 'value': 'age'}, 
                     {'label': 'area', 'value': 'area'}, 
                     {'label': 'street width', 'value': 'street_width'}]

city_sides = [#{'label': 'All', 'value': ['north','south', 'east', 'west']}, 
              {'label': 'North', 'value': 'north'}, 
              {'label': 'South', 'value': 'south'}, 
              {'label': 'East', 'value': 'east'},
              {'label': 'West', 'value': 'west'},
              {'label': 'City center', 'value': 'middle'}]

attributes_filter = ['price', 'age', 'area', 'street_width', 'beds', 'livings', 'wc', 'furnished', 'advertiser_type']


def round_k(n):
     
    return int(n / 1000)


# ==================================================

# make Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.Div(
        html.H3('Explore Current Trends in the Real Estate Market in Riyadh'),
        style={'width':'40%', 'display': 'inline-block'}),
    
    html.Div(
        html.H4("Get assessment for an apartment's price! Enter the apartment post ID:"),
        style={'width':'15%', 'display':'inline-block'}),
    
    html.Div(
        dcc.Textarea(id='input-on-submit', placeholder="Post ID (Example: 4175521)"),
        style={'width':'15%', 'display':'inline-block'}),
    
    html.Div(
        html.Button('Submit', id='indicator-button', n_clicks=0),
        style={'width':'10%', 'display':'inline-block'}),

    html.Div(
        id='empty',
        children=[],
        style={'width':'70%'}
        ),
        
    # html.Div(
    #     id='deal_goodness',
    #     children=[],
    #     style={'width':'25%'}
    #     ),
    
    html.H4(id='deal_goodness'),

    
            
    dcc.Graph(id="graph", ),
    
    html.H4("Select a feature to color the plot"),
    # dcc.Dropdown(id="dropdown_color", options=district_features),
    dcc.RadioItems(id="radio_color", options=district_features, value="price"),
    dcc.Checklist(id="checklist_city_side", options=city_sides, value=['north']),
    
    # Choose feature to filter according
    html.H4("Filters"),
    
    # Price
    html.H5('Price'),
    dcc.RangeSlider(id='price_slider', min=0, max=apartments.price.max(),),
                    # style={'width':'50%'})
    
    
    # Age
    html.H5('Age'),
    dcc.RangeSlider(id='age_slider', min=0, max=apartments.age.max()),
    
    # Area
    html.H5('Area'),
    dcc.RangeSlider(id='area_slider', min=0, max=apartments.area.max()),
    
    
    
    # Beds
    html.H5('Number of bedrooms'),
    dcc.RangeSlider(id='beds_slider', min=0, max=apartments.beds.max()),
                    
    # Beds
    html.H5('Number of living/guest rooms'),
    dcc.RangeSlider(id='livings_slider', min=0, max=apartments.livings.max()),
    
    # Beds
    html.H5('Number of bathrooms'),
    dcc.RangeSlider(id='bathrooms_slider', min=0, max=apartments.wc.max()),
    
    # Beds
    html.H5('Furnished'),
    dcc.Slider(id='furnished_slider', min=0, max=1),
    
 
    
    
    
])


@app.callback(
              Output('deal_goodness', 'children'),
              Output("graph", "figure"), 
              Input('input-on-submit', 'value'),
              Input('indicator-button', 'n_clicks'),
              Input("radio_color", "value"),
              Input("checklist_city_side", "value"),
              
              # Filters
              Input('price_slider', 'value'),
              Input('age_slider', 'value'),
              Input('area_slider', 'value'),
              Input('beds_slider', 'value'),
              Input('livings_slider', 'value'),
              Input('bathrooms_slider', 'value'),
              Input('furnished_slider', 'value'),
              )

def app_function(post_id=0, n_clicks=0, plot_coloring='price', city_sides=['north','south', 'east', 'west'], 
                 price_slider=None, age_slider=None, area_slider=None, beds_slider=None, livings_slider=None, bathrooms_slider=None, furnished_slider=None):
    
    # Load data
    df = pd.read_csv("../data/apartments_sale_riyadh_cleaned.csv")
        
    # Assess deal_goodness 
    deal_goodness_report = ""
    if post_id != None and len(list(str(post_id))) > 1:

        deal_goodness, asking_price, predicted_price = good_deal_indicator(df, int(post_id))
        deal_goodness_report = f"This is a {deal_goodness.upper()}. Actual asking price is {round_k(asking_price)}k. Our estimate of a fair price for this apartment is: {round_k(predicted_price)}k"
    # Filter apartments dataframe
    
    # city_side_mapper = {'north': 1, 'south': 2, 'east': 3, 'west':4, 'middle':5}
    city_sides = list(pd.Series(city_sides).apply(lambda side: city_side_mapper[side]))

    # print(f'City Sides: {city_sides}')
    # print("Geo DF:",'\n',geo_df.head())
    
    # What does this do?
    geo_df = get_geo_df(price_slider, age_slider, area_slider, beds_slider, livings_slider, bathrooms_slider, furnished_slider)
    geo_df = geo_df.loc[geo_df['city_side'].apply(lambda side: side in city_sides)]
    

    
        
    geo_df['price_'] = (geo_df.price / 1000).astype('int')
    geo_df['price_'] = geo_df.price_.apply(lambda price: str(price) + 'k')
    
    # Create plot
    fig = make_plot(geo_df, plot_coloring)

    

    return deal_goodness_report, fig



#%%
app.run(debug=True)

# %%
# 4403633