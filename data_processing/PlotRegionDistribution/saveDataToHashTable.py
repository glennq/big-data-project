import pickle
import sys
import datetime
import time
import pandas as pd


def saveDataAndSaveDataStructureToFile(fileNameList):
    """Read all the pickup data and store them to file as a nested hashtable"""
    pickupData = dict()
    for fileName in fileNameList:
        try:
            f = open(fileName)
            for line in f:
                region, year, month, day, hour, week, count = line.split("\t")
                year, month, day, hour, week, count = map(int, [year, month, day, hour, week, count])
                if region in pickupData:
                    if month in pickupData[region]:
                        if day in pickupData[region][month]:
                            if hour in pickupData[region][month][day]:
                                pickupData[region][month][day][hour] += count
                            else:
                                pickupData[region][month][day][hour] = count
                        else:
                            pickupData[region][month][day] = dict()
                            pickupData[region][month][day][hour] = count
                    else:
                        pickupData[region][month] = dict()
                        pickupData[region][month][day] = dict()
                        pickupData[region][month][day][hour] = count
                else:
                    pickupData[region] = dict()
                    pickupData[region][month] = dict()
                    pickupData[region][month][day] = dict()
                    pickupData[region][month][day][hour] = count
        except Exception:
            print "Cannot open the file duce to the exception:", sys.exc_info()[0]
            raise
    try:
        pickupDataFile = open("doData.pkl", "wb")
        pickle.dump(pickupData, pickupDataFile)
        pickupDataFile.close()
    except Exception:
        print "Cannot save the pickup data into file due to the exception:", sys.exc_info()[0]
        raise


def savePickupWeekdayDataToFile(fileNameList):
    """Save pickup data according to the weekday """
    pickupWeekdayData = dict()
    for fileName in fileNameList:
        try:
            print "Dealing with file:", fileName
            f = open(fileName)
            for line in f:
                region, year, month, day, hour, week, count = line.split("\t")
                year, month, day, hour, week, count = map(int, [year, month, day, hour, week, count])
                weekNumber = datetime.datetime(year, month, day).strftime("%W")
                if region in pickupWeekdayData:
                    if week in pickupWeekdayData[region]:
                        if weekNumber in pickupWeekdayData[region][week]:
                            if hour in pickupWeekdayData[region][week][weekNumber]:
                                pickupWeekdayData[region][week][weekNumber][hour] += count
                            else:
                                pickupWeekdayData[region][week][weekNumber][hour] = count
                        else:
                            pickupWeekdayData[region][week][weekNumber] = dict()
                            pickupWeekdayData[region][week][weekNumber][hour] = count
                    else:
                        pickupWeekdayData[region][week] = dict()
                        pickupWeekdayData[region][week][weekNumber] = dict()
                        pickupWeekdayData[region][week][weekNumber][hour] = count
                else:
                    pickupWeekdayData[region] = dict()
                    pickupWeekdayData[region][week] = dict()
                    pickupWeekdayData[region][week][weekNumber] = dict()
                    pickupWeekdayData[region][week][weekNumber][hour] = count
        except Exception:
            print fileName
            print line
            print "Cannot open the file duce to the exception:", sys.exc_info()[0]
            # raise
    print "Done!"
    try:
        pickupDataFile = open("doWeekdayData.pkl", "wb")
        pickle.dump(pickupWeekdayData, pickupDataFile)
        pickupDataFile.close()
    except Exception:
        print "Cannot save the pickup data into file due to the exception:", sys.exc_info()[0]
        raise
    print pickupWeekdayData.keys()


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
    dateList = df["2013010100"].tolist()
    weatherList = df["Overcast"].tolist()
    weather["2013-01-01-00"] = "Overcast"
    for i in range(len(dateList)):
        year = str(dateList[i])[:4]
        month = str(dateList[i])[4:6]
        day = str(dateList[i])[6:8]
        hour = str(dateList[i])[8:]
        dateStr = year + "-" + month + "-" + day + "-" + hour
        weather[dateStr] = weatherList[i]
    
    try:
        weatherDataFile = open("weatherData.pkl", "wb")
        pickle.dump(weather, weatherDataFile)
        weatherDataFile.close()
    except Exception, e:
        print "Cannot save the weather data into file due ti the exception:", e
        raise e


if __name__ == "__main__":
    fileNameList = ["jan.txt", "feb.txt", "mar.txt", "apr.txt", "may.txt", "jun.txt", "jul.txt", "aug.txt", "sep.txt", "oct.txt", "nov.txt", "dec.txt"]
    saveDataAndSaveDataStructureToFile(fileNameList)
    savePickupWeekdayDataToFile(fileNameList)
    dealWithWeatherData(readWeatherData("cleaned_weather_data.csv"))
