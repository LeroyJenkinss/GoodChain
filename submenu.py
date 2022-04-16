from database import *
import main


class Submenu:

    def __init__(self):
        selection = None

    def mainSubMenu(self, selection):
        self.selection = selection
        if selection == 1:
            self.transferCoins()
        if selection == 2:
            self.checkTheBlalance()
        if self.selection == 3:
            self.exploreTheChain()
        if self.selection == 4:
            self.checkThePool()
        if self.selection == 5:
            self.cancelTransaction()
        if self.selection == 6:
            self.mineBlock()
        if self.selection == 7:
            main.menu4()
        if self.selection == 8:
            main.mainmenu()

    def transferCoins(self):
        pass

    def checkTheBlalance(self):
        pass

    def exploreTheChain(self):
        pass

    def checkThePool(self):
        pass

    def cancelTransaction(self):
        pass

    def mineBlock(self):
        pass
