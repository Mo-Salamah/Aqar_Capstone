from re import X
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from dash import Dash, dcc, html, Input, Output
from sklearn.model_selection import train_test_split

mesh_size = .02
margin = 1

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Explanatory k-NN plot'),
    dcc.Graph(id="graph"),
    html.P("Select number of neighbors:"),
    dcc.Slider(
        id='slider-neighbors',
        min=1, max=20, step=1, value=10,
        marks={i: str(i) for i in range(1,21,3)}),
    dcc.RadioItems(id='radio-heatmap', value='confidence', options=[{'label': 'Confidence', 'value': 'confidence'},
                                                        {'label': 'Prediction', 'value': 'prediction'}]),
    html.P("Select x and y axis:"),
    dcc.Dropdown(id='select-axis', options=[{'label':'sepal length', 'value':'sepal_length'},
                                            {'label': 'sepal width', 'value':'sepal_width'},
                                            {'label': 'petal height', 'value':'petal_length'},
                                             {'label':'petal width', 'value': 'petal_width'}],
                 value=['sepal_length', 'sepal_width'],
                 multi=True)
])

@app.callback(
    Output("graph", "figure"), 
    [Input("slider-neighbors", "value"),
     Input('radio-heatmap', 'value'),
     Input('select-axis', 'value')]
     )

def train_and_display_model(k, heat, axis):
    

    # We will use the iris data, which is included in px 
    (X_train, y_train), (X_test, y_test) = data_split(attributes=axis)
    

    # Create a mesh grid on which we will run our model
    lrange, wrange = get_range(X_train)
    ll, ww = np.meshgrid(lrange, wrange)
    
    # Create classifier, run predictions on grid
    proba = predict_proba(ll, ww, X_train, y_train, k)


    df_test = X_test.copy()
    df_test['species'] = y_test
    
    heat_type = heat
    heat = choose_heat(heat, proba)
    fig = make_fig(proba, heat, lrange, wrange, df_test, heat_type)
    
    return fig





# Helper functions =================================================


def data_split(data=px.data.iris().drop(columns='species_id'), attributes=['sepal_length', 'sepal_width']):
    if len(attributes) != 2:
        attributes = attributes[0:2]
    df_train, df_test = train_test_split(data, test_size=0.3, random_state=0)
    # X_train = df_train.iloc[:, 0:2]
    X_train = df_train[attributes]
    y_train = df_train.iloc[:, -1]

    X_test = df_test[attributes]
    y_test = df_test.iloc[:, -1]
        
    return (X_train, y_train), (X_test, y_test)

def get_range(X_train):
    l_min, l_max = X_train.iloc[:, 0].min() - margin, X_train.iloc[:, 0].max() + margin
    w_min, w_max = X_train.iloc[:, 1].min() - margin, X_train.iloc[:, 1].max() + margin
    
    lrange = np.arange(l_min, l_max, mesh_size)
    wrange = np.arange(w_min, w_max, mesh_size)
    
    return lrange, wrange

def predict_proba(ll, ww, X_train, y_train, k = 5):
    clf = KNeighborsClassifier(k, weights='distance')
    clf.fit(X_train, y_train)
    Z = clf.predict(np.c_[ll.ravel(), ww.ravel()])
    Z = Z.reshape(ll.shape)
    proba = clf.predict_proba(np.c_[ll.ravel(), ww.ravel()])
    proba = proba.reshape(ll.shape + (3,))      
    
    return proba



def make_fig(proba, diff, lrange, wrange, df_test, heat):
    fig = px.scatter(
        df_test, x=df_test.columns[0], y=df_test.columns[1], color=df_test.columns[-1]
        # symbol='species',
        # symbol_map={
        #     'setosa': 'square-dot',
        #     'versicolor': 'circle-dot',
        #     'virginica': 'diamond-dot'},
    )
    fig.update_traces(
        marker_size=12, marker_line_width=1.5,
        # marker_color="lightyellow"
    )
    print("df_test shape:"+ str(df_test.shape))
    fig.add_trace(
        go.Heatmap(
            x=lrange,
            y=wrange,
            z=diff,
            opacity=0.25,
            customdata=proba,
            colorscale='RdBu',
            hovertemplate=(
                'p(setosa): %{customdata[0]:.3f}<br>'
                'p(versicolor): %{customdata[1]:.3f}<br>'
                'p(virginica): %{customdata[2]:.3f}<extra></extra>'
            )
        )
    )
    fig.update_layout(
        legend_orientation='h',
        title= heat + 'on test split')

    
    return fig

def choose_heat(heat, proba):
    if heat == 'confidence':
        # Compute the confidence, which is the difference
        return proba.max(axis=-1) - (proba.sum(axis=-1) - proba.max(axis=-1))
        # Compute the predicted labels
    elif heat == 'prediction':
        return proba.argmax(axis=-1)
    
    


if __name__ == "__main__":
    app.run_server(debug=True)
