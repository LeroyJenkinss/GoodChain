from consolemenu import SelectionMenu, ConsoleMenu
from consolemenu.items import FunctionItem, command_item, submenu_item
import database
from submenu import *

from login import Login
from signup import Signup


def menu1():
    option1 = Login()
    count = 0

    while count != 3:
        login = option1.tryLogIn()
        if login:
            submenu1()
        if count == 3:
            exit()
        if not login:
            count += 1
            if count < 3:
                print('Your login attempt was incorrect')
            else:
                print('We will now close the connetion')


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
            if count < 3:
                print('Your entry was not unique')
            else:
                print('We will now close the connection')
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


def submenu1():
    option1 = Login()
    sub = Submenu(option1.id)

    menu = ConsoleMenu(f'UserName: {option1.userName}', "Welcome to the goodChain Node", exit_option_text="Log out")
    transferCoin = FunctionItem("Transfer Coins", sub.transferCoins)
    checkTheBalance = FunctionItem("Check the Balance", sub.checkTheBalance)
    menu.append_item(transferCoin)
    menu.append_item(checkTheBalance)

    menu.show()
    # menu_list = ["Transfer Coins", "Check the Balance", "Explore the Chain", "Check the pool",
    #              "Cancel a transaction", "Mine a Block", "Log out"]
    # menu = SelectionMenu(menu_list, f'UserName: {option1.userName}', "Welcome to the goodChain Node")
    # menu.show()
    # menu.join()
    # selection = menu.selected_option + 1
    #
    # sub.mainSubMenu(selection, option1.userName)
    # while selection != 7 or selection != 8:
    #     main.submenu1()
    # when passing parameters
    # checkTheBalance = FunctionItem("Check the Balance", sub.checkTheBalance, [id])


if __name__ == "__main__":
    database.main()
    mainmenu()
