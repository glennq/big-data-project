#!/usr/bin/python

import sys
from datetime import datetime


for line in sys.stdin:
    row = line.strip().split(',')
    if row[0] == 'medallion':
        continue
    pu_week_day = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S').weekday()
    do_week_day = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S').weekday()
    print "%d\t%s" % (pu_week_day, '1')
    print "%d\t%s" % (do_week_day, '1')
