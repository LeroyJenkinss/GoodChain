from database import *


class Block:

    def verifyBlocks(self, userId):
        outputString = ""
        try:
            availableBlockId = cur.execute(

                "select B.id  from Block B left outer join BLOCKVERIFY BV on B.id = BV.blockid where b.mineruserid != (?) and b.verifiedblock == false and b.mineruserid != (?) and (bv.validateUserId != (?) or bv.validateUserId is null);", [userId, userId, userId]).fetchall()
            txsList = self.getTxFeeBlock(availableBlockId)
            for a in availableBlockId:
                if outputString == '':
                    outputString += str(a[0])
                else:
                    outputString += ', ' + str(a[0])
            if len(outputString) != 0:
                print(f'The following id numbers are from block that can be verified by you: {outputString}')
                choice = input(f'Would you like to verify any of these blocks? (Y = yes N = no)')
                if choice == 'Y':
                    choiceloop = True
                    while choiceloop:
                        idchoice = input(f'Which block id would you like to verify?')
                        if outputString.__contains__(idchoice):
                            choiceloop = False



        except Error as e:
            print(e)

        return

    def getTxFeeBlock(self, blockIdList):
        txList = []
        for a in blockIdList:
            try:
                txValue = cur.execute("SELECT sum(txfee) FROM TRANSACTIONS WHERE poolid IS (SELECT poolid FROM BLOCK WHERE id == (?))", [a[0]]).fetchall()
                txList.append(txValue)
            except Error as e:
                print(e)
        return txList



