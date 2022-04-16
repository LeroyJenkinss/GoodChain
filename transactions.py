import main
from database import *



class Transactions:

    def __init__(self):
        self.Id = None

    def newTransaction(self, id, senderName):
        sqlStatement = 'SELECT username from USERS WHERE username=:sender'
        senderIdCorrect = cur.execute(sqlStatement, {"sender": senderName})
        if len(senderIdCorrect.fetchall()) != 0:
            pass
        else:
            print('The user you want to transfer to doesn\'t exist ' )
            return False
        self.Id = id
        print('yes')
