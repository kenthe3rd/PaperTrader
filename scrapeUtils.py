import requests
import datetime
from mathHelp import getHourAndMinuteFromString, isDaylightSavingsTime
import cryptoSymbols
import time

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
    time.sleep(0.5)
    exchanges = [
        'NYSE',
        'NASDAQ',
        'NYSEARCA'
    ]
    for exchange in exchanges:
        url = 'https://google.com/finance/quote/' + symbol + ":" + exchange
        response = requests.get(url)
        data = str(response.content)
        if data.find("No results found") != -1:
            continue
        else:
            break   
    priceDivIdx = data.find('<div class="YMlKec fxKbKc">')
    substring = data[priceDivIdx+28:priceDivIdx+40]
    substring = substring[0:substring.find('<')]
    return float(substring)

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
    time.sleep(0.5)
    pathParam = str(symbol).lower()
    if symbol in cryptoSymbols.SYMBOL_TO_NAME:
        pathParam = cryptoSymbols.SYMBOL_TO_NAME[symbol].lower()
    url = 'https://coinmarketcap.com/currencies/' + pathParam + '/'
    response = requests.get(url)
    data = str(response.content)
    if data.find("Sorry, we couldn't find your page") != -1:
        return "Unable to find price for " + symbol
    priceDivIdx = data.find("priceValue___11gHJ")
    if priceDivIdx != -1:
        substring = data[priceDivIdx+21:priceDivIdx+40]
        substring = substring[0:substring.find('<')]
        substring = substring.replace(',','')
        return float(substring)
    return "Unable to find price for " + symbol

    