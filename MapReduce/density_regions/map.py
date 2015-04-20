#!/usr/bin/python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time
from datetime import datetime


def findNeighborhood(location, index, neighborhoods):
    match = index.intersection((location[0], location[1],
                                location[0], location[1]))
    for a in match:
        if any(map(lambda x: x.contains_point(location), neighborhoods[a][1])):
            return a
    return -1


def readNeighborhood(shapeFilename, index, neighborhoods):
    sf = shapefile.Reader(shapeFilename)
    for sr in sf.shapeRecords():
        if sr.record[1] not in ['New York', 'Kings', 'Queens', 'Bronx']:
            continue
        paths = map(Path, numpy.split(sr.shape.points, sr.shape.parts[1:]))
        bbox = paths[0].get_extents()
        map(bbox.update_from_path, paths[1:])
        index.insert(len(neighborhoods),
                     list(bbox.get_points()[0]) + list(bbox.get_points()[1]))
        neighborhoods.append((sr.record[3], paths))
    neighborhoods.append(('UNKNOWN', None))


index = rtree.Index()
neighborhoods = []
readNeighborhood('ZillowNeighborhoods-NY.shp', index, neighborhoods)

for line in sys.stdin:
    row = line.strip().split(',')
    if row[0] == 'medallion':
        continue
    pu_time_h = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S').hour
    pu_loc = (float(row[10]), float(row[11]))
    pu_region = neighborhoods[findNeighborhood(pu_loc, index,
                                               neighborhoods)][0]
    do_time_h = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S').hour
    do_loc = (float(row[12]), float(row[13]))
    do_region = neighborhoods[findNeighborhood(do_loc, index,
                                               neighborhoods)][0]
    print "%d\t%s,%s" % (pu_time_h, pu_region, '1')
    print "%d\t%s,%s" % (do_time_h, do_region, '1')
