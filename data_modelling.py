import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from pandas import read_csv
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import datetime

from sklearn.metrics import mean_squared_error
import dateutil.parser # for handling the conversion of datetime formats
from datetime import timedelta # for operating the datetime objects
from statsmodels.tsa. statespace.sarimax import SARIMAX

import warnings
warnings.filterwarnings('ignore')

url = 'assets/processed_data/output.csv'
df = pd.read_csv(url, index_col = 'year', parse_dates=True, infer_datetime_format=True)
df = df.sort_index(axis=0, level=None, ascending=True, inplace=False, kind='quicksort', na_position='last', sort_remaining=True, ignore_index=False, key=None)
countries=df['country'].unique()

# Add a attribute name to add it in the prediction/forecasting
columns = ['sucid_in_hundredk']


# This function will generate a dataframe out of a time series list
def time_to_df(list1, number_of_attributes = 3):
    df = pd.DataFrame(columns=range(number_of_attributes))
    
    for i in range(len(list1)-number_of_attributes+1):
        record = []
        for j in range(i,i+number_of_attributes):
            record.append(list1[j])
        df.loc[len(df.index)] = record
        
        
    return df


# This function trains the model using the input data(dataframe)
def train_and_forecast(list1, number_of_forecast = 5, npast_year =0, number_of_attributes = 3):

    input1 = time_to_df(list1, number_of_attributes)
    # We take last column of the features as target and rest are taken as attributes
    featureMat = input1.iloc[:, : len(input1.columns) - 1]
    label = input1[input1.columns[-1]]
    train_features, test_features, train_res, test_res= train_test_split(featureMat,label,test_size=0.4)
    
    # Here we are using linear regression model
    #model = linear_model.LinearRegression()
    model = linear_model.ElasticNet(alpha = 0.7)
    model.fit(train_features, train_res)
    test_result = model.predict(test_features)
    # Checking for the score
    #print("Score (R2 score): ", model.score(test_features, test_res))
    print("MSE Score: ", int(100*((1/len(test_res))*np.sum(test_result - test_res))*(1/len(test_res))*np.sum(test_result - test_res))/100)

    forecasted_values = []
    if(npast_year != 0):
        list_for_forcasting = list1[:-npast_year]
    else:
        list_for_forcasting = list1
    for i in range(number_of_forecast+npast_year):
        
        features_for_forecast = list_for_forcasting[-number_of_attributes+1:]
        forecasted_value = model.predict([features_for_forecast])[0]
        forecasted_values.append(forecasted_value)
        list_for_forcasting.append(forecasted_value)
        
    return forecasted_values

    
def AR_forecast(series, nforecast_year = 10, npast_year =0, p = 3):

    number_of_forecast = nforecast_year
    
    # Generate predictions
    forecasts = train_and_forecast(series.to_list(), number_of_forecast, npast_year, p+1)
    forecasts_ser = pd.Series(forecasts, copy=False)
    to_plot=forecasted_series_to_df(series, forecasts_ser, npast_year, str(series.name), "Date")

    return to_plot, series

# function to check if the year is leap year or not
def is_leap_year(year):

    if (year%4) == 0:
        if (year%100) == 0:
            if (year%400) == 0:
                return True
            else:
                return False
        else:
             return True
    else:
        return False

def forecasted_series_to_df(series, forecasted_series_, npast_year, name_of_forecasted_column, name_of_datetime_index_column):
  forecasted_series = forecasted_series_.copy()
  y = 0
  index_for_forcaste = []
  index_for_forcaste.append(series.index[-npast_year-1])
  for i in range(len(forecasted_series)-1):
    y = y+1
    date_temp = index_for_forcaste[-1]
    if(is_leap_year(date_temp.year)):
      date_temp = date_temp + timedelta(days = 366)
    else:
      date_temp = date_temp + timedelta(days = 365)
    index_for_forcaste.append(date_temp)

  forecasted_series.index = pd.to_datetime(index_for_forcaste)

  forecasted_series = pd.DataFrame({name_of_datetime_index_column:forecasted_series.index, name_of_forecasted_column:forecasted_series.values})
  forecasted_series.index = forecasted_series[name_of_datetime_index_column]
  forecasted_series = forecasted_series.drop(name_of_datetime_index_column, axis = 1)

  return forecasted_series



for i, country in enumerate(countries):
    print("Creating a time series for country ",country," with parameter ", columns)
    country_df = df[(df.country == country)]
    country_with_columns = pd.DataFrame(country_df, columns=columns)
    # adding all deaths together and group by year
    country_with_columns = country_with_columns.groupby(['year'])[columns].transform('sum')
    #country_with_columns = pd.Series.to_frame(country_with_columns)
    country_with_columns['year'] = list(country_with_columns.index)
    country_with_columns = country_with_columns.drop_duplicates()
    country_with_columns = country_with_columns.drop(labels='year', axis=1)

    country_with_columns.to_csv('assets/processed_data/country_wise/data/'+str(country)+'.csv')

print("All files are written in the directory.")
print("\n"*5)


# evaluate an SARIMA model for a given order (p,d,q)
def evaluate_sarima_model(X, sarima_order):

    # prepare training dataset
    train_size = int(len(X) * 0.66)
    train, test = X[0:train_size], X[train_size:]
    history = [x for x in train]

    # make predictions
    predictions = list()

    for t in range(len(test)):
        model = SARIMAX(history, order=sarima_order)
        model_fit = model.fit(disp=0)
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test[t])

    # calculate out of sample error
    rmse = sqrt(mean_squared_error(test, predictions))

    return rmse

# evaluate combinations of p, d and q values for an SARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
    
    dataset = dataset.astype('float32')
    best_score, best_cfg = float("inf"), None

    for p in p_values:

        for d in d_values:

            for q in q_values:

                order = (p,d,q)
                try:
                    rmse = evaluate_sarima_model(dataset, order)
                    if rmse < best_score:
                        best_score, best_cfg = rmse, order
                    #print('SARIMA%s RMSE=%.3f' % (order,rmse))
                except:
                    continue

        #print('Best SARIMA%s RMSE=%.3f' % (best_cfg, best_score))

    print('Best SARIMA%s RMSE=%.3f' % (best_cfg, best_score))
    return best_cfg, best_score


def forecast(country,npast_year = 0, nforecast_year = 5):

    series = read_csv('assets/processed_data/country_wise/data/'+str(country)+'.csv', header=0, index_col=0, parse_dates=True)
    first_time = True
    for parameter_to_forecast in series.columns:
        if parameter_to_forecast == 'year':
            pass
        else:
            # evaluate parameters
            p_values = [0, 1, 2, 4, 6]
            d_values = range(0, 3)
            q_values = range(0, 3)
            
            tdf = series[parameter_to_forecast].copy()
            tdf.index = series.index
            tdf = tdf.squeeze()
           
            # selecting best model using grid search
            best_cfg, best_score = evaluate_models(tdf.values, p_values, d_values, q_values)
            # Instantiate the model
           
            model = SARIMAX(series[parameter_to_forecast], order=best_cfg)

            # Fit the model
            results = model.fit()

            # Generate predictions
            forecasts = results.get_prediction(start=len(series)-npast_year,end = len(series)+nforecast_year-1)
            forecasted_1, actual = AR_forecast(series[parameter_to_forecast], 
                nforecast_year = nforecast_year,npast_year = npast_year, p = 5)
            forcasted_final = [actual.to_list()[-1]]
            forcasted_final.extend(forecasted_1[parameter_to_forecast].to_list())
            
            
            mean_forecast_sarima = forecasts.predicted_mean

            forcasted_final_sarima = [actual.to_list()[-1]]
            forcasted_final_sarima.extend(mean_forecast_sarima.to_list())
            forcasted_final_sarima = pd.Series(forcasted_final_sarima, copy=False)
            
            print("Forecasting for country: ", country)

            to_plot=forecasted_series_to_df(series[parameter_to_forecast], forcasted_final_sarima, npast_year, str(parameter_to_forecast), "year")
            to_plot[parameter_to_forecast+"_sarimax"] = to_plot[parameter_to_forecast]
            to_plot[parameter_to_forecast+"_AR"] = forcasted_final
            to_plot=to_plot.drop([parameter_to_forecast], axis = 1)

            to_plot[parameter_to_forecast+"_sarimax"] = to_plot[parameter_to_forecast+"_sarimax"].apply(lambda x: int(x*100)/100)
            to_plot[parameter_to_forecast+"_AR"] = to_plot[parameter_to_forecast+"_AR"].apply(lambda x: int(x*100)/100)


            if first_time:
                first_time = False
                temp = to_plot.copy()
            else:
                temp=pd.merge(to_plot, temp, on = "year", how = 'right')





    # writting forecastes to the hard-disk
    temp.to_csv('assets/processed_data/country_wise/forecasted/'+str(country)+'.csv')

    return temp, series


for i, country in enumerate(countries):

    to_plot, series = forecast(country = country, npast_year = 0, nforecast_year = 15)
    print("Progress: ",int(i*10000/len(countries))/100,"%")