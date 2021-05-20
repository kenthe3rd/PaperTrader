import sqlite3
import os
from scrapeUtils import getCryptoPrice, getPrice
class DatabaseManager:

    def openPosition(self, portfolio, symbol, quantity):
        if self.getPosition(portfolio, symbol) == 0:
            query = "INSERT INTO positions (portfolio_id, symbol, quantity) VALUES (?,?,?);"
            params = [portfolio, symbol, quantity]
            self.executeQuery(query, params)
        else:
            query = "UPDATE positions SET quantity = quantity + ? WHERE portfolio_id = ? AND symbol = ?;"
            params = [quantity, portfolio, symbol]
            self.executeQuery(query,params)

    def closePosition(self, portfolio, symbol, quantity):
        quantityHeld =  self.getPosition(portfolio, symbol)
        if quantityHeld == quantity:
            query = "DELETE FROM positions WHERE portfolio_id = ? AND symbol = ?;"
            params = [portfolio, symbol]
            self.executeQuery(query, params)
            return True
        elif quantityHeld < quantity:
            return False
        else:
            quantityHeld -= quantity
            query = "UPDATE positions SET quantity = ? WHERE portfolio_id = ? AND symbol = ?;"
            params = [quantityHeld, portfolio, symbol]
            self.executeQuery(query, params)
            return True   

    def getPosition(self, portfolio, symbol):
        output = 0
        conn = self.getConnection()
        query = "SELECT quantity FROM positions WHERE portfolio_id = ? AND symbol = ?;"
        params = [portfolio, symbol]
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        if row != None:
            output = row[0]
        conn.close()
        return output

    def getPortfolioID(self, investorID, isCrypto):
        output = None
        conn = self.getConnection()
        query = "SELECT id FROM portfolios WHERE investor_id = ? AND is_crypto = ?;"
        params = [investorID, isCrypto]
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        if row != None:
            output = row[0]
        conn.close()
        return output

    def createPortfolios(self, username):
        query = "INSERT INTO portfolios (investor_id, is_crypto) VALUES (?,?);"
        id = self.getInvestorID(username)
        if id == None:
            return
        params = [id, True]
        self.executeQuery(query, params)
        params = [id, False]
        self.executeQuery(query, params)

    def createInvestor(self, username):
        query = "INSERT INTO investors (username, dollars) VALUES (?,100000);"
        params = [username]
        self.executeQuery(query, params)
        self.createPortfolios(username)

    def getInvestorID(self, username):
        output = None
        conn = self.getConnection()
        query = "SELECT id FROM investors WHERE username = ?;"
        params = [username]
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        if row != None:
            output = row[0]
        conn.close()
        return output

    def getDollars(self, username):
        output = None
        conn = self.getConnection()
        query = "SELECT dollars FROM investors WHERE username = ?;"
        params = [username]
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        if row != None:
            output = row[0]
        conn.close()
        return output

    def setDollars(self, username, dollars):
        query = "UPDATE investors SET dollars = ? WHERE username = ?;"
        params = [dollars, username]
        self.executeQuery(query, params)

    def investorExists(self, username):
        output = False
        conn = self.getConnection()
        cursor = conn.cursor()
        query = "SELECT id FROM investors WHERE username = ?;"
        params = [username]
        cursor.execute(query, params)
        row = cursor.fetchone()
        if row != None:
            output = True
        conn.close()
        return output

    def getConnection(self):
        return sqlite3.connect(database=os.getenv('PATH_TO_SQLITE_DB'))

    def executeQuery(self, query, params):
        conn = self.getConnection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    def getPortfolioValue(self, portfolioID, isCrypto):
        output = 0
        conn = self.getConnection()
        cursor = conn.cursor()
        query = "SELECT symbol, quantity FROM positions WHERE portfolio_id = ?;"
        params = [portfolioID]
        cursor.execute(query, params)
        rows = cursor.fetchall()
        if isCrypto:
            for row in rows:
                price = getCryptoPrice(row[0])
                output += price * row[1]
        else:
            for row in rows:
                price = getPrice(row[0])
                output += price * row[1]
        return output