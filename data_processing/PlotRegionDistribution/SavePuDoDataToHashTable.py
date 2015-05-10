import pickle
import sys
import datetime
import time
import pandas as pd


def savePuDoDataToFile(fileNameList):
    """Save pick-up data and drop-off data into file according to the weekday """
    data = dict()
    for fileName in fileNameList:
        try:
            print "Dealing with file:", fileName
            f = open(fileName)
            for line in f:
                region, year, month, day, hour, week, count = line.split("\t")
                year, month, day, hour, week, count = map(int, [year, month, day, hour, week, count])
                weekNumber = datetime.datetime(year, month, day).strftime("%W")
                if region in data:
                    if week in data[region]:
                        if weekNumber in data[region][week]:
                            if hour in data[region][week][weekNumber]:
                                data[region][week][weekNumber][hour] += count
                            else:
                                data[region][week][weekNumber][hour] = count
                        else:
                            data[region][week][weekNumber] = dict()
                            data[region][week][weekNumber][hour] = count
                    else:
                        data[region][week] = dict()
                        data[region][week][weekNumber] = dict()
                        data[region][week][weekNumber][hour] = count
                else:
                    data[region] = dict()
                    data[region][week] = dict()
                    data[region][week][weekNumber] = dict()
                    data[region][week][weekNumber][hour] = count
        except Exception:
            print "Cannot open the file duce to the exception:", sys.exc_info()[0]
    print "Done!"

    try:
        puDoDataFile = open("WeekdayData.pkl", "wb")
        pickle.dump(data, puDoDataFile)
        puDoDataFile.close()
    except Exception:
        print "Cannot save the pick-up and drop-off data into file due to the exception:", sys.exc_info()[0]
        raise


def saveDecLastWeekDataToFile(fileNameList):
    """Save 2013's last week's pickup and dropoff data into file according to the weekday """
    data = dict()
    for fileName in fileNameList:
        try:
            print "Dealing with file:", fileName
            f = open(fileName)
            fw = open("weatherLastWeek.pkl", "rb")
            weatherData = pickle.load(fw)
            fw.close()

            for line in f:
                line = line.rstrip("\n")
                # print line
                region, year, month, day, hour, week, count = line.split("\t")
                year, month, day, hour, week, count = map(int, [year, month, day, hour, week, count])
                if month != 12:
                    continue
                if day not in [23, 24, 25, 26, 27, 28, 29]:
                    continue
                date = "2013-12-" + str(day) + "-"
                if hour < 10:
                    date += "0" + str(hour)
                else:
                    date += str(hour)
                weather = weatherData[date]
                
                if region in data:
                    if week in data[region]:
                        if weather in data[region][week]:
                            if hour / 3 * 3 in data[region][week][weather]:
                                data[region][week][weather][hour / 3 * 3] += count
                            else:
                                data[region][week][weather][hour / 3 * 3] = count
                        else:
                            data[region][week][weather] = dict()
                            data[region][week][weather][hour / 3 * 3] = count
                    else:
                        data[region][week] = dict()
                        data[region][week][weather] = dict()
                        data[region][week][weather][hour / 3 * 3] = count
                else:
                    data[region] = dict()
                    data[region][week] = dict()
                    data[region][week][weather] = dict()
                    data[region][week][weather][hour / 3 * 3] = count
        except Exception:
            print "Cannot open the file duce to the exception:", sys.exc_info()[0]
    try:
        dataFile = open("decData.pkl", "wb")
        pickle.dump(data, dataFile)
        dataFile.close()
    except Exception:
        print "Cannot save the pickup data into file due to the exception:", sys.exc_info()[0]


def readWeatherData(fileName):
    """Read weather data from file"""
    try:
        f = pd.read_csv(fileName)
        return f
    except Exception, e:
        raise e


def dealWithWeatherData(df):
    """Use hashtable to store weather data"""
    weather = {}
    Normal = ["Overcast", "Partly Cloudy", "Mostly Cloudy", " Scattered Clouds", "Clear", "Unknown"]
    for i in range(3):
        if i == 2:
            print "========================dealing with 2013 weather data======================="
            dateList = df[2]["2013010100"].tolist()
            weatherList = df[2]["Overcast"].tolist()
            weather["2013-01-01-00"] = "Normal"
        elif i == 0:
            print "========================dealing with 2011 weather data======================="
            dateList = df[0]["2011010100"].tolist()
            weatherList = df[0]["Clear"].tolist()
            weather["2011-01-01-00"] = "Normal"
        else:
            print "========================dealing with 2012 weather data======================="
            dateList = df[1]["2012010100"].tolist()
            weatherList = df[1]["Clear"].tolist()
            weather["2012-01-01-00"] = "Normal"
        for i in range(len(dateList)):
            year = str(dateList[i])[:4]
            month = str(dateList[i])[4:6]
            day = str(dateList[i])[6:8]
            hour = str(dateList[i])[8:]
            dateStr = year + "-" + month + "-" + day + "-" + hour
            if weatherList[i] in Normal:
                weather[dateStr] = "Normal"
            else:
                weather[dateStr] = "Unnormal"
    try:
        weatherDataFile = open("weatherData.pkl", "wb")
        pickle.dump(weather, weatherDataFile)
        weatherDataFile.close()
    except Exception, e:
        print "Cannot save the weather data into file due ti the exception:", e


if __name__ == "__main__":
    fileNameList = []
    for m in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]:
        for i in range(1, 4):
            fileName = "data/do" + str(i) + m + ".txt"
            fileNameList.append(fileName)
            fileName = "data/pu" + str(i) + m + ".txt"
            fileNameList.append(fileName)
    savePuDoDataToFile(fileNameList) 
    dfList = []
    dfList.append(readWeatherData("cleaned_2011_weather.csv"))
    dfList.append(readWeatherData("cleaned_2012_weather.csv"))
    dfList.append(readWeatherData("cleaned_weather_data.csv"))
    dealWithWeatherData(dfList)
