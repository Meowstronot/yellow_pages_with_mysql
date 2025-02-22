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
            show_database()
            sort_nama()
        elif input_user == "2":
            show_database()
            filter_database()
        elif input_user == "3":
            show_database()
            add_data()
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