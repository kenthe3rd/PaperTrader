import os
import requests
import datetime

#symbol: ticker symbol as string
#start: POSIX timestamp as float
def getHighLow(symbol, startArg):
    ### THIS IS STILL WIP###
    url = os.getenv('ALPACA_ENDPOINT')
    start = datetime.datetime.fromtimestamp(startArg, datetime.timezone.utc)
    end = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(minutes=15)
    paramsObj = {
        'start': start.isoformat("T").replace("+00:00", "") + "Z",
        'end':  end.isoformat("T").replace("+00:00", "") + "Z",
        'timeframe': '1Hour'
    }
    headersObj = {
        'APCA-API-KEY-ID': os.getenv('ALPACA_KEY_ID'),
        'APCA-API-SECRET-KEY': os.getenv('ALPACA_SECRET')
    }

    url += '/v2/stocks/' + symbol + '/bars'
    response = requests.get(url, headers=headersObj, params=paramsObj)
    print(response.content)