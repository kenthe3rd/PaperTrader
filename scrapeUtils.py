import requests
import datetime
from mathHelp import getHourAndMinuteFromString, isDaylightSavingsTime

exchangeOpenClose = {
    "NYSE" : {
        "open": "14:30",
        "close": "21:00",
        "dst": True
    },
    "NASDAQ" : {
        "open": "14:30",
        "close": "21:00",
        "dst": True
    },
    "NYSEARCA" : {
        "open" : "14:30",
        "close" : "21:00",
        "dst": True
    }
}

def getPrice(symbol):
    exchanges = [
        'NYSE',
        'NASDAQ',
        'NYSEARCA'
    ]
    for exchange in exchanges:
        url = 'https://google.com/finance/quote/' + symbol + ":" + exchange
        print(url)
        response = requests.get(url)
        data = str(response.content)
        if data.find("No results found") != -1:
            continue
        else:
            break
    if data.find("No results found") != -1:
        return getCryptoPrice(symbol)
    else:    
        priceDivIdx = data.find('<div class="YMlKec fxKbKc">')
        substring = data[priceDivIdx+28:priceDivIdx+40]
        substring = substring[0:substring.find('<')]
        return substring

def exchangeIsOpen(exchange):
    global exchangeOpenClose
    exchangeInfo = exchangeOpenClose[exchange]
    timeAdj = 0
    if exchangeInfo['dst'] == True and isDaylightSavingsTime() == True:
        timeAdj = -1
    if None == exchangeInfo:
        print("I can't find exchange:" + exchange)
    else:
        current = datetime.datetime.now(tz=datetime.timezone.utc)
        openInfo = getHourAndMinuteFromString(exchangeInfo['open'])
        closeInfo = getHourAndMinuteFromString(exchangeInfo['close'])
        if current.time() < datetime.time(hour=int(openInfo['hour'])+timeAdj, minute=int(openInfo['minute'])) or current.time() > datetime.time(hour=int(closeInfo['hour'])+timeAdj, minute=int(closeInfo['minute'])):
            return False
        return True


def getCryptoPrice(symbol):
    return "Unable to find price"

    