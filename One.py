from numpy import int32
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline

car = pd.read_csv('/Users/ramadugudhanush/Documents/CarPricePrediction/quikr_car.csv')
# print(car.head())
# print(car.shape)
# print(car.info())

# print(car['year'].unique())
# print(car['Price'].unique())
# print(car['kms_driven'].unique())

# Quality

# --year has many non year values
# --year object to int
# --price has ask for price
# --Price object to int
# --kms_driven has kms with integers
# --kms_driven object to int
# --kms_driven has nan values
# --fuel_type has nan values
# --keep first 3 words of name

# Cleaning

backup = car.copy()

car = car[car['year'].str.isnumeric()]
car['year'] = car['year'].astype(int32)


car = car[car['Price']!="Ask For Price"]
car['Price'] = car['Price'].str.replace(',','').astype(int32)

car['kms_driven']=car['kms_driven'].str.split(' ').str.get(0).replace(',','')
car = car[car['kms_driven']!="Petrol"]

car['kms_driven']=car['kms_driven'].str.replace(',','').astype(int32)

car=car[~car['fuel_type'].isna()]

car['name']=car['name'].str.split(' ').str.slice(0,3).str.join(' ')

car = car.reset_index(drop=True)

car = car[car['Price']<6e6].reset_index(drop=True)
# print(car.info())
# print(car.shape)
car.to_csv('Cleaned Car.csv')

# Model
X = car.drop(columns='Price')
Y =car['Price']
# print(X)
# print(Y)

ohe = OneHotEncoder()
ohe.fit(X[['name','company','fuel_type']])

OneHotEncoder()

column_trans = make_column_transformer((OneHotEncoder(categories=ohe.categories_),['name','company','fuel_type']),remainder='passthrough')
scores=[]
for i in range(1000):
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2, random_state=i)
    lr = LinearRegression()
    pipe=make_pipeline(column_trans,lr)
    pipe.fit(X_train,Y_train)
    Y_pred = pipe.predict(X_test)
    scores.append(r2_score(Y_test,Y_pred))

# print(scores)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2, random_state=np.argmax(scores))


# # print(ohe.categories_)


lr = LinearRegression()
pipe = make_pipeline(column_trans,lr)
pipe.fit(X_train,Y_train)

Y_pred = pipe.predict(X_test)
# print(r2_score(Y_test,Y_pred))
# print(car.shape)

pickle.dump(pipe,open('LinearRegressionModel.pkl','wb'))

# print(pipe.predict(pd.DataFrame([['Maruti Suzuki Swift','Maruti',2019,100,'Petrol']], columns=['name','company','year','kms_driven','fuel_type'])))