#!/usr/bin/python
import sys
import numpy as np

region_cnt = {}
current_hour = None
regions_set = False
regions_high_density = set()
regions_low_density = set()


def findHLDensityRegions(region_cnt):
    upper = np.percentile(region_cnt.values(), 70)
    lower = np.percentile(region_cnt.values(), 30)
    high_density = set()
    low_density = set()
    for k, v in region_cnt.items():
        if v >= upper:
            high_density.add(k)
        if v <= lower:
            low_density.add(k)
    return high_density, low_density

for line in sys.stdin:
    hour, v = line.strip().split("\t", 1)
    region, value = v.split(',', 1)
    if not regions_set:
        regions_high_density.add(region)
        regions_low_density.add(region)
    try:
        value = int(value)
    except:
        continue

    if hour == current_hour:
        region_cnt[region] = region_cnt.get(region, 0) + 1
    else:
        if current_hour:
            regions_set = True
            high, low = findHLDensityRegions(region_cnt)
            regions_high_density.intersection_update(high)
            regions_low_density.intersection_update(low)
        region_cnt = {region: value}
        current_hour = hour

if current_hour:
    high, low = findHLDensityRegions(region_cnt)
    regions_high_density.intersection_update(high)
    regions_low_density.intersection_update(low)

for i in regions_high_density:
    print '%s\t%s' % ('high_density', i)
for i in regions_low_density:
    print '%s\t%s' % ('low_density', i)
