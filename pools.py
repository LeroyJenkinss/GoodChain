from database import *
from datetime import datetime


class Pools:

    def __init__(self):
        self.Poolid = None

    def getavailablePool(self):
        try:
            sqlStatement = '''SELECT id from POOL WHERE poolfull = 0 and realpool = 1'''
            cur.execute(sqlStatement)
        except Error as e:
            print(e)
        poolid = cur.fetchone()
        if poolid == None:
            return self.makeNewPool()
        else:
            self.countPoolTransactions(poolid)
            self.Poolid = poolid
            return self.Poolid

    def makeNewPool(self):
        try:
            sqlStatement = '''insert into POOL (poolfull, created, realpool) VALUES (?,?,?)'''
            values_to_insert = (False, str(datetime.now()), True)
            cur.execute(sqlStatement, values_to_insert)
            conn.commit()

        except Error as e:
            print(e)
        return self.getavailablePool()

    def countPoolTransactions(self, idpool):
        sqlStatement = '''select * from TRANSACTIONS where poolid = ? and poolid != 1'''
        values_to_insert = (idpool)
        cur.execute(sqlStatement, values_to_insert)
        listAllTrans = cur.fetchall()
        if listAllTrans == 10:
            self.setPool2Full(idpool)
            return self.getavailablePool()
        return

    def setPool2Full(self, poolid):
        try:
            cur.execute("UPDATE pool set poolfull = 1 WHERE id = (?) ", [poolid])
            conn.commit()
        except Error as e:
            print(e)
        return

    def newUserPool(self):
        sqlstatement = '''select id from POOL where realpool = 0'''
        nullcheck = cur.execute(sqlstatement).fetchone()
        if nullcheck is None:
            sqlstatement = '''insert into POOL (poolfull, created, realpool, verified) VALUES (?,?,?,?)'''
            values_to_insert = (False, datetime.now(), False, False)
            cur.execute(sqlstatement, values_to_insert)
            conn.commit()

    def checkPool(self):
        global poolnum
        try:
            cur.execute(
                '''SELECT id from POOL where realpool = true''')
            toCheckTransId = cur.fetchall()
            for a in toCheckTransId:
                print(f'These are the Pool id numbers:{a[0]}')

            poolnum = input(
                f'We have {len(toCheckTransId)} pools pls typ in the id of the pool you would like to see: ')
        except Error as e:
            print(e)

        try:
            requestedPool = cur.execute("SELECT * FROM TRANSACTIONS WHERE poolid = (?)", [poolnum]).fetchall()
            if len(requestedPool) == 0:
                print(f'The pool with id {poolnum} is empty')
            self.showTransactionsOfPool(requestedPool)
        except Error as e:
            print(e)

    def showTransactionsOfPool(self, pool):
        senderList = []
        recieverList = []
        amounts = []
        for transaction in pool:
            for i in range(0, len(transaction)):
                if i == 1:
                    try:
                        senderName = \
                        cur.execute("SELECT username FROM USERS WHERE id = (?)", [transaction[i]]).fetchone()[0]
                        senderList.append(senderName)
                    except Error as e:
                        print(e)
                if i == 2:
                    try:
                        recieverName = \
                        cur.execute("SELECT username FROM USERS WHERE id = (?)", [transaction[i]]).fetchone()[0]
                        recieverList.append(recieverName)
                    except Error as e:
                        print(e)
                if i == 3:
                    amounts.append(transaction[i])

        for a in range(0, len(senderList)):
            print(
                f'Transaction {a + 1} in pool with ID {pool[0][5]}: Sender {senderList[a]} transferred {amounts[a]} to reciever {recieverList[a]}')
        return

    def GetPoolTransactions(self, poolId):
        print(f'this is poolid {poolId}')
        sql_statement = '''SELECT * from POOl as P left join TRANSACTIONS T on P.Id = T.PoolId WHERE P.Id = poolId'''
        try:
            cur.execute(sql_statement)
        except Error as e:
            print(e)
            return False
        return cur.fetchone()
