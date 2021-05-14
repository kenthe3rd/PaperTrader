import datetime

def isNum(number):
    try:
        n = float(number)
        return True
    except:
        return False

def getHourAndMinuteFromString(timeString):
    idx = str(timeString).find(":")
    if idx == -1:
        return None
    hour = timeString[0:idx]
    minute = timeString[idx+1:]
    return {
        "hour": hour,
        "minute": minute
    }

def isDaylightSavingsTime():
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    month = now.month
    day = now.day
    date = now.date()
    if month == 12 or month < 3:
        return False
    if month == 3:
        weekdayFirstDayOfMonth = datetime.date(year=date.year, month=date.month, day=1).weekday()
        if day >= 14 - weekdayFirstDayOfMonth:
            return True
        else:
            return False
    if month == 11:
        weekdayFirstDayOfMonth = datetime.date(year=date.year, month=date.month, day=1).weekday()
        if day >= 7 - weekdayFirstDayOfMonth:
            return True
        else:
            return False

