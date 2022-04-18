from consolemenu import SelectionMenu, ConsoleMenu
from consolemenu.items import FunctionItem, command_item, submenu_item
import database
from submenu import *

from login import Login
from signup import Signup


def menu1():
    loginUser = Login()
    count = 0

    while count != 3:
        login = loginUser.tryLogIn()
        if login:
            submenu1(loginUser)
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


def submenu1(loginUser):
    sub = Submenu(loginUser.id)
    print(loginUser.userName)

    menu = ConsoleMenu(f'UserName: {loginUser.userName}', "Welcome to the goodChain Node", exit_option_text="Log out")
    transferCoin = FunctionItem("Transfer Coins", sub.transferCoins, [loginUser.id])
    checkTheBalance = FunctionItem("Check the Balance", sub.checkTheBalance, [loginUser.id])
    exploreTheChain = FunctionItem("Explore the Chain", sub.exploreTheChain, [loginUser.id])
    checkThePool = FunctionItem("Check the pool", sub.checkThePool, [loginUser.id])
    cancelTransaction = FunctionItem("Cancel a transaction", sub.cancelTransaction, [loginUser.id])
    mineBlock = FunctionItem("Mine a Block", sub.mineBlock, [loginUser.id])
    menu.append_item(transferCoin)
    menu.append_item(checkTheBalance)
    menu.append_item(exploreTheChain)
    menu.append_item(checkThePool)
    menu.append_item(cancelTransaction)
    menu.append_item(mineBlock)
    menu.show()


if __name__ == "__main__":
    database.main()
    mainmenu()
