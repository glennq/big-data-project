#!/usr/bin/python

import sys

hour_cnt = {}

for line in sys.stdin:
    key, value = line.strip().split("\t", 1)
    try:
        value = int(value)
    except:
        continue
    hour_cnt[key] = hour_cnt.get(key, 0) + value

for k, v in hour_cnt.items():
    print '%s\t%d' % (k, v)
