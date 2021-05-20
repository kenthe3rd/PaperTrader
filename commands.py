from scrapeUtils import getCryptoPrice, getPrice
from mathHelp import isNum
import classes.DatabaseManager as db

database = db.DatabaseManager()

commands = [
    "$buy-stock",
    "$sell-stock",
    "$stock-quote",
    "$buy-crypto",
    "$sell-crypto",
    "$crypto-quote",
    "$help",
    "$start-trading",
    "$leaderboard"
]

def isValidCommand(command):
    global commands
    if command in commands:
        return True
    return False

def getSymbolAndQuantityFromMessage(content):
    symbolIdx = content.find(" ")+1
    quantityIdx = content.find(" ",symbolIdx)+1
    symbol = str(content[symbolIdx:quantityIdx-1])
    quantity = float(content[quantityIdx:])
    return {
        "quantity" : quantity,
        "symbol" : symbol
    }

async def executeCommand(command, message):
    global database
    content = str(message.content)
    username = message.author.name + '#' + message.author.discriminator
    if command == '$buy-stock':
        if not database.investorExists(username):
            await message.channel.send("You need to ask at the Small-Loans desk for $100000 to start trading: $start-trading will get the ball rolling for you")
        else:
            args = getSymbolAndQuantityFromMessage(content)
            symbol = args['symbol']
            quantity = args['quantity']
            price = getPrice(symbol)
            cost = quantity * price
            money = database.getDollars(username)
            if money > cost:
                database.openPosition(database.getPortfolioID(database.getInvestorID(username), False), symbol, quantity)
                database.setDollars(username, money - cost)
                await message.channel.send("Purchasing " + str(quantity) + " of " + symbol + " at $" + str(price) + ". You now have $" + str(money-cost) + " on hand")
    if command == '$sell-stock':
        if not database.investorExists(username):
            await message.channel.send("You need to ask at the Small-Loans desk for $100000 to start trading: $start-trading will get the ball rolling for you")
        else:
            args = getSymbolAndQuantityFromMessage(content)
            symbol = args['symbol']
            quantity = args['quantity']
            if database.closePosition(database.getPortfolioID(database.getInvestorID(username), False), symbol, quantity):
                price = getPrice(symbol)
                money = database.getDollars(username)
                database.setDollars(username, money + (price * quantity))
                await message.channel.send("Sold " + str(quantity) + " of " + symbol + " at $" + str(price) + ". You now have $" + str( money + (price * quantity)) + " on hand")
            else:
                await message.channel.send("Insufficient quantity of " + symbol + " on hand.")
    if command == '$stock-quote':
        symbol = str(content[content.find(" ")+1:])
        price = getPrice(symbol)
        if isNum(price):
            await message.channel.send(symbol + " is currently trading at $" + str(price))
        else:
            await message.channel.send("Unable to fetch price for " + symbol)
    if command == '$buy-crypto':
        if not database.investorExists(username):
            await message.channel.send("You need to ask at the Small-Loans desk for $100000 to start trading: $start-trading will get the ball rolling for you")
        else:
            args = getSymbolAndQuantityFromMessage(content)
            symbol = args['symbol']
            quantity = args['quantity']
            price = getCryptoPrice(symbol)
            cost = quantity * price
            money = database.getDollars(username)
            if money > cost:
                database.openPosition(database.getPortfolioID(database.getInvestorID(username), True), symbol, quantity)
                database.setDollars(username, money - cost)
                await message.channel.send("Purchasing " + str(quantity) + " of " + symbol + " at $" + str(price) + ". You now have $" + str(money-cost) + " on hand")

    if command == '$sell-crypto':
        if not database.investorExists(username):
            await message.channel.send("You need to ask at the Small-Loans desk for $100000 to start trading: $start-trading will get the ball rolling for you")
        else:
            args = getSymbolAndQuantityFromMessage(content)
            symbol = args['symbol']
            quantity = args['quantity']
            if database.closePosition(database.getPortfolioID(database.getInvestorID(username), True), symbol, quantity):
                price = getCryptoPrice(symbol)
                money = database.getDollars(username)
                database.setDollars(username, money + (price * quantity))
                await message.channel.send("Sold " + str(quantity) + " of " + symbol + " at $" + str(price) + ". You now have $" + str( money + (price * quantity)) + " on hand")
            else:
                await message.channel.send("Insufficient quantity of " + symbol + " on hand.")
    if command == '$crypto-quote':
        symbol = str(content[content.find(" ")+1:])
        price = getCryptoPrice(symbol)
        if isNum(price):
            await message.channel.send(symbol + " is currently trading at $" + str(price))
        else:
            await message.channel.send("Unable to fetch price for " + symbol)
    if command == "$help":
        await message.channel.send("Go ask someone who cares. I'm busy counting my money.")
    if command == "$start-trading":
        if database.investorExists(username):
            await message.channel.send("You are already in the database " + message.author.name + ". Try $help if you need help figuring out what to do next")
        else:
            database.createInvestor(username)
            await message.channel.send("Congratulations " + message.author.name + ". You are now a PaperHands Trader! You have $100,000 to invest.")
    if command == "$leaderboard":
        leaderboard = ''
        dataArray = []
        for member in message.guild.members:
            memberUsername = member.name + "#" + member.discriminator
            if(database.investorExists(memberUsername)):
                data = {}
                investorID = database.getInvestorID(memberUsername)
                cryptoPortfolioID = database.getPortfolioID(investorID, True)
                stockPortfolioID = database.getPortfolioID(investorID, False)
                data['username'] = memberUsername
                data['dollars'] = database.getDollars(memberUsername)
                data['cryptoValue'] = database.getPortfolioValue(cryptoPortfolioID, True)
                data['stockValue'] = database.getPortfolioValue(stockPortfolioID, False)
                data['totalValue'] = data['dollars'] + data['cryptoValue'] + data['stockValue']
                dataArray.append(data)
        def getKeyForSorting(input):
            return input['totalValue']
        dataArray.sort(key=getKeyForSorting)
        for obj in dataArray:
            leaderboard += "\n" + obj['username'] + "\n\ttotal: " + str(obj['totalValue']) + "\n\tdollars: " + str(obj['dollars']) + "\n\tstocks: " + str(obj['stockValue']) + "\n\tcrypto: " + str(obj['cryptoValue']) + "\n"
        await message.channel.send("Leaderboard for " + message.guild.name + "\n" + leaderboard)