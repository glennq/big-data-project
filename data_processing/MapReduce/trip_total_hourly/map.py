#!/usr/bin/python
import sys
import random
import datetime
from sets import Set



def deleteWhiteSpace(str):
    """docstring for deleteWhiteSpace"""
    return str.strip()


for line in sys.stdin:
    line = line.strip()
    unpack = line.split(",")
    if len(unpack[0]) == 9:
        continue
    try:
        medallion, hack_license, vendor_id, rate_code, store_and_fwd_flag, pickup_datetime, dropoff_datetime, passenger_count, trip_time_in_secs, trip_distance, pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude = unpack
        
        time_info = datetime.datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
                
        pick_weekday = time_info.weekday()
        pick_time = str(time_info.year)+str(time_info.month).zfill(2)+str(time_info.day).zfill(2)+str(time_info.hour).zfill(2)
	
	
	print pick_time+'\t'+medallion+','+hack_license+','+str(pick_weekday)+'\t'+str(1)
	
    except:
        continue
