from database import *


class Balance:

    def calculateBalanceUntilTransaction(self, transId, minerId):
        try:
            receivedValues = cur.execute(
                "select sum(txvalue) from TRANSACTIONS T LEFT OUTER JOIN BLOCK B on T.poolid = B.poolid where (B.verifiedblock = 1 or T.poolid = 1) and T.reciever = (?) and T.Id < (?)",
                [minerId, transId]).fetchone()[0]
            if receivedValues is None:
                receivedValues = 0
            sendValues = cur.execute("SELECT sum(txvalue) FROM TRANSACTIONS WHERE sender = (?) and id < (?)",
                                     [minerId, transId]).fetchone()[0]
            if sendValues is None:
                sendValues = 0
            transValue = cur.execute("SELECT txvalue FROM TRANSACTIONS WHERE sender = (?) and id = (?)",
                                     [minerId, transId]).fetchone()[0]
            if transValue is None:
                transValue = 0
            if receivedValues - sendValues - transValue >= 0:
                print(f'these are the values {receivedValues} - {sendValues} - {transValue} = {receivedValues - sendValues - transValue}')
                return True
            return False
        except Error as e:
            print(e)

    def returnBalance(self, userid):
        userRecieved = cur.execute("SELECT SUM(txvalue) FROM TRANSACTIONS WHERE reciever = (?)", [userid]).fetchone()[0]
        userSpend = cur.execute("SELECT SUM(txvalue) FROM TRANSACTIONS WHERE sender = (?)", [userid]).fetchone()[0]
        # userSpendFee = cur.execute("SELECT SUM(txvalue) FROM TRANSACTIONS WHERE sender = (?)", [userid]).fetchone()[0]
        return str(userRecieved - userSpend)
