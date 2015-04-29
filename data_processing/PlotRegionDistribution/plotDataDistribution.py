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

font = FontProperties(fname=r"/System/Library/Fonts/HelveticaNeue.dfont", size=12)

def readData(fileName):
    '''Read pickup data from a data structure file named fileName'''
    try:
        f = open(fileName, "rb")
        data = pickle.load(f)
        f = close()
    except Exception:
        print "Cannot open the data file due to the exception:", sys.exc_info()[0]
    return data


def plotRegionDistribution(puData, doData, weatherData, region, week, targetHour):
    """plot the pickup distribution according to specific week and hour"""
    pickupData = puData[region][week]
    dropoffData = doData[region][week]
    puNormalDistribution = []
    puUnnormalDistribution = []
    doNormalDistribution = []
    doUnnormalDistribution = []
    for weekNumber in range(52):
        if weekNumber < 10:
            weekNumber = "0" + str(weekNumber)
        else:
            weekNumber = str(weekNumber)
        d = "2013-W" + weekNumber + "-" + str(week)
        r = datetime.datetime.strptime(d, "%Y-W%W-%w")
        date = "2013-"
        if r.month < 10:
            date += "0" + str(r.month) + "-"
        else:
            date += str(r.month) + "-"

        if r.day < 10:
            date += "0" + str(r.day) + "-"
        else:
            date += str(r.day) + "-"

        if targetHour < 10:
            date += "0" + str(targetHour) 
        else:
            date += str(targetHour)
        weather = weatherData[date]
        
        try:
            if weather == "Normal":
                puNormalDistribution.append(pickupData[weekNumber][targetHour])
                doNormalDistribution.append(dropoffData[weekNumber][targetHour])
            else:
                puUnnormalDistribution.append(pickupData[weekNumber][targetHour])
                doUnnormalDistribution.append(dropoffData[weekNumber][targetHour])
        except:
            pass
    
    maxNumPuNormal = max(puNormalDistribution)
    minNumPuNormal = min(puNormalDistribution)
    maxNumDoNormal = max(doNormalDistribution)
    minNumDoNormal = min(doNormalDistribution)
    maxNumNormal = max(maxNumPuNormal, maxNumDoNormal)
    minNumNormal = min(minNumPuNormal, minNumDoNormal)
   
    maxNumPuUnnormal = max(puUnnormalDistribution)
    minNumPuUnnormal = min(puUnnormalDistribution)
    maxNumDoUnnormal = max(doUnnormalDistribution)
    minNumDoUnnormal = min(doUnnormalDistribution)
    maxNumUnnormal = max(maxNumPuUnnormal, maxNumDoUnnormal)
    minNumUnnormal = min(minNumPuUnnormal, minNumDoUnnormal)


    bucketSizeNormal = (maxNumNormal - minNumNormal) / 9
    numNormalDistribution = {}
    for num in puNormalDistribution:
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
    
    for num in doNormalDistribution:
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
    for num in puUnnormalDistribution:
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
    
    for num in doUnnormalDistribution:
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

    rect1 = plt.bar(XNormal, numNormalDistribution.values(), alpha=0.5, 
        color='#5fafff', align='center', width=1, label='Normal Weather')
    autolabel(rect1)
    
    XticksNormal = []
    XticksUnnormal = []
    for i in range(9):
        sNormal = str(minNumNormal + i * bucketSizeNormal) + "~" + str(minNumNormal + (i + 1) * bucketSizeNormal - 1)
        sUnnormal = str(minNumUnnormal + i * bucketSizeUnnormal) + "~" + str(minNumUnnormal + (i + 1) * bucketSizeUnnormal - 1)
        XticksNormal.append(sNormal)
        XticksUnnormal.append(sUnnormal)
    XticksNormal.append("> " + str(minNumNormal + 9 * bucketSizeNormal - 1))
    XticksUnnormal.append("> " + str(minNumUnnormal + 9 * bucketSizeUnnormal - 1))
    plt.xticks(XNormal, XticksNormal, fontproperties=font, fontsize=8)
    plt.xlabel("Taxi Traffic Count Range", fontproperties=font)
    plt.ylabel("Number of Times", fontproperties=font)
    plt.title("Taxi Traffic Distribution", y=1.04, fontproperties=font)
    plt.legend(prop=font)
    
    if len(region.split(" ")) > 1:
        region = region.replace(" ", "_")
    
    plt.savefig("%s_Normal_%d_%d.png" % (region, week, targetHour))
    
    plt.figure()
    rect2 = plt.bar(XUnnormal, numUnnormalDistribution.values(), alpha=0.5, 
        color='#5fafff', align='center', width=1, label='Unnormal Weather')
    autolabel(rect2)
    plt.xticks(XUnnormal, XticksUnnormal, fontproperties=font, fontsize=8)
    plt.xlabel("Taxi Traffic Count Range", fontproperties=font)
    plt.ylabel("Number of Times", fontproperties=font)
    plt.title("Taxi Traffic Distribution", y=1.04, fontproperties=font)
    plt.legend(prop=font)
    
    plt.savefig("%s_Unnormal_%d_%d.png" % (region, week, targetHour))

def autolabel(rect):
    '''Add text label to every column in the bar plot''' 
    
    for i in range(len(rect)):
        height = rect[i].get_height()
        plt.text(rect[i].get_x()+rect[i].get_width()/4., 0.1 + height, '%d' %int(height), fontproperties=font)
    return 


def getDataFromATimePeriod(region, startMonth, startDay, startHour, endMonth, endDay, endHour, data):
    """
    show the distribution of pickup data from a specific time period

    @para region:                           The region which you want to see the distribution in.
          startMonth, startDay, startHour:  The time period starts at the startMonth, startDay, startHour. For example, March, 3th, 3:00.
          endMonth,   endDay,   endHour:    The time period ends at the endMonth, endDay, endHour. For example, March, 4th, 18:00.
          data:                             The day can be pick up data or drop off data.
                                            The format of the data is a nested dictionary: {region:{month:{day:{hour: count}}}}
                                            month ranges from 1-12
                                            hour ranges from 0-23
    """
    regionData = data[region]
    dataList = []
    for month in range(startMonth, endMonth + 1):
        if month == startMonth:
            for day in regionData[month]:
                if day == startDay:
                    for hour in regionData[month][day]:
                        if hour >= startHour:
                            dataList.append(regionData[month][day][hour])
                elif day > startDay:
                    for hour in regionData[month][day]:
                        dataList.append(regionData[month][day][hour])
        elif month == endMonth:
            for day in regionData[month]:
                if day == endDay:
                    for hour in regionData[month][day]:
                        if hour <= endHour:
                            dataList.append(regionData[month][day][hour])
                elif day < endDay:
                    for hour in regionData[month][day]:
                        dataList.append(regionData[month][day][hour])
        elif month > startMonth and month < endMonth:
            for day in regionData[month]:
                for hour in regionData[month][day]:
                    dataList.append(regionData[month][day][hour])
    X = np.arange(len(dataList))
    plt.plot(X, dataList)
    plt.title("pickup number distribution")
    plt.savefig("dist.png")


if __name__ == "__main__":
    weatherData = readData("weatherData.pkl")
    puData = readData("puWeekdayData.pkl")
    doData = readData("doWeekdayData.pkl")
    plotRegionDistribution(puData, doData, weatherData, "Sunny Side", 2, 13)
    # tripData = readData("puData.pkl")
    # getDataFromATimePeriod("Chinatown", 2, 4, 5, 2, 9, 22, tripData)
