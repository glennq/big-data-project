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


def readData(fileName):
    '''Read pickup data from a data structure file named fileName'''
    try:
        f = open(fileName, "rb")
        data = pickle.load(f)
        f = close()
    except Exception:
        print "Cannot open the data file due to the exception:", sys.exc_info()[0]
    return data


def plotRegionDistribution(puData, doData, region, week, targetHour):
    """plot the pickup distribution according to specific week and hour"""
    pickupData = puData[region][week]
    dropoffData = doData[region][week]
    puDistribution = []
    doDistribution = []
    for weekNumber in pickupData:
        puDistribution.append(pickupData[weekNumber][targetHour])
    for weekNumber in dropoffData:
        doDistribution.append(dropoffData[weekNumber][targetHour])
    
    maxNumPu = max(puDistribution)
    minNumPu = min(puDistribution)
    maxNumDo = max(doDistribution)
    minNumDo = min(doDistribution)
    maxNum = max(maxNumPu, maxNumDo)
    minNum = min(minNumPu, minNumDo)

    bucketSize = (maxNum - minNum) / 9
    print "bucketSize =", bucketSize
    numPuDistribution = {}
    for num in puDistribution:
        k = (num - minNum) / bucketSize
        if (minNum + k * bucketSize) in numPuDistribution:
            numPuDistribution[minNum + k * bucketSize] += 1
        else:
            numPuDistribution[minNum + k * bucketSize] = 1
    for i in range(10):
        if minNum + i * bucketSize not in numPuDistribution:
            numPuDistribution[minNum + i * bucketSize] = 0
    numPuDistribution = collections.OrderedDict(sorted(numPuDistribution.items()))
    
    numDoDistribution = {}
    for num in doDistribution:
        k = (num - minNum) / bucketSize
        if (minNum + k * bucketSize) in numDoDistribution:
            numDoDistribution[minNum + k * bucketSize] += 1
        else:
            numDoDistribution[minNum + k * bucketSize] = 1
    for i in range(10):
        if minNum + i * bucketSize not in numDoDistribution:
            numDoDistribution[minNum + i * bucketSize] = 0
    numDoDistribution = collections.OrderedDict(sorted(numDoDistribution.items()))
    
    dfPu = pd.DataFrame(data=numPuDistribution, index=range(1))
    dfDo = pd.DataFrame(data=numDoDistribution, index=range(1, 2))
    print dfPu
    print dfDo
    
    XPu = np.arange(len(numPuDistribution))
    XDo = np.arange(len(numDoDistribution))
    rect1 = plt.bar(XPu, numPuDistribution.values(), align='center', width=0.5, label='pick up')
    rect2 = plt.bar(XDo, numDoDistribution.values(), color='y', align='center', width=0.5, bottom=numPuDistribution.values(), label='drop off')
    autolabel(rect1, rect2)
    plt.xticks(XDo, numDoDistribution.keys())
    plt.xlabel("pickup and dropodd numbers")
    plt.ylabel("times")
    plt.title("Pickup and dropoff number distribution")
    plt.legend()
    # ymax = max(numPuDistribution.values()) + 1
    # pl.ylim(0, ymax)
    plt.savefig("a.png")


def autolabel(rect1, rect2):
    '''Add text label to every column in the bar plot''' 
    for i in range(len(rect1)):
        height1 = rect1[i].get_height()
        height2 = rect2[i].get_height()

        plt.text(rect2[i].get_x()+rect2[i].get_width()/4., 0.4 + (height1 + height2), '%d' %int(height1 + height2))


def getDataFromATimePeriod(region, startMonth, startDay, startHour, endMonth, endDay, endHour, data):
    """
    show the distribution of pickup data from a specific time period
    @para region:     The region which you want to see the distribution in.
          startMonth, startDay, startHour: The time period starts at the startMonth, startDay, startHour. For example, March, 3th, 3:00.
          endMonth, endDay, endHour: The time period ends at the endMonth, endDay, endHour. For example, March, 4th, 18:00.
          data: The day can be pick up data or drop off data.
                The format of the data is a nested dictionary: {region:{month:{day:{hour}}}}
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
    puData = readData("puWeekdayData.pkl")
    doData = readData("doWeekdayData.pkl")
    plotRegionDistribution(puData, doData, "Sunny Side", 2, 1)
    tripData = readData("puData.pkl")
    getDataFromATimePeriod("Chinatown", 2, 4, 5, 2, 9, 22, tripData)
