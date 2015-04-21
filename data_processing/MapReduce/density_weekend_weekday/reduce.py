#!/usr/bin/python

import sys

weekday_cnt = {}

for line in sys.stdin:
    key, value = line.strip().split("\t", 1)
    try:
        value = int(value)
        key = 'weekday' if int(key) < 5 else 'weekend'
    except:
        continue
    weekday_cnt[key] = weekday_cnt.get(key, 0) + value

for k, v in weekday_cnt.items():
    print '%s\t%d' % (k, v)
