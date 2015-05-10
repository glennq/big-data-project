import pickle
import sys
import time
mport numpy as np
import collections
import pandas as pd
import datetime

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


def generateThreshold(data, weatherData, regions):
    """Generate anomaly threshold of every distribution according to specific week and hour"""
    threshold = dict()
    for region in regions:
        if region not in data:
            continue
        for week in range(1, 8):
            if week not in data[region]:
                continue
            total_data = data[region][week]
            for targetHour in [[i, i+1, i+2] for i in range(0, 22, 3)]:
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
                            d = "201" + str(i) + "-W" + weekNumber + "-" + str(week)
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
                        print sys.exc_info()[0]

                if NormalDistribution != []:
                    if region in threshold:
                        if week in threshold[region]:
                            if targetHour[0] in threshold[region][week]:
                                threshold[region][week][targetHour[0]]["Normal"] = sorted(NormalDistribution)[-len(NormalDistribution) / 20]
                            else:
                                threshold[region][week][targetHour[0]] = dict()
                                threshold[region][week][targetHour[0]]["Normal"] = sorted(NormalDistribution)[-len(NormalDistribution) / 20]
                        else:
                            threshold[region][week] = dict()
                            threshold[region][week][targetHour[0]] = dict()
                            threshold[region][week][targetHour[0]]["Normal"] = sorted(NormalDistribution)[-len(NormalDistribution) / 20]
                    else:
                        threshold[region] = dict()
                        threshold[region][week] = dict()
                        threshold[region][week][targetHour[0]] = dict()
                        threshold[region][week][targetHour[0]]["Normal"] = sorted(NormalDistribution)[-len(NormalDistribution) / 20]
                if UnnormalDistribution != []:
                    if region in threshold:
                        if week in threshold[region]:
                            if targetHour[0] in threshold[region][week]:
                                threshold[region][week][targetHour[0]]["Unnormal"] = sorted(UnnormalDistribution)[-len(UnnormalDistribution) / 20]
                            else:
                                threshold[region][week][targetHour[0]] = dict()
                                threshold[region][week][targetHour[0]]["Unnormal"] = sorted(UnnormalDistribution)[-len(UnnormalDistribution) / 20]
                        else:
                            threshold[region][week] = dict()
                            threshold[region][week][targetHour[0]] = dict()
                            threshold[region][week][targetHour[0]]["Unnormal"] = sorted(UnnormalDistribution)[-len(UnnormalDistribution) / 20]
                    else:
                        threshold[region] = dict()
                        threshold[region][week] = dict()
                        threshold[region][week][targetHour[0]] = dict()
                        threshold[region][week][targetHour[0]]["Unnormal"] = sorted(UnnormalDistribution)[-len(UnnormalDistribution) / 20]
    thresholdDataFile = open("threshold.pkl", "wb")
    pickle.dump(threshold, thresholdDataFile)
    thresholdDataFile.close()


if __name__ == "__main__":
    weatherData = readData("weatherData.pkl")
    data = readData("WeekdayData.pkl")
    regions = data.keys()
    plotRegionDistribution(data, weatherData, regions)
    getDataFromATimePeriod("Chinatown", 2, 4, 5, 2, 9, 22, tripData)
