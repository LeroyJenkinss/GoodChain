from database import *


class Mining:

    def __init__(self):
        self.poolsString = ''

    pass

    # alle transaction uit een pool in een list

    def mine(self, minerId):
        self.checkAvailablePools()

    def checkAvailablePools(self):
        choicepool = True
        pools = cur.execute('''SELECT P.id from POOL as P LEFT JOIN block B on P.id = B.poolid WHERE  poolfull = 1 and realpool = 1
        EXCEPT
        SELECT P.id from block as B LEFT JOIN Pool P on P.id = B.poolid WHERE poolfull = 1 and realpool = 1''').fetchall()

        for a in range(0, len(pools)):
            if len(self.poolsString) == 0:
                self.poolsString += str(pools[a][0])
            else:
                self.poolsString += f', {str(pools[a][0])}'

        while choicepool:
            mineChoice = input(f'Which pool would you like to mine? {self.poolsString}')
            if len(mineChoice) <= 2 and self.poolsString.__contains__(mineChoice):
                choicepool = False
                self.checkTransactions(mineChoice)
            else:
                print('The given choice of pool was incorrect')

    def checkTransactions(self, poolId):
        try:
            transactionList = cur.execute("SELECT * FROM TRANSACTIONS WHERE poolid = (?)", [poolId]).fetchall()
            print(f'these are all transactions in the pool {transactionList}')
        except Error as e:
            print(e)

# mine functie aanroepen met poolid
# van die pool alle transactions checken
# loop door transactions en elke transactie naar verifyu classmethod
#
#
# falseTransactions = []
