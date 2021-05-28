from datetime import datetime
import streamlit as st
import requests
import pandas as pd
import numpy as np

@st.cache
def get_map_data():
    print('get_map_data called')
    return pd.DataFrame(
            [[pickup_longitude,pickup_latitude] , [dropoff_longitude, dropoff_latitude]],
            columns=['lat', 'lon']
        )

'''
# Welcome to the New York Taxi Fare Predictor!
'''

st.sidebar.write('## To predict your fare we first need some information about your journey')
#####################################
# INPUTS
#####################################


st.sidebar.write('''### When do you need the taxi?''')
# get the input for the date and the time
date = st.sidebar.date_input('Please choose a date:')
time = st.sidebar.time_input('And pick a time:')

# prebuild a string combining the date and the time in a fitting format for the api 
date_time = str(date) + ' ' + str(time)

st.sidebar.write('''### Now we need to know your starting location and your destination''')

# get the inputs for the pick up and the drop off
st.sidebar.write('''#### Coordinates for the pick up location:''')
pickup_longitude = st.sidebar.number_input('Longitude:', key='pickup_lon', value=40.76)
pickup_latitude = st.sidebar.number_input('Latitude:', key='pickup_lat', value=-73.97)

st.sidebar.write('''#### Coordinates for the destination:''')
dropoff_longitude = st.sidebar.number_input('Longitude:', key='dropoff_lon', value=40.76)
dropoff_latitude = st.sidebar.number_input('Latitude:', key='dropoff_lat', value=-73.97)

# show map with coordinates
df = get_map_data()
st.map(df)

# get the input for the passenger count
st.sidebar.write('''### And finally we need the number of passengers:''')
passenger_count = st.sidebar.number_input('Passengers:', min_value=1,value = 1, format='%i')

#####################################
# REQUEST TO THE API
#####################################

def get_prediction(date_time,pickup_longitude, pickup_latitude, dropoff_longitude,dropoff_latitude,passenger_count): 
    # url to the predict endpoint of the api
    url = 'https://taxifare.lewagon.ai/predict'

    # organize the inputs as parameters for the request
    params = {
        'pickup_datetime' : date_time,
        'pickup_longitude': pickup_longitude,
        'pickup_latitude': pickup_latitude,
        'dropoff_longitude': dropoff_longitude,
        'dropoff_latitude': dropoff_latitude,
        'passenger_count': passenger_count
    }

    # get request to the api 
    response = requests.get(url, params=params).json()

    # save the predicted taxi fare
    fare = response['prediction']

    return fare

#####################################
# OUTPUT
#####################################

if st.button('Predict fare'):
    fare = get_prediction(date_time,pickup_longitude, pickup_latitude, dropoff_longitude,dropoff_latitude,passenger_count)

    # output of the fare for the user
    prediction = st.success(f' Your estimated taxi fare: {round(fare, 2)} $')

