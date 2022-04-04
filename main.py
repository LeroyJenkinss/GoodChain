from consolemenu import SelectionMenu, ConsoleMenu
from consolemenu.items import *

from login import Login
from signup import Signup



if __name__ == "__main__":
    menu_list=["login", "explore the blockchain", "Sign up"]
    menu = SelectionMenu(menu_list,"Public Menu", "Menu for sign up in Goodchain")
    menu.show()
    menu.join()

    selection = menu.selected_option + 1



    if selection == 1:
        option1 = Login()
        option1.hi()
        if option1.succesfullLogIn == True:
            menu_list = ["Transfer Coins", "Check the Balance", "Explore the Chain", "Check the pool",
                         "Cancel a transaction", "Mine a Block", "Log out"]
            menu = SelectionMenu(menu_list, f'UserName: {option1.userName}', "Welcome to the goodChain Node")
            menu.show()
            menu.join()

            selection = menu.selected_option + 1

    elif selection == 2:
        pass

    elif selection == 3:
        menu = ConsoleMenu("Sign up", "SubMenu")



        sign = Signup()
        sign.registerNewUser()

    elif selection == 4:
        exit()



