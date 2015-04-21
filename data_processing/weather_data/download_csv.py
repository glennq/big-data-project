__author__ = 'chianti'

import requests

url = 'http://www.wunderground.com/history/airport/KNYC/2013/{}/{}/DailyHistory.html?req_city=New+York&req_state=NY&req_statename=&reqdb.zip=10106&reqdb.magic=4&reqdb.wmo=99999&format=1'

# Change the month manually, download the data for all 12 month
for j in range(1, 13):
    for i in range(1, 32):
        r = requests.get(url.format(j, i))
        data = r.text
        f = open('2013{:02}{:02}.csv'.format(j, i), 'wb')
        f.write(data)
        f.close()
