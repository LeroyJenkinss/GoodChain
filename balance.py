from database import *


class Balance:

    def returnBalance(self, userid):
        userRecieved = cur.execute("SELECT SUM(txvalue) FROM TRANSACTIONS WHERE reciever = (?)", [userid]).fetchone()[0]
        userSpend = cur.execute("SELECT SUM(txvalue) FROM TRANSACTIONS WHERE sender = (?)", [userid]).fetchone()[0]
        # userSpendFee = cur.execute("SELECT SUM(txvalue) FROM TRANSACTIONS WHERE sender = (?)", [userid]).fetchone()[0]

        return str(userRecieved - userSpend)
