#!/usr/bin/python
import sys

medallion = None
hack_license = None
pick_time = None
pick_weekday = None
current_pick_time = None
current_count = 0


for line in sys.stdin:

    pick_time, info, count = line.split('\t')
    medallion, hack_license, pick_weekday = info.split(',')

    try:
        count = int(count)
    except:
        continue


    if current_pick_time == pick_time:
        
        current_count += count
    
    else:
        
        if current_pick_time == None:

            current_pick_time = pick_time
            current_count = count
        
        else:
            print "%s\t%d" %(current_pick_time, current_count)
 
            current_pick_time = pick_time
            current_count = count

print "%s\t%d" %(current_pick_time, current_count)


