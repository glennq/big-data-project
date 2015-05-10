import pickle
import sys
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import collections
import seaborn as sns
import pandas as pd
import datetime
from matplotlib import rc
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"/System/Library/Fonts/Helvetica.dfont", size=14)
numFont = FontProperties(fname=r"/System/Library/Fonts/Helvetica.dfont", size=16)
log = open("log.txt", "w")


def readData(fileName):
    '''Read pickup data from a data structure file named fileName'''
    try:
        f = open(fileName, "rb")
        data = pickle.load(f)
        f = close()
    except Exception:
        print "Cannot open the data file due to the exception:", sys.exc_info()[0]
    return data


def plotTaxiTrafficDistribution(data, weatherData, region, week, targetHour):
    """plot the pickup distribution according to specific week and hour"""
    if region not in data:
        return
    if week not in data[region]:
        return
    total_data = data[region][week]
    NormalDistribution = []
    UnnormalDistribution = []
    for weekNumber in range(54):
        totalDate = []
        for hour in targetHour:
            for i in range(1, 4):
                if weekNumber < 10:
                    weekNumber = "0" + str(weekNumber)
                else:
                    weekNumber = str(weekNumber)
                d = "201" + str(i) + "-W" + weekNumber + "-" + str(1)
                try:
                    r = datetime.datetime.strptime(d, "%Y-W%W-%w")
                except:
                    log.write("date %s %d %d\n" % (region, week, targetHour[0]))
                date = "201" + str(i) + "-"
                if r.month < 10:
                    date += "0" + str(r.month) + "-"
                else:
                    date += str(r.month) + "-"
                if r.day < 10:
                    date += "0" + str(r.day) + "-"
                else:
                    date += str(r.day) + "-"
                if hour < 10:
                    date += "0" + str(hour)
                else:
                    date += str(hour)
                totalDate.append(date)
        try:
            unnormalCount = 0
            for date in totalDate:
                if str(date) in weatherData:
                    if weatherData[date] == "Unnormal":
                        unnormalCount += 1
            if unnormalCount > 0:
                weather = "Unnormal"
            else:
                weather = "Normal"
                        
            if weather == "Normal":
                for hour in targetHour:
                    NormalDistribution.append(total_data[weekNumber][hour])
            else:
                for hour in targetHour:
                    UnnormalDistribution.append(total_data[weekNumber][hour])
        except Exception:
            log.write("weather %s %d %d\n" % (region, week, targetHour[0]))
    try: 
        maxNumNormal = max(NormalDistribution)
        minNumNormal = min(NormalDistribution)

        maxNumUnnormal = max(UnnormalDistribution)
        minNumUnnormal = min(UnnormalDistribution)

    except Exception:
        log.write("Min-max null list problem %s %d %d\n" % (region, week, targetHour[0])

    try: 
        bucketSizeNormal = (maxNumNormal - minNumNormal) / 9
        numNormalDistribution = {}
        for num in NormalDistribution:
            k = (num - minNumNormal) / bucketSizeNormal
            if k > 9:
                k = 9
            if (minNumNormal + k * bucketSizeNormal) in numNormalDistribution:
                numNormalDistribution[minNumNormal + k * bucketSizeNormal] += 1
            else:
                numNormalDistribution[minNumNormal + k * bucketSizeNormal] = 1
        for i in range(10):
            if minNumNormal + i * bucketSizeNormal not in numNormalDistribution:
                numNormalDistribution[minNumNormal + i * bucketSizeNormal] = 0

        numNormalDistribution = collections.OrderedDict(sorted(numNormalDistribution.items()))

        bucketSizeUnnormal = (maxNumUnnormal - minNumUnnormal) / 9
        numUnnormalDistribution = {}
        for num in UnnormalDistribution:
            k = (num - minNumUnnormal) / bucketSizeUnnormal
            if k > 9:
                k = 9
            if (minNumUnnormal + k * bucketSizeUnnormal) in numUnnormalDistribution:
                numUnnormalDistribution[minNumUnnormal + k * bucketSizeUnnormal] += 1
            else:
                numUnnormalDistribution[minNumUnnormal + k * bucketSizeUnnormal] = 1
        for i in range(10):
            if minNumUnnormal + i * bucketSizeUnnormal not in numUnnormalDistribution:
                numUnnormalDistribution[minNumUnnormal + i * bucketSizeUnnormal] = 0
        numUnnormalDistribution = collections.OrderedDict(sorted(numUnnormalDistribution.items()))

        dfNormal = pd.DataFrame(data=numNormalDistribution, index=range(1))
        dfUnnormal = pd.DataFrame(data=numUnnormalDistribution, index=range(1, 2))

        XNormal = np.arange(len(numNormalDistribution))
        XUnnormal = np.arange(len(numUnnormalDistribution))

        plt.figure()
        rect1 = plt.bar(XNormal, numNormalDistribution.values(), alpha=0.5, 
            color='#5fafff', align='center', width=1, label='Normal Weather')
        autolabel(rect1)


        maxValue = max(numNormalDistribution.values())

        XticksNormal = []
        XticksUnnormal = []
        for i in range(9):
            sNormal = str(minNumNormal + i * bucketSizeNormal) + "~" + str(minNumNormal + (i + 1) * bucketSizeNormal - 1)
            sUnnormal = str(minNumUnnormal + i * bucketSizeUnnormal) + "~" + str(minNumUnnormal + (i + 1) * bucketSizeUnnormal - 1)
            XticksNormal.append(sNormal)
            XticksUnnormal.append(sUnnormal)
        XticksNormal.append("> " + str(minNumNormal + 9 * bucketSizeNormal - 1))
        XticksUnnormal.append("> " + str(minNumUnnormal + 9 * bucketSizeUnnormal - 1))
        plt.xticks(XNormal, XticksNormal, fontproperties=font, rotation=30, fontsize=12)

        y = np.arange(0, int(maxValue * 1.2) + 3, int(maxValue * 1.2) / 4)
        plt.yticks(y, fontproperties=font)

        if len(region.split(" ")) > 1:
            region = region.replace(" ", "_")

        plt.savefig("pic/%s_Normal_%d_%d_%d.png" % (region, week, targetHour[0], targetHour[-1]), bbox_inches='tight')
        plt.figure()
        rect2 = plt.bar(XUnnormal, numUnnormalDistribution.values(), alpha=0.5, 
            color='#5fafff', align='center', width=1, label='Unnormal Weather')
        maxUnValue = max(numUnnormalDistribution.values())
        autolabel(rect2)
        y = np.arange(0, int(maxUnValue * 1.2) + 3, int(maxUnValue * 1.2) / 4)
        plt.xticks(XUnnormal, XticksUnnormal, fontproperties=font, rotation=30, fontsize=12)
        plt.yticks(y, fontproperties=font)
        plt.savefig("pic/%s_Unnormal_%d_%d_%d.png" % (region, week, targetHour[0], targetHour[-1]), bbox_inches='tight')
    except:
        log.write("plot problem %s %d %d\n" % (region, week, targetHour[0]))


def autolabel(rect):
    '''Add text label to every column in the bar plot''' 
    max = 0
    for i in range(len(rect)):
        if rect[i].get_height() > max:
            max = rect[i].get_height()
    for i in range(len(rect)):
        height = rect[i].get_height()
        if height == 0:
            continue
        plt.text(rect[i].get_x()+rect[i].get_width()/4., max * 0.02 + height, '%d' %int(height), fontproperties=numFont)
    return 


if __name__ == "__main__":
    weatherData = readData("weatherData.pkl")
    data = readData("WeekdayData.pkl")
    regions = data.keys()
    for region in regions:
        for week in range(1, 8):
            for hour in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23]]:
                print "============generating %s  weekday %d  hour %d's picture============"%(region, week, hour[0])
                plotRegionDistribution(data, weatherData, region, week, hour)
                print "============%s  weekday %d  hour %d's picture has been generated============"%(region, week, hour[0])
