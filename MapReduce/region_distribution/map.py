#!/usr/bin/env python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time
import random
from datetime import datetime
from datetime import date


def findNeighborhood(location, index, neighborhoods, recursionTimes):
    if recursionTimes > 4:
        return -1
    match = index.intersection((location[0], location[1], location[0], location[1]))
    for a in match:
        if any(map(lambda x: x.contains_point(location), neighborhoods[a][1])):
            return a
    
    n = random.randint(1, 4)

    if n == 1:
        longitude = location[0] + 0.1
        latitude = location[1]
        newLocation = (longitude, latitude)
        return findNeighborhood(newLocation, index, neighborhoods, recursionTimes + 1)
    elif n == 2:
        longitude = location[0] - 0.1
        latitude = location[1]
        newLocation = (longitude, latitude)
        return findNeighborhood(newLocation, index, neighborhoods, recursionTimes + 1)
    elif n == 3:
        longitude = location[0]
        latitude = location[1] + 0.1
        newLocation = (longitude, latitude)
        location[1] += 0.1
        return findNeighborhood(newLocation, index, neighborhoods, recursionTimes + 1)
    elif n == 4:
        longitude = location[0]
        latitude = location[1] - 0.1
        newLocation = (longitude, latitude)
        return findNeighborhood(newLocation, index, neighborhoods, recursionTimes + 1)
    
    return -1


def readNeighborhood(shapeFilename, index, neighborhoods):
    sf = shapefile.Reader(shapeFilename)
    for sr in sf.shapeRecords():
        if sr.record[1] not in ['New York', 'Kings', 'Queens', 'Bronx']: continue
        paths = map(Path, numpy.split(sr.shape.points, sr.shape.parts[1:]))
        bbox = paths[0].get_extents()
        map(bbox.update_from_path, paths[1:])
        index.insert(len(neighborhoods), list(bbox.get_points()[0])+list(bbox.get_points()[1]))
        neighborhoods.append((sr.record[3], paths))
    neighborhoods.append(('UNKNOWN', None))


def mapper():
    index = rtree.Index()
    neighborhoods = []
    readNeighborhood('ZillowNeighborhoods-NY.shp', index, neighborhoods)
    agg = {}
    for line in sys.stdin:
        line = line.strip('\n')
        values = line.split(',')
        if len(values) > 1 and values[0] != 'medallion': 
            try:
                pickup_location = (float(values[10]), float(values[11]))
                pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods, 0)
                
                dropoff_location = (float(values[12])), float(values[13])
                dropoff_neighborhood = findNeighborhood(dropoff_location, index, neighborhoods, 0)

                pickup_year = datetime.strptime(values[5], '%Y-%m-%d %H:%M:%S').year
                pickup_month = datetime.strptime(values[5], '%Y-%m-%d %H:%M:%S').month
                pickup_day = datetime.strptime(values[5], '%Y-%m-%d %H:%M:%S').day
                pickup_hour = datetime.strptime(values[5], '%Y-%m-%d %H:%M:%S').hour
                pickup_weekday = date(pickup_year, pickup_month, pickup_day).isoweekday()

                dropoff_year = datetime.strptime(values[6], '%Y-%m-%d %H:%M:%S').year
                dropoff_month = datetime.strptime(values[6], '%Y-%m-%d %H:%M:%S').month
                dropoff_day = datetime.strptime(values[6], '%Y-%m-%d %H:%M:%S').day
                dropoff_hour = datetime.strptime(values[6], '%Y-%m-%d %H:%M:%S').hour
                dropoff_weekday = date(dropoff_year, dropoff_month, dropoff_day).isoweekday()

                if pickup_neighborhood != -1:
                    pickupRegion = neighborhoods[pickup_neighborhood][0]
                    print "%s,%d,%d,%d,%d,%d\t%s\t%s" %(pickupRegion, pickup_year, pickup_month, pickup_day, pickup_hour, pickup_weekday, values[10], values[11])
                
                # if dropoff_neighborhood != -1:
                #     dropoffRegion = neighborhoods[dropoff_neighborhood][0]
                #     print "%s,%d,%d,%d,%d,%d\t%s\t%s" %(dropoffRegion, dropoff_year, dropoff_month, dropoff_day, dropoff_hour, dropoff_weekday, values[12], values[13])
                    #print '%s\t%s' dd% (neighborhoods[item[0]][0], item[1])
            except Exception:
                pass

if __name__ == '__main__':
    mapper()
