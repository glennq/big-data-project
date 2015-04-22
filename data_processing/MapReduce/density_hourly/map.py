#!/usr/bin/python

import sys
from datetime import datetime


for line in sys.stdin:
    row = line.strip().split(',')
    if row[0] == 'medallion':
        continue
    pu_time_h = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S').hour
    do_time_h = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S').hour
    print "%d\t%s" % (pu_time_h, '1')
    print "%d\t%s" % (do_time_h, '1')
