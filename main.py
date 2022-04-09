from consolemenu import SelectionMenu, ConsoleMenu
from consolemenu.items import *

from login import Login
from signup import Signup


def menu1():
    option1 = Login()
    option1.hi()
    if option1.succesfullLogIn == True:
        menu_list = ["Transfer Coins", "Check the Balance", "Explore the Chain", "Check the pool",
                     "Cancel a transaction", "Mine a Block", "Log out"]
        menu = SelectionMenu(menu_list, f'UserName: {option1.userName}', "Welcome to the goodChain Node")
        menu.show()
        menu.join()
        selection = menu.selected_option + 1

def menu2():
    pass


def menu3():
    menu = ConsoleMenu("Sign up", "SubMenu")
    sign = Signup()
    count = 0
    while count != 3:
        validation = sign.registerNewUser()
        if count == 3:
            exit()
        if not validation:
            count += 1
        if validation:
            mainmenu()



def menu4():
    exit()




def mainmenu():
    menu_list = ["login", "explore the blockchain", "Sign up"]
    menu = SelectionMenu(menu_list, "Public Menu", "Menu for sign up in Goodchain")
    menu.show()
    menu.join()

    selection = menu.selected_option + 1
    if selection == 1:
        menu1()
    elif selection == 2:
        menu2()
    elif selection == 3:
        menu3()
    elif selection == 4:
        menu4()

if __name__ == "__main__":
    mainmenu()