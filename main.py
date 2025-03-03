from utils.data_utils import *
from utils.add_data import *
from utils.update_data import *
from utils.delete_and_recycle_bin import *
from utils.mysql_login import *


def main():
    """Function for main program
    """
    input_user = None

    while input_user != "7":
        
        print("""
░█──░█ ░█▀▀▀ ░█─── ░█─── ░█▀▀▀█ ░█──░█ 　 ░█▀▀█ ─█▀▀█ ░█▀▀█ ░█▀▀▀ ░█▀▀▀█ 　 █▀▀█ █▀▀█ █▀▀█ █▀▀▀ █▀▀█ █▀▀█ █▀▄▀█ 
░█▄▄▄█ ░█▀▀▀ ░█─── ░█─── ░█──░█ ░█░█░█ 　 ░█▄▄█ ░█▄▄█ ░█─▄▄ ░█▀▀▀ ─▀▀▀▄▄ 　 █──█ █▄▄▀ █──█ █─▀█ █▄▄▀ █▄▄█ █─▀─█ 
──░█── ░█▄▄▄ ░█▄▄█ ░█▄▄█ ░█▄▄▄█ ░█▄▀▄█ 　 ░█─── ░█─░█ ░█▄▄█ ░█▄▄▄ ░█▄▄▄█ 　 █▀▀▀ ▀─▀▀ ▀▀▀▀ ▀▀▀▀ ▀─▀▀ ▀──▀ ▀───▀""")
        print("")
        print("List Menu :")
        print("1. Show Contact Data")
        print("2. Find Contact")
        print("3. Add Contact")
        print("4. Update Contact Data")
        print("5. Hapus Data Kontak")
        print("6. Recycle Bin")
        print("7. Exit Program")
        print("")

        input_user = input("Please select the menu: ")

        if input_user == "1":
            show_database(dict_config)
            # sort_nama()
        elif input_user == "2":
            show_database(dict_config)
            filter_database(dict_config)
        elif input_user == "3":
            show_database(dict_config)
            add_data(dict_config)
        elif input_user == "4":
            show_database(dict_config)
            update_data(dict_config)
        elif input_user == "5":
            show_database(dict_config)
            soft_delete(dict_config)
        elif input_user == "6":
            recycle_bin_menu(dict_config)
        elif input_user == "7":
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