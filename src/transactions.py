import goodchain
from database import *
from pools import Pools
from datetime import datetime
from DbHashCheck import *
from tools import sign, verify
from clientService import ClientService


class Transactions:

    def __init__(self):
        self.Id = None
        self.amount = None

        self.sendToId = None
        self.transactionFee = None
        self.created = None

    def validTransaction(self, id, sendername):
        name = True
        while name:
            sqlStatement = 'SELECT id from USERS WHERE username=:sender'
            try:
                name = cur.execute(sqlStatement, {"sender": sendername}).fetchone()
                if name is not None:
                    self.sendToId = name[0]
                    name = False
                else:
                    return False
            except Error as e:
                print(e)
                return False
        self.Id = id
        return True

    def newTransaction(self):
        count = 0
        while count != 3:
            transferValue = input('Plz state the amount you would like to transfer, it must be a decimal number: ')
            self.amount = float(transferValue)
            if any(chr.isdigit() for chr in transferValue) and isinstance(float(transferValue), float) and float(
                    transferValue) > 0:
                self.createTransAction(float(transferValue))
                return
            elif transferValue[0:1] == '-' or transferValue == '0':
                self.amount = 0.0
                print(f'The requested amount is less then or is 0 coin')
                self.createTransAction(self.amount)
                return
            else:
                count += 1
                print(f'The amount is not a decimal number you can try {3 - count} try remaining')
        return

    def createTransAction(self, value):
        self.transactionFee = value * 0.05
        poolId = Pools().getavailablePool()[0]
        self.created = str(datetime.now())
        try:
            sqlstatement = '''insert into TRANSACTIONS (sender, reciever, txvalue, txfee, poolid, created) VALUES (?,?,?,?,?,?)'''
            values_to_insert = (
                self.Id, self.sendToId, self.amount, self.transactionFee, poolId, self.created)
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()
            transactionId = cur.execute("select Id from TRANSACTIONS where created = (?)", [self.created]).fetchone()[0]
            signedTransaction = self.signtransaction(transactionId)
            sqlstatement = '''update TRANSACTIONS  set transactionsig = (?) where id = (?)'''
            values_to_insert = (signedTransaction, transactionId)
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()
            HashCheck().writeHashtransaction()

            # Here I will extract the latest insert for the serverbroadcast
            latestTransAction = self.getLatestTransaction()
            result = ClientService().sendTransactions(latestTransAction)
            if not result:
                self.removeLatestTransaction()

            try:
                poolCount = cur.execute("select count(id) from transactions where poolid = (?)", [poolId]).fetchone()
            except Error as e:
                print(e)

            if poolCount[0] >= 10:
                print(f'this is the pool {poolId}')
                Pools().setPool2Full(poolId)

        except Error as e:
            print(e)

    def getLatestTransaction(self):
        try:
            latestInsert = cur.execute(
                "select sender, reciever, txvalue, txfee, poolid, created, modified, falsetransaction, transactionsig from  TRANSACTIONS where ID = (select max(ID) from TRANSACTIONS)").fetchone()
            latestInsertModified = (
            latestInsert[0], latestInsert[1], float(latestInsert[2]), float(latestInsert[3]), latestInsert[4],
            latestInsert[5], latestInsert[6], latestInsert[7], latestInsert[8])

            return latestInsertModified
        except Error as e:
            print(f'This is an error when getting lastest insert: {e}')

    def removeLatestTransaction(self):
        try:
            cur.execute("delete from  TRANSACTIONS where ID = (select max(ID) from TRANSACTIONS)")
            conn.commit()

        except Error as e:
            print(f'removeLatestTransaction didnt work : {e}')

    def newUserInsert(self, userName):
        try:
            userId = cur.execute("SELECT ID FROM USERS WHERE username = (?)", [userName]).fetchone()[0]
        except Error as e:
            print(e)

        try:
            sqlstatement = '''select id from POOL where realpool = False'''
            poolId = cur.execute(sqlstatement).fetchone()[0]
        except Error as e:
            print(e)

        try:
            sqlstatement = '''select id from users where username = "fake"'''
            fakeSenderId = cur.execute(sqlstatement).fetchone()[0]
        except Error as e:
            print(e)

        try:
            sqlstatement = '''insert into TRANSACTIONS (sender, reciever, txvalue, txfee, poolid, created) VALUES (?,?,?,?,?,?)'''
            values_to_insert = (fakeSenderId, userId, 50, 0, poolId, datetime.now())
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()

            latestTransAction = self.getLatestTransaction()
            result = ClientService().sendTransactions(latestTransAction)
            if not result:
                self.removeLatestTransaction()

            HashCheck().writeHashtransaction()



        except Error as e:
            print(e)

    def signtransaction(self, transactionId):
        try:

            privatesig = cur.execute("SELECT private_key FROM USERS WHERE id = (?)", [self.Id]).fetchone()[0]
            signdata = self.fetchSignData(transactionId)
            return sign(signdata, privatesig)

        except Error as e:
            print(e)

    def signtransaction2(self, transactionId, userid):
        try:
            privatesig = cur.execute("SELECT private_key FROM USERS WHERE id = (?)", [userid]).fetchone()[0]
            signdata = self.fetchSignData(transactionId)
            return sign(signdata, privatesig)

        except Error as e:
            print(e)

    def setFalseTransaction(self, transId):
        sql_statement = f'UPDATE transactions Set falsetransaction = 1 WHERE Id = {transId}'
        try:
            cur.execute(sql_statement)
            conn.commit()
            print(f'Transaction has been flagged as not correct')
        except Error as e:
            print(e)

    def setFalseTransactionToZero(self, userId):
        try:

            falseparlist = cur.execute(
                f'select id from transactions where sender = (?) and falsetransaction = 1 and txvalue != 0',
                [userId]).fetchall()
            if len(falseparlist) > 0:
                self.redirectCorrectTransactionsToPool(userId)
            cur.execute(f'UPDATE transactions set txvalue = 0, txfee = 0 where falsetransaction = 1 and sender = (?)',
                        [userId])
            conn.commit()

            if len(falseparlist) > 0:
                print(f'The following transactions have been set to zero, due to not being valid {falseparlist}')
            return

        except Error as e:
            print(e)

    def redirectCorrectTransactionsToPool(self, userId):
        try:
            redictPoolid = cur.execute(
                f'select poolid from transactions where sender = (?) and falsetransaction = 1 and txvalue != 0',
                [userId]).fetchone()
            print(f'this is redictPoolid  {redictPoolid}')

            if redictPoolid[0] is not None:
                validTransactions = cur.execute(
                    f'select id from transactions where poolid = (?) and txvalue != 0 and falsetransaction IS NULL',
                    [redictPoolid[0]]).fetchall()

                poolId = Pools().getavailablePool()[0]

                lenPool = cur.execute(
                    f'select count(id) from transactions where poolid = (?)',
                    [poolId]).fetchone()[0]

                if (10 - int(lenPool)) >= len(validTransactions):
                    for a in validTransactions:
                        cur.execute(
                            f'UPDATE transactions set poolid = (?) where id = (?)',
                            [poolId, a[0]])
                        conn.commit()

        except Error as e:
            print(e)

        return

    def fetchSignData(self, transactionId):
        data = cur.execute(
            f'select T.reciever , T.poolid, T.txfee, U.public_key, T.created from TRANSACTIONS T left join USERS U on T.sender = U.id where T.Id = (?) ',
            [transactionId]).fetchone()
        return data

    def verifyTransAction(self, transactionId, senderId, txvalue, signature):
        try:
            signedData = self.fetchSignData(transactionId)

            return verify(signedData, signature, signedData[3])
        except Error as e:
            print(e)

    def createTransAction2(self, fakeuser, recieverId, txValue, txFee, poolId, signature):
        try:
            sqlstatement = '''insert into TRANSACTIONS (sender, reciever, txvalue, txfee, poolid, created) VALUES (?,?,?,?,?,?)'''
            values_to_insert = (
                fakeuser, recieverId, txValue, txFee, poolId, datetime.now())
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()

            sqlstatement = '''select Id from TRANSACTIONS order by 1 desc limit 1'''
            transactionId = cur.execute(sqlstatement).fetchone()[0]
            signedTransaction = self.signtransaction2(transactionId, recieverId)

            sqlstatement = '''update TRANSACTIONS  set transactionsig = (?) where id = (?)'''
            values_to_insert = (signedTransaction, transactionId)
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()
            HashCheck().writeHashtransaction()

            latestTransAction = self.getLatestTransaction()
            result = ClientService().sendTransactions(latestTransAction)
            if not result:
                self.removeLatestTransaction()

        except Error as e:
            print(e)

    def cancelTransaction(self, userId):
        allUserTransactions = ''
        idstr = ''
        tryagain = True

        falseparlist = cur.execute(
            'select T.id, T.sender, T.reciever, T.txvalue from Transactions T left join Pool P on P.Id = T.PoolId left join (select * from Block B where B.pending = 0 and B.verifiedblock = 0  order by verifiedblock limit 1) as B on P.Id = B.PoolId where B.PoolId is not 0 and T.Sender = :userId and t.PoolId is not null',
            [userId]).fetchall()

        if len(falseparlist) > 0:
            for a in range(0, len(falseparlist)):
                idstr += f'{str(falseparlist[a][0])}'
                allUserTransactions += f'\nThe transaction Id = {str(falseparlist[a][0])}, '
                allUserTransactions += f' The id of the sender = {str(falseparlist[a][1])}'
                allUserTransactions += f' The id of the receiver = {str(falseparlist[a][2])}, '
                allUserTransactions += f' The Value send = {str(falseparlist[a][3])}'
        if len(falseparlist) != 0:
            while tryagain:
                transId = input(
                    f'{allUserTransactions}\nWhich of the above mentioned transactions id\'s would you like to cancel? :')
                if len(str(transId)) < 3 and idstr.__contains__(str(transId)):
                    tryagain = False
                    try:
                        cur.execute('delete from TRANSACTIONS where id = (?)', [transId])
                        conn.commit()
                        return
                    except Error as e:
                        print(e)
                else:
                    again = input(f'The Id you have chosen was incorrect would you like to try again? yes(Y) or no(N)')
                    if again == 'Y':
                        self.cancelTransaction(userId)
                    elif again == 'N':
                        return
                    else:
                        print(f'Your an idiot pls stop using this application')
                        return
        else:
            print('There are no transactions for you to cancel')
            return

    def GetPoolTransactionFees(self, poolId):
        # sql_statement = f'''SELECT count(TxFee) from Pool as P left join Transactions T on P.Id = T.PoolId WHERE P.Id = {poolId} and T.FalseTransaction = 0 and TxValue != 0'''
        try:
            value = cur.execute(
                "select sum(txfee) from TRANSACTIONS as T left join POOL as P on P.id = T.poolid where t.poolid = (?) and txvalue != 0",
                [poolId]).fetchone()
            if int(value[0]) == 0:
                value = '0'
                return value
        except Error as e:
            print(e)
            return False
        return str(format(value[0], ".2f"))

    def addTransAction(self, transaction):
        try:
            sqlstatement = '''insert into TRANSACTIONS ( sender, reciever, txvalue, txfee, poolid, created, modified, falsetransaction, transactionsig) VALUES (?,?,?,?,?,?,?,?,?)'''
            values_to_insert = (
                transaction[0], transaction[1], transaction[2], transaction[3], transaction[4], transaction[5],
                transaction[6], transaction[7], transaction[8])
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()
            return True


        except Error as e:
            print(e)
            return False
