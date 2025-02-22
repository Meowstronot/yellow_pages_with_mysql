from utils.data_utils import *
from utils.add_data import *

# ------------------ Harus login ke MySQL terlebih dahulu
while True:
    host = input_not_null("Silahkan Masukan host MySQL :")
    user = input_not_null("Silahkan Masukan user MySQL :")
    password = input_not_null("Silahkan Masukan password MySQL :")
    # database = input_not_null("Silahkan Masukan database MySQL :")
    database = "yellow_pages"
    #Configuration
    dict_config = {
                "host": host,
                "user": user,
                "password": password,
                "database": database,
                "cursorclass": pymysql.cursors.DictCursor # merubah output result menjadi list of dictionary
                }
    try:
        connect_mysql(dict_config)
        break
    except:
        print("Connection to MySQL failed!")


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
        print("1. Tampilkan Data Kontak")
        print("2. Pencarian Data Kontak")
        print("3. Menambahkan Data Kontak")
        print("4. Update Data kontak")
        print("5. Hapus Data Kontak")
        print("6. Recycle Bin")
        print("7. Exit Program")
        print("")

        input_user = input("Silahkan pilih menu yang ingin dijalankan: ")

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
            show_database()
            update_data()
        elif input_user == "5":
            show_database()
            delete_data()
        elif input_user == "6":
            recycle_bin_menu()
        elif input_user == "7":
            print("")
            print("Good bye!")
            print("")
            
        else:
            print("Input is not valid !")

if __name__ == "__main__":
    main()