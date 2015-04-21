__author__ = 'chianti'

import requests
import numpy as np

# Change the month manually, download the data for all 12 months
for i in np.arange(1, 32):
    r = requests.get('http://www.wunderground.com/history/airport/KNYC/2013/12/'+str(i)+'/DailyHistory.html?req_city=New+York&req_state=NY&req_statename=&reqdb.zip=10106&reqdb.magic=4&reqdb.wmo=99999&format=1')
    data = r.text
    f = open('201312'+str(i).zfill(2)+'.csv', 'a')
    f.write(data)
    f.close()

