__author__ = 'chianti'

import pandas as pd
import numpy as np
import time

def read_weather_data(file_name):

    file = '/Users/chianti/Documents/1004BigData/BigDataProject/new_weather/'+file_name+'.csv'
    df = pd.read_csv(file)
    #print file_name, 'done'
    try:
        df['Hour'] = df['TimeEST'].map(lambda x: time.strptime(x, "%I:%M %p").tm_hour)
    except:
        df['Hour'] = df['TimeEDT'].map(lambda x: time.strptime(x, "%I:%M %p").tm_hour)
    #df['Min'] = df['TimeEST'].map(lambda x: time.strptime(x, "%I:%M %p").tm_min)
    #df['Round_hour'] = df['Min'].map(lambda x: 1 if x > 30 else 0)
    #df['Hour'] = df['Round_hour'] + df['Hour']
    df['Time'] = df['Hour'].map(lambda x: file_name+str(x).zfill(2))
    df = df[['Time', 'Conditions']]
    df = df.drop_duplicates(cols='Time')
    df = df.set_index('Time')

    return df

for j in np.arange(1, 13):
    for i in np.arange(1, 32):
        try:
            test_file = '2013'+str(j).zfill(2)+str(i).zfill(2)
            df = read_weather_data(test_file)
            df.to_csv('cleaned_weather_'+test_file+'.csv', sep=',')
        except:
            continue

print 'done'