
from database import *
from transactions import Transactions
from balance import Balance
from tools import verify


class Mining:

    def __init__(self):
        self.MinerId = None
        self.poolsString = ''

    pass

    # alle transaction uit een pool in een list

    def mine(self, minerId):
        self.MinerId = minerId
        poolId = self.checkAvailablePools()
        if poolId is not None:
            print(f'this is poolid {poolId}')
        else:
            return


    def checkAvailablePools(self):
        choicepool = True
        try:
            pools = cur.execute('''SELECT P.id from block as B LEFT JOIN Pool P on P.id = B.poolid WHERE  P.realpool = 1''').fetchall()
            for a in range(0, len(pools)):
                if len(self.poolsString) == 0:
                    self.poolsString += str(pools[a][0])
                else:
                    self.poolsString += f', {str(pools[a][0])}'

            while choicepool:
                if len(self.poolsString) == 0:
                    print('There are no pools avialable to mine')
                    return
                mineChoice = input(f'Which of the following pools would you like to mine? {self.poolsString}: ')
                if len(mineChoice) <= 2 and self.poolsString.__contains__(mineChoice):
                    choicepool = False

                    return self.fetchTransactions(mineChoice)
                else:
                    print('The given choice of pool was incorrect')
        except Error as e:
            print(e)

    def fetchTransactions(self, poolId):
        falseTransaction = []
        try:
            transactionList = cur.execute("SELECT * FROM TRANSACTIONS WHERE poolid = (?) and falsetransaction == true || falsetransaction is NULL", [poolId]).fetchall()
            print(f'this is the transList {transactionList}')
            for a in range(0, len(transactionList)):
                balance = self.checkTransactions(transactionList[a][0], transactionList[a][1], transactionList[a][3],
                                                 transactionList[a][9])
                if not balance:
                    Transactions().setFalseTransaction(transactionList[a][0])
                    falseTransaction.append(transactionList[a])
            if len(falseTransaction) < 5:
                return poolId
            else:
                print(f'This pool has more then 5 false transaction, which is too much')
                return

                # Hier moet gekeken worden naar de threshold voor aantal valse transacties

        except Error as e:
            print(e)
        if len(falseTransaction) != 0:
            print(f'these are the false transactions: {falseTransaction}')

    def checkTransactions(self, transactionId, senderId, txValue, transSig):
        valuesTransaction = False
        if Balance().calculateBalanceUntilTransaction(transactionId, self.MinerId):
            valuesTransaction = True
        if not Transactions().verifyTransAction(transactionId, senderId, txValue, transSig):
            valuesTransaction = False
        return valuesTransaction



