import pickle
import pandas as pd
import json
import sys


def readData(fileName):
    '''Read pickup data from a data structure file named fileName'''
    try:
        f = open(fileName, "rb")
        data = pickle.load(f)
        f = close()
    except Exception:
        print "Cannot open the data file due to the exception:", sys.exc_info()[0]
    return data


def dealWithDecLastWeekWeatherData(df):
    """docstring for dealWithWeatherData"""
    weather = {}
    Normal = ["Overcast", "partly Cloudly", "Mostly Cloudly", "Scattered Clouds", "Clear", "Unknown"]
    dateList = df["2013010100"].tolist()
    weatherList = df["Overcast"].tolist()
    for i in range(len(dateList)):
        year = str(dateList[i])[:4]
        month = str(dateList[i])[4:6]
        if month != "12":
            continue
        day = str(dateList[i])[6:8]
        if day not in ["23", "24", "25", "26", "27", "28", "29"]:
            continue
        hour = str(dateList[i])[8:]
        dateStr = year + "-" + month + "-" + day + "-" + hour
        if weatherList[i] in Normal:
            weather[dateStr] = "Normal"
        else:
            weather[dateStr] = "Unnormal"
    try:
        weatherDataFile = open("weatherLastWeek.pkl", "wb")
        pickle.dump(weather, weatherDataFile)
        weatherDataFile.close()
    except:
        pass


def detectAnomaly(data, threshold_data, weatherData, region):
    d = dict()
    w = dict()
    for region in threshold_data.keys():
        d[region] = dict()
        w[region] = dict()
        for week in range(1, 8):
            d[region][week] = dict()
            w[region][str(week)] = dict()
    for region in threshold_data.keys():
        for week in range(1, 8):
            for targetHour in [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23]]:
                weather = "Normal"
                for hour in targetHour:
                    date = "2013-12-"
                    if week == 1:
                        date += "23-"
                    elif week == 2:
                        date += "24-"
                    elif week == 3:
                        date += "25-"
                    elif week == 4:
                        date += "26-"
                    elif week == 5:
                        date += "27-"
                    elif week == 6:
                        date += "28-"
                    else:
                        date += "29-"
                    if hour < 10:
                        date += "0" + str(hour)
                    else:
                        date += str(hour)
                    if weatherData[date] == "Unnormal":
                        weather = "Unnormal"
                w[region][str(week)][str(targetHour[0]) + "_" + str(targetHour[-1])] = weather
    
                if region in data:
                    if week in data[region]:
                        if weather not in data[region][week]:
                            d[region][week][targetHour[0]] = "Normal"
                            continue
                        if targetHour[0] in data[region][week][weather]:
                            num = data[region][week][weather][targetHour[0]]
                        else:
                            num = -1
                    else:
                        num = -1
                else:
                    num = -1
                if weather == "Normal":
                    if region in threshold_data:
                        if week in threshold_data[region]:
                            if targetHour[0] in threshold_data[region][week]:
                                if "Normal" in threshold_data[region][week][targetHour[0]]:
                                    threshold = threshold_data[region][week][targetHour[0]]["Normal"]
                                else:
                                    threshold = 10000000
                            else:
                                threshold = 10000000
                        else:
                            threshold = 10000000
                    else:
                        threshold = 10000000
                    if num >= threshold:
                        d[region][week][targetHour[0]] = "Unnormal"
                    else:
                        d[region][week][targetHour[0]] = "Normal"
                else:
                    if region in threshold_data:
                        if week in threshold_data[region]:
                            if targetHour[0] in threshold_data[region][week]:
                                if "Unnormal" in threshold_data[region][week][targetHour[0]]:
                                    threshold = threshold_data[region][week][targetHour[0]]["Unnormal"]
                                else:
                                    threshold = 10000000
                            else:
                                threshold = 1000000
                        else:
                            threshold = 1000000
                    else:
                        threshold = 1000000
                    if num >= threshold:
                        d[region][week][targetHour[0]] = "Unnormal"
                    else:
                        d[region][week][targetHour[0]] = "Normal"
    f = open("anomaly.json", "wb")
    json.dump(w, f)
    f.close()
    
    f = open("anomalyData.pkl", "wb")
    pickle.dump(d, f)
    f.close()

if __name__ == '__main__':
    data = readData("decData.pkl")
    weatherdata = readData("weatherLastWeek.pkl")
    threshold_data = readData("threshold.pkl")
    regions = readData("WeekdayData.pkl").keys()
    detectAnomaly(data, threshold_data, weatherdata, regions)
    anomal = readData("anomalyData.pkl")
    column = []
    for i in range(1, 8):
        for j in range(0, 24, 3):
            column.append(str(i) + "_" + str(j) + "_" + str(j + 2))
    Data = []
    for region in anomal.keys():
        subData = []
        for week in range(1, 8):
            for hour in range(0, 24, 3):
                if anomal[region][week][hour] == "Normal":
                    subData.append(1)
                else:
                    subData.append(0)
        Data.append(subData)
    df = pd.DataFrame(data=Data, index=anomal.keys(), columns=column)
    df.index.name = "name"
    df.to_csv("anomaly.csv")
