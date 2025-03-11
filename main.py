from utils.data_utils import *
from utils.add_data import *
from utils.update_data import *
from utils.delete_and_recycle_bin import *
from utils.mysql_login import *


def main():
    """Function for main program
    """
    print("""
░█──░█ ░█▀▀▀ ░█─── ░█─── ░█▀▀▀█ ░█──░█ 　 ░█▀▀█ ─█▀▀█ ░█▀▀█ ░█▀▀▀ ░█▀▀▀█ 　 █▀▀█ █▀▀█ █▀▀█ █▀▀▀ █▀▀█ █▀▀█ █▀▄▀█ 
░█▄▄▄█ ░█▀▀▀ ░█─── ░█─── ░█──░█ ░█░█░█ 　 ░█▄▄█ ░█▄▄█ ░█─▄▄ ░█▀▀▀ ─▀▀▀▄▄ 　 █──█ █▄▄▀ █──█ █─▀█ █▄▄▀ █▄▄█ █─▀─█ 
──░█── ░█▄▄▄ ░█▄▄█ ░█▄▄█ ░█▄▄▄█ ░█▄▀▄█ 　 ░█─── ░█─░█ ░█▄▄█ ░█▄▄▄ ░█▄▄▄█ 　 █▀▀▀ ▀─▀▀ ▀▀▀▀ ▀▀▀▀ ▀─▀▀ ▀──▀ ▀───▀""")
    print("")
    print("List Menu :")

    menu = ["Show Contact Data",
            "Find Contact",
            "Add Contact",
            "Update Contact Data",
            "Delete Contact Data",
            "Recycle Bin",
            "Reset info login",
            "Exit Program",]


    input_user = None
    while input_user != len(menu):
        print("")
        for i, val in enumerate(menu,1):
            print(f"{i}. {val}")
        input_user = input_choose_num(f"Please select the menu: ",min=1, max=i)

        if input_user == 1:
            show_database(dict_config)
        elif input_user == 2:
            show_database(dict_config)
            filter_database(dict_config)
        elif input_user == 3:
            show_database(dict_config)
            add_data(dict_config)
        elif input_user == 4:
            show_database(dict_config)
            update_data(dict_config)
        elif input_user == 5:
            show_database(dict_config)
            soft_delete(dict_config)
        elif input_user == 6:
            recycle_bin_menu(dict_config)
        elif input_user == 7:
            reset_login_info()
        elif input_user == 8:
            print("")
            print("Good bye!")
            print("")
        else:
            print("Input is not valid !")

if __name__ == "__main__":
    # create, read, and validate MySQL configuratioon before main program
    dict_config = mysql_configuration() 
    # print(dict_config)
    try:
        connect_mysql(dict_config)
        # break
    except:
        print("Connection to MySQL failed!")
        print("Please ensure that you have correctly entered your MySQL data and have run the 'yellow_pages_schema.sql'")
        print("Reset Connection!")
        reset_login_info()

    main()