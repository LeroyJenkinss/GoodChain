from consolemenu import SelectionMenu
from login import Login



if __name__ == "__main__":
    menu_list=["login", "explore the blockchain", "Sign up"]
    menu = SelectionMenu(menu_list,"Public Menu", "Menu for sign up in Goodchain")
    menu.show()
    menu.join()

    selection = menu.selected_option + 1

    print(f'this is the option {selection}')


    if selection == 1:
        option1 = Login()
        option1.hi()
        if option1.succesfullLogIn == True:
            menu_list = ["Transfer Coins", "Check the Balance", "Explore the Chain", "Check the pool",
                         "Cancel a transaction", "Mine a Block", "Log out"]
            menu = SelectionMenu(menu_list, f'UserName: {option1.userName}. {option1.lastName}', "Welcome to the goodChain Node")
            menu.show()
            menu.join()

            selection = menu.selected_option + 1

    elif selection == 2:
        pass

    elif selection == 3:
        pass

    elif selection == 4:
        exit()



