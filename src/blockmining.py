from tools import verify
from transactions import Transactions
from balance import Balance
from database import *


class Blockmining:

    def fetchTransactions2(self, poolId):
        falseTransaction = []
        try:
            transactionList = cur.execute(
                "SELECT * FROM TRANSACTIONS WHERE poolid = (?) and falsetransaction == true || falsetransaction is NULL",
                [poolId]).fetchall()
            for a in range(0, len(transactionList)):
                balance = self.checkTransactions(transactionList[a][0], transactionList[a][1], transactionList[a][3],
                                                 transactionList[a][9])
                if not balance:
                    Transactions().setFalseTransaction(transactionList[a][0])
                    falseTransaction.append(transactionList[a])
        except Error as e:
            print(e)
        if len(falseTransaction) != 0:
            return False
        return True

    def checkTransactions(self, transactionId, senderId, txValue, transSig):
        valuesTransaction = False
        if self.calculateBalanceUntilTransaction(transactionId, senderId):
            valuesTransaction = True
        if not self.verifyTransAction(transactionId, senderId, txValue, transSig):
            valuesTransaction = False
        return valuesTransaction

    def calculateBalanceUntilTransaction(self, transId, minerId):
        try:
            receivedValues = cur.execute(
                "select sum(txvalue) from TRANSACTIONS T LEFT OUTER JOIN BLOCK B on T.poolid = B.poolid where (B.verifiedblock = 1 or T.poolid = 1) and T.reciever = (?) and T.Id < (?)",
                [minerId, transId]).fetchone()
            if receivedValues[0] is None:
                receivedValues = 0

            sendValues = cur.execute("SELECT sum(txvalue) FROM TRANSACTIONS WHERE sender = (?) and id < (?)",
                                     [minerId, transId]).fetchone()
            if sendValues[0] is None:
                sendValues = 0
            else:
                sendValues = sendValues[0]

            transValue = cur.execute("SELECT txvalue FROM TRANSACTIONS WHERE sender = (?) and id = (?)",
                                     [minerId, transId]).fetchone()
            if transValue is None:
                transValue = 0
            else:
                transValue = int(transValue[0])

            if receivedValues[0] - sendValues - transValue >= 0:
                return True
            return False
        except Error as e:
            print(e)

    def returnBalance(self, userid):
        userRecieved = cur.execute("SELECT SUM(txvalue) FROM TRANSACTIONS WHERE reciever = (?)", [userid]).fetchone()[0]
        userSpend = cur.execute("SELECT SUM(txvalue) FROM TRANSACTIONS WHERE sender = (?)", [userid]).fetchone()[0]
        # userSpendFee = cur.execute("SELECT SUM(txvalue) FROM TRANSACTIONS WHERE sender = (?)", [userid]).fetchone()[0]
        return str(userRecieved - userSpend)

    def fetchSignData(self,transactionId):
        data = cur.execute(f'select T.reciever , T.poolid, T.txfee, U.public_key, T.created from TRANSACTIONS T left join USERS U on T.sender = U.id where T.Id = (?) ', [transactionId]).fetchone()
        return data

    def verifyTransAction(self, transactionId, senderId, txvalue, signature):
        try:
            signedData = self.fetchSignData(transactionId)
            data = cur.execute(
                f'select transactionsig from TRANSACTIONS where Id = (?) ',
                [transactionId]).fetchone()

            return verify(signedData, data[0], signedData[3])
        except Error as e:
            print(e)


