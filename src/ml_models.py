#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from plotnine import *
import os 

# preprocessing 
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.preprocessing import PowerTransformer
from sklearn.preprocessing import OneHotEncoder
from feature_engine.encoding import RareLabelEncoder
from sklearn.compose import TransformedTargetRegressor
from sklearn.compose import ColumnTransformer
from sklearn.compose import make_column_selector as selector
from category_encoders.ordinal import OrdinalEncoder
from sklearn.feature_selection import VarianceThreshold
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn import cross_decomposition
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.impute import KNNImputer

# modeling
from sklearn.model_selection import train_test_split, KFold, RepeatedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold

# Ignore warnings.
import warnings
warnings.filterwarnings("ignore")

#%%
# load data
apartments = pd.read_csv("../data/apartments_sale_riyadh_cleaned.csv")
# create train-test split
train, test = train_test_split(apartments, test_size=0.3, random_state=123)

X_train = train.drop(columns='price')
y_train = train['price']

X_test = test.drop(columns='price')
y_test = test['price']




# %%
# target enginnering

y_train = PowerTransformer('box-cox').fit_transform(np.array(y_train).reshape(-1, 1))

# %%
# Numeric feature engineering
nzv_encoder = VarianceThreshold(threshold=0.1)
yj = PowerTransformer(method='yeo-johnson')
scaler = StandardScaler()

### lump the infrequent categories
# rare_encoder = RareLabelEncoder(tol=0.01, replace_with="other")

# Categorical feature engineering
dummy_encoder = OneHotEncoder()


#%%
#impute missing values
knn_imp = KNNImputer(n_neighbors=5, missing_values=np.nan)

# make all null values encoded in the same way
X_train = X_train.fillna(value=np.nan)

#%%
# combine all steps into a preprocessing pipeline
preprocessor = ColumnTransformer(
  remainder="passthrough",
  transformers=[
    
    ("nzv_encode", nzv_encoder, selector(dtype_include="number")),
    ("normalize_encode", yj, selector(dtype_include="number")),
    ("std_encode", scaler, selector(dtype_include="number")),
    ("dummy_encod", dummy_encoder, selector(dtype_include="object")),
    ("knn_impute", knn_imp, selector(dtype_include='number')),

    #   ("ord_encode", ord_encoder, ord_cols),
    # ("std_encode", scaler, selector(dtype_include="number")),
    #   ("pca_encode", pca, selector(dtype_include="number")),
    #   ("one-hot", encoder, selector(dtype_include="object")),
  ])

preprocessor_minimal = ColumnTransformer(
  remainder="passthrough",
  transformers=[
    ("dummy_encod", dummy_encoder, selector(dtype_include="object")),
    ("knn_impute", knn_imp, selector(dtype_include="number")),
  ])


# %%
lm = LinearRegression()

loss = 'neg_root_mean_squared_error'

cv = RepeatedKFold(n_splits=5, n_repeats=1)

print(f"loss function: {loss}")
print(f"cross-validation folds: 5")
print(f"cross-validation repeats: 5", end='\n\n')





#%%
preprocessed_minimal_X_train = preprocessor_minimal.fit_transform(X_train)

results_lm = cross_val_score(lm, preprocessed_minimal_X_train, y_train, cv = cv, scoring=loss)
result = np.mean(np.abs(results_lm))

print("========= Ordinary Least Squares (Minimal Preprocessing) =========")

print(f"mean score : {result}", end='\n\n')

#%%
def train_and_predict(df, to_predict):
    # not necessary
    print("the problem is in splitting the data")
    train, test = train_test_split(df, test_size=0.3)
    X_train = train.drop(columns="price")
    y_train = train['price']
    print("no problem splitting the data to train and test",end='\n\n')
    # ensure all null values have the same encoding
    X_train = X_train.fillna(value=np.nan)
    to_predict = to_predict.fillna(value=np.nan)
    print("no problem filling na values",end='\n\n')



    real_price = to_predict['price'].iloc[0]
    to_predict.drop(columns=["price"], inplace=True)
    
    
    print("no problem sitting up the test case (to predict)", end='\n\n')
    # preprocess training set and 'test' case
    preprocessed_minimal_X_train = preprocessor_minimal.fit_transform(X_train)
    preprocessed_to_predict = preprocessor_minimal.transform(to_predict)
    print("no problem preprocessing", end='\n\n')
    # preprocess training set label
    # preprocessed_y_train = PowerTransformer('box-cox').fit_transform(np.array(y_train).reshape(-1, 1))
    preprocessed_y_train = y_train

    lm.fit(preprocessed_minimal_X_train, preprocessed_y_train)
    predicted_price = lm.predict(preprocessed_to_predict)[0]
    # predicted_price = 4
    predicted_price_type = type(predicted_price)
    real_price_type = type(real_price)
    print(f"predicted price: {predicted_price}")
    print(f"real price: {real_price}")
    print(f"predicted price type: {predicted_price_type}")
    print(f"real price type: {real_price_type}", end="\n\n")
    return predicted_price, real_price
    
    




# %%
'''
preprocessed_X_train = preprocessor.fit_transform(X_train)

results_lm = cross_val_score(lm, preprocessed_X_train, y_train, cv = cv, scoring=loss)
result = np.mean(np.abs(results_lm))

print("========= Ordinary Least Squares (Extensive Preprocessing) =========")

print(f"mean score : {result}", end='\n\n')
'''
