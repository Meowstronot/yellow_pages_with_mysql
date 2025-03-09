import pymysql
import pymysql.cursors
from tabulate import tabulate
from utils.update_data import *


def show_database_recyclebin(dict_config):
    """function to show Recycle Bin Database
    Args:
        dict_config (dict): dictionary configuration to login MySQL
    """
    try:
        conn = pymysql.connect(**dict_config) # ( ** ) = Unpacking nilai -> bisa memasukan jumlah custom parameter (*) = unpacking list/tuple, (**) -> Dict
        # print("Connection Success !")
        cursor = conn.cursor() # membuka gerbang akses mysql

        sql_query = """
                    SELECT * FROM recycle_bin;
                    """

        cursor.execute(query=sql_query)
        conn.commit() 
        # print("Commit Sucsess !")
        print("")
        print("Database Recycle Bin: ")
        hasil = cursor.fetchall()
        print(tabulate(hasil, headers="keys", tablefmt="pipe"))
        return hasil
    except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")
    finally: # code yang selalu dijalankan meskipun error atau tidak
        conn.close()

def get_database_recyclebin(dict_config):
    """function to get Recycle Bin Database
    Args:
        dict_config (dict): dictionary configuration to login MySQL
    """
    try:
        conn = pymysql.connect(**dict_config) # ( ** ) = Unpacking nilai -> bisa memasukan jumlah custom parameter (*) = unpacking list/tuple, (**) -> Dict
        # print("Connection Success !")
        cursor = conn.cursor() # membuka gerbang akses mysql

        sql_query = """
                    SELECT * FROM recycle_bin;
                    """

        cursor.execute(query=sql_query)
        conn.commit() 
        # print("Commit Sucsess !")
        hasil = cursor.fetchall()
        return hasil
    except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")
    finally: # code yang selalu dijalankan meskipun error atau tidak
        conn.close()

def send_to_recycle_bin(dict_config, phone_number):
    """Function to send contact data to the recycle bin.
    Args:
        dict_config (dict): Dictionary configuration for MySQL login.
        phone_number (str): Phone number of the contact to be soft deleted.
    """
    database = get_database_info(dict_config)
    df = pd.DataFrame(database)
    recycle_bin = get_database_recyclebin(dict_config)
    df_rtc = pd.DataFrame(recycle_bin)

    filtered_df = df[df["phone_number"]==phone_number]
    result_dict = filtered_df.to_dict(orient="records")[0]
    del result_dict["last_update"]
    # print(result_dict)
    last_id = df_rtc["id"].max()
    # print(last_id)
    result_tuple = tuple(result_dict.values())
    result_tuple = (last_id+1,) + result_tuple
    # print(result_tuple)

    try: # Recycle Bin
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    INSERT INTO recycle_bin(id, phone_number, email, full_name, nickname, gender, state, city, address, contact_category, notes, facebook, instagram, twitter, last_update)
                        VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW());
                    """ 
        cursor.execute(query=sql_query, args=result_tuple)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 


def restore_recycle_bin(dict_config, phone_number):
    """Function to restore contact data from the recycle bin to the main database.
    Args:
        dict_config (dict): Dictionary configuration for MySQL login.
        phone_number (str): Phone number of the contact to be restored.
    """
    recycle_bin = get_database_recyclebin(dict_config)
    df = pd.DataFrame(recycle_bin)
    filtered_df = df[df["phone_number"]==phone_number]
    result_dict = filtered_df.to_dict(orient="records")[0]

    try:
        conn = pymysql.connect(**dict_config)
        # print("Connection Success !")
        cursor = conn.cursor() 
        sql_query_profil = """
                    INSERT INTO profil(email, full_name, nickname, gender, state, city, address)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """
        cursor.execute(query=sql_query_profil, args=(result_dict["email"], result_dict["full_name"], result_dict["nickname"], result_dict["gender"], 
                                                    result_dict["state"], result_dict["city"], result_dict["address"]))
        sql_query_contact = """
                    INSERT INTO contact(phone_number, email, facebook, instagram, twitter)
                    VALUES (%s, %s, %s, %s, %s)
                    """
        cursor.execute(query=sql_query_contact, args=(result_dict["phone_number"], result_dict["email"], result_dict["facebook"], result_dict["instagram"], result_dict["twitter"]))
        sql_query_category = """
                    INSERT INTO category(phone_number, category, notes, last_update)
                    VALUES (%s, %s, %s, NOW())
                    """
        cursor.execute(query=sql_query_category, args=(result_dict["phone_number"], result_dict["contact_category"], result_dict["notes"]))

        conn.commit() 
        # return hasil
        # print("Contact successfully Restore!")
    except Exception as e:
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")
    finally:
        conn.close()


def recycle_bin_menu(dict_config):
    """Function to access recycle bin
    """
    recycle_bin_storage = show_database_recyclebin(dict_config)
    main_storage = get_database_info(dict_config)
    df_ryc = pd.DataFrame(recycle_bin_storage)
    df_main = pd.DataFrame(main_storage)
    print("")
    print("1. Restore Data")
    print("2. Back to main menu")
    option = input_choose_num("Please select option (1-2) : ",1,2)

    while True:
        if option == 1:
            # 1. validasi input id recycle bin
            while True:
                id = input_not_null("Please enter id recycle bin to restore: ")
                if id.isdigit():
                    id = int(id)
                    break
                else:
                    print("Input Invalid!")

            # 2. cari data id di recycle bin
            filtered_df_ryc = df_ryc[df_ryc["id"]==id]
            if filtered_df_ryc.empty:
                print("The id recycle bin you enter is not found!")
                
            else:
                print(tabulate(filtered_df_ryc, headers="keys", tablefmt="pipe"))
                filtered_df_main = df_main[df_main["phone_number"]==filtered_df_ryc["phone_number"].values[0]]

                if not filtered_df_main.empty: # jika data sudah ada di main
                    # option jika restore sudah ada di main
                    print("\nThe contact phone you want to restore already exist in main data:")
                    print(tabulate(filtered_df_main, headers="keys", tablefmt="pipe"))
                    print("1. Replace main data anyway")
                    print("2. Cancel Replace")
                    replace = input_choose_num("Please select option (1-2): ",1,2)
                    if replace == 1:
                        # send and delete main
                        soft_delete(dict_config, filtered_df_main["email"].values[0], filtered_df_main["phone_number"].values[0])
                        # restore and delete recycle bin
                        restore_recycle_bin(dict_config, filtered_df_ryc["phone_number"].values[0])
                        delete_permanen(dict_config, filtered_df_ryc["email"].values[0], filtered_df_ryc["phone_number"].values[0], id_ryc=id)
                        print("Contact successfully Restore!")
                        return
                    elif replace == 2:
                        return
                else: # jika data belum ada di main maka restore dan delete recycle bin
                    restore_recycle_bin(dict_config, filtered_df_ryc["phone_number"].values[0])
                    delete_permanen(dict_config, filtered_df_ryc["email"].values[0], filtered_df_ryc["phone_number"].values[0], id_ryc=filtered_df_ryc["id"].values[0])
                    print("Contact successfully Restore!")
                    return
        elif option == 2:
            return
        else:
            print("Input Invalid!")

#________________________________________DELETE_____________________________________________________________

def delete_permanen(dict_config, email, phone_number, id_ryc=None):
    """Function to permanently delete data from the table.
    Args:
        dict_config (dict): Dictionary configuration for MySQL login.
        email (str): Email of the contact to be deleted.
        phone_number (str): Phone number of the contact to be deleted.
        id_ryc (int): id recycle bin
        on_main (bool, optional): True = Delete original data, False = Delete data from Recycle Bin. Defaults to False.
    """

    if id_ryc != None: 
        try: # recycle_bin
            conn = pymysql.connect(**dict_config)
            cursor = conn.cursor()
            sql_query = """
                        DELETE FROM recycle_bin
                        WHERE id = %s
                        """
            cursor.execute(query=sql_query, args=(id_ryc))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"msg: {e}")   

    elif id_ryc == None:
        try: # Profil
            conn = pymysql.connect(**dict_config)
            cursor = conn.cursor()
            sql_query = """
                        DELETE FROM profil
                        WHERE email = %s
                        """
            cursor.execute(query=sql_query, args=(email))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"msg: {e}")   
        try: # contact
            conn = pymysql.connect(**dict_config)
            cursor = conn.cursor()
            sql_query = """
                        DELETE FROM contact
                        WHERE phone_number = %s
                        """
            cursor.execute(query=sql_query, args=(phone_number))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"msg: {e}")   
        try: # category
            conn = pymysql.connect(**dict_config)
            cursor = conn.cursor()
            sql_query = """
                        DELETE FROM category
                        WHERE phone_number = %s
                        """
            cursor.execute(query=sql_query, args=(phone_number))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"msg: {e}")


def soft_delete(dict_config, email=None, phone_number=None):
    """Function to soft delete data and move it to the recycle bin database.
    Args:
        dict_config (dict): Dictionary configuration for MySQL login.
        email (str): Email of the contact to be deleted. Defaults to None.
        phone_number (str): Phone number of the contact to be deleted. Defaults to None.
    """
    recycle_bin_storage = get_database_recyclebin(dict_config)
    main_storage = get_database_info(dict_config)
    df_ryc = pd.DataFrame(recycle_bin_storage)
    df_main = pd.DataFrame(main_storage)

    while True:
        if phone_number == None:
            while True:
                phone_number = input_not_null("Please enter phone number: ")
                if phone_number.isdigit() and (len(phone_number) == 12 or len(phone_number)== 13) :
                    break
                else:
                    print("Input Invalid!")

        filtered_df_main = df_main[df_main["phone_number"]==phone_number]

        if filtered_df_main.empty:
            print(f"The contact data of {phone_number} is not found!")
            break
        else:
            print(f"1. Soft delete {phone_number}")
            print("2. Cancel")
            del_option = input_choose_num("Please select option (1-2): ",1,2)
            if del_option == 1:
                send_to_recycle_bin(dict_config, phone_number)
                delete_permanen(dict_config, filtered_df_main["email"].values[0], phone_number)
                print('successfully soft delete!')
                return
            elif del_option == 2:
                print("Cancel soft delete!")
                return




    # print("")
    # stop_loop = False # untuk control keluar nested loop
    # while True:
            
    #     # validasi input nomor hp
    #     while True:
    #         nomor_hp = input("Masukan nomor HP untuk mencari data yang akan dihapus : ")
    #         if nomor_hp.isdigit() and (len(nomor_hp) == 12 or len(nomor_hp)== 13) :
    #             #print("aman")
    #             break
    #         else:
    #             print("Nomor HP tidak valid! (harus 12 atau 13 digit)")
        
    #     # 2nd loop untuk cari nomor hp
    #     for i in range(0,len(database)):

    #         if database[i]["phone_number"] == nomor_hp:
    #             dict_old_fil_database= show_filtered_database(nomor_hp,dict_config)
    #             dict_old_fil_database= dict_old_fil_database[0]

    #             while True:
    #                 del_option = input(f"Ingin menghapus data {nomor_hp}? (y/n) :")
    #                 if del_option.lower() == "y":

    #                     # menyimpan data yang terhapus ke recycle bin
    #                     send_to_recycle_bin(dict_config,dict_old_fil_database["email"],dict_old_fil_database["phone_number"] )

    #                     # delete database
    #                     delete_permanen(dict_config, database[i]["email"], nomor_hp, True)
    #                     print("Data sukses dihapus dan masuk recycle bin!")
    #                     return

    #                 elif del_option.lower() == "n":
    #                     print(f"Cancel Hapus data {nomor_hp}")
    #                     break

    #             stop_loop = True
    #             break
    #     else:
    #         print("Nomor HP tidak ditemukan!")
    #         # loop untuk cari lagi
    #         while True:
    #             cari_lagi = input("Ingin mencari lagi? (y/n) :")
    #             if cari_lagi.lower() == "y":
    #                 break
    #             elif cari_lagi.lower() == "n":
    #                 stop_loop=True
    #                 break

    #     if stop_loop:
    #         break