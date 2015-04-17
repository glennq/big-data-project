#!/usr/bin/python
import sys

region = None
year = None
month = None
day = None
hour = None
count = 0
for line in sys.stdin:
    key, longitude, latitude = line.split("\t")
    r, y, m, d, h = key.split(",")
    y = int(y)
    m = int(m)
    d = int(d)
    h = int(h)
    if r == region and y == year and m == month and d == day and h == hour:
        count = count + 1
    else:
        if region is None or year is None or month is None or day is None or hour is None:
            region, year, month, day, hour = r, y, m, d, h
            count = 1
        else:
            print "%s\t%s\t%s\t%s\t%s\t%d" %(region, year, month, day, hour, count)
            region, year, momth, day, hour = r, y, m, d, h
            count = 1
# print "%s\t%s\t%s\t%s\t%s\t%d" %(region, year, month, day, hour, count)
