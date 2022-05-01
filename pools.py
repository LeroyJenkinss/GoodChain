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
        sqlStatement = '''select * from TRANSACTIONS where poolid = ? and realpool = 1'''
        values_to_insert = (idpool)
        cur.execute(sqlStatement, values_to_insert)
        listAllTrans = cur.fetchall()
        if listAllTrans == 10:
            self.setPool2Full(idpool)
            return self.getavailablePool()
        return

    def setPool2Full(self, poolid):
        try:
            cur.execute('''UPDATE pool set poolfull=:poolfull WHERE id=:id , {"poolfull": 1, "id": poolid}''')
            conn.commit()
        except Error as e:
            print(e)
        return

    def newUserPool(self):
            sqlstatement = '''select id from POOL where realpool = 0'''
            nullcheck = cur.execute(sqlstatement).fetchone()
            if nullcheck is None:

                sqlstatement = '''insert into POOL (poolfull, created, realpool) VALUES (?,?,?)'''
                values_to_insert = (False, datetime.now(), False)
                cur.execute(sqlstatement, values_to_insert)
                conn.commit()
