from database import *
from datetime import datetime
from clientService import ClientService


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

            # New pool broadcast
            latestPool = self.getLatestPool()
            result = ClientService().sendPool(latestPool)
            if not result:
                self.removeLatestPool(latestPool[4])

        except Error as e:
            print(e)
        return self.getavailablePool()

    def getLatestPool(self):
        try:
            latestInsert = cur.execute("select  poolfull, realpool, verified, created, id from  POOL where ID = (select max(ID) from USERS)").fetchone()
            latestPool = (latestInsert[0], latestInsert[1], latestInsert[2], latestInsert[3], latestInsert[4])

            return latestPool
        except Error as e:
            print(f'This is an error when getting lastest pool insert: {e}')

    def removeLatestPool(self, poolId):
        try:
            cur.execute("delete from  POOL where ID = (?)", [poolId])
            conn.commit()

        except Error as e:
            print(f'removeLatestPool didnt work : {e}')



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

            # New pool broadcast
            latestUpdatedPool = self.getLatestPool()
            result = ClientService().sendUpdatedFullPool(latestUpdatedPool)
            if not result:
                self.removeUpdateFullLatestPool(poolid)
        except Error as e:
            print(e)
        return

    def removeUpdateFullLatestPool(self, poolid):
        try:
            cur.execute("UPDATE pool set poolfull = 0 WHERE id = (?) ", [poolid])
            conn.commit()
            
        except Error as e:
            print(e)
        return

    def UpdatefullPool(self, poolid):
        try:
            cur.execute("UPDATE pool set poolfull = 1 WHERE id = (?) ", [poolid])
            conn.commit()
            return True
        except Error as e:
            print(e)
            return False


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
                print(f'These are the Pool id numbers: {a[0]}')
            if len(toCheckTransId) == 0:
                print(f'There are no pools available for you to check')
                return
            else:
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
        return

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
                f'Transaction {a + 1} in pool with ID {pool[0][5]}: Sender {senderList[a]} transferred {amounts[a]} coin to reciever {recieverList[a]}')
        return

    def GetPoolTransactions(self, poolId):
        try:
            cur.execute('''SELECT T.* from Transactions as T left join Pool P on P.Id = T.PoolId WHERE T.poolid = (?) and (t.falsetransaction = 0 or t.falsetransaction is null) and t.txvalue != 0''', [poolId])
        except Error as e:
            print(e)
            return False
        return cur.fetchall()

    def CreateNewPool(self, poolData):
        sql_statement = '''INSERT INTO Pool (poolfull, realpool ,verified, created) VALUES(?,?,?,?)'''
        values_to_insert = (poolData[0], poolData[1], poolData[2], poolData[3])
        try:
            cur.execute(sql_statement, values_to_insert)
            conn.commit()
            print('Pool has been added.')
            return True

        except Error as e:
            print(e)
            return False
