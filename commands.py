from scrapeUtils import getPrice
from mathHelp import isNum
commands = [
    "$buy-stock",
    "$sell-stock",
    "$stock-quote"
]

def isValidCommand(command):
    global commands
    print(commands)
    print(command)
    if command in commands:
        return True
    return False

async def executeCommand(command, message):
    content = str(message.content)
    if command == '$buy-stock':
        return True
    if command == '$sell-stock':
        return True
    if command == '$stock-quote':
        symbol = str(content[content.find(" ")+1:])
        price = getPrice(symbol)
        if isNum(price):
            await message.channel.send(symbol + " is currently trading at $" + price)
        else:
            await message.channel.send("Unable to fetch price for " + symbol)