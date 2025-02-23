import pymysql
import pymysql.cursors
from tabulate import tabulate
from utils.update_data import *


def show_database_recyclebin(dict_config):
   """function untuk menampilkan Database Recycle Bin
    Args:
        dict_config (dict): dictionary configuration untuk login MySQL
    """
   try:
        conn = pymysql.connect(**dict_config) # ( ** ) = Unpacking nilai -> bisa memasukan jumlah custom parameter (*) = unpacking list/tuple, (**) -> Dict
        # print("Connection Success !")
        cursor = conn.cursor() # membuka gerbang akses mysql

        sql_query = """
                    SELECT 	c.phone_number,
                            p.*, 
                            c.contact_category,
                            c.notes,
                            s.facebook,
                            s.instagram,
                            s.twitter,
                            c.last_update
                        FROM l2_profil p
                        LEFT JOIN l2_contact c
                            ON p.email = c.email
                        LEFT JOIN l2_social_media s
                            ON c.phone_number = s.phone_number
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

def send_to_recycle_bin(dict_config, email, nomor_hp):
    """Function untuk mengirim data kontak ke recycle bin
    Args:
        dict_config (dict): dictionary configuration untuk login MySQL
        email (str): email contact yang ingin di soft delete
        nomor_hp (str): nomor hp contact yang ingin di soft delete
    """
    try: # L2 Profil
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    INSERT INTO l2_profil (email, full_name, nickname, gender, state, city, address)
                        SELECT email, full_name, nickname, gender, state, city, address FROM profil p
                        WHERE p.email LIKE %s
                    """ 
        cursor.execute(query=sql_query, args=email)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 

    try: # L2 Contact
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    INSERT INTO l2_contact (phone_number, email, contact_category, notes, last_update)
                        SELECT phone_number, email, contact_category, notes, NOW() FROM contact c
                        WHERE c.phone_number LIKE %s
                    """ 
        cursor.execute(query=sql_query, args=nomor_hp)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 
        
    try: # L2 Sosmed
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    INSERT INTO l2_social_media (phone_number, facebook, instagram, twitter)
                        SELECT phone_number, facebook, instagram, twitter FROM social_media s
                        WHERE s.phone_number LIKE %s
                    """ 
        cursor.execute(query=sql_query, args=nomor_hp)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 

def restore_recycle_bin(dict_config, email, nomor_hp):
    """Function untuk mengirim data dari recycle bin ke main data
    Args:
        dict_config (dict): dictionary configuration untuk login MySQL
        email (str): email contact yang ingin di restore
        nomor_hp (str): nomor hp contact yang ingin di restore
    """
    try: # Profil
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    INSERT INTO profil(email, full_name, nickname, gender, state, city, address)
                        SELECT email, full_name, nickname, gender, state, city, address FROM l2_profil p
                        WHERE p.email LIKE %s
                    """ 
        cursor.execute(query=sql_query, args=email)
        conn.commit()
    except Exception as e: 
        conn.rollback()
        print(f"msg: {e}") 

    try: # Contact
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    INSERT INTO contact(phone_number, email, contact_category, notes, last_update)
                        SELECT phone_number, email, contact_category, notes, NOW() FROM l2_contact c
                        WHERE c.phone_number LIKE %s
                    """ 
        cursor.execute(query=sql_query, args=nomor_hp)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 
        
    try: # Sosmed
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    INSERT INTO social_media(phone_number, facebook, instagram, twitter)
                        SELECT phone_number, facebook, instagram, twitter FROM l2_social_media s
                        WHERE s.phone_number LIKE %s
                    """ 
        cursor.execute(query=sql_query, args=nomor_hp)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 

def recycle_bin_menu(dict_config):
    """Function untuk akses recycle bin
    """
    option = None
    while option != "2":

        recycle_bin_storage = show_database_recyclebin(dict_config)
        print("")
        print("1. Restore Data")
        print("2. Kembali ke menu utama")
        option = input("Silahkan pilih menu : ")

        if option == "1":
            # 1. validasi input nomor hp
            while True:
                nomor_hp = input("Masukan nomor HP untuk mencari di recycle bin : ")
                if nomor_hp.isdigit() and (len(nomor_hp) == 12 or len(nomor_hp)== 13) :
                    break
                else:
                    print("Nomor HP tidak valid! (harus 12 atau 13 digit)")

            # 2. cari data nomor di recycle bin
            for i in range(0,len(recycle_bin_storage)):
                
                if recycle_bin_storage[i]["phone_number"] == nomor_hp:
                    filtered_database = [item for item in recycle_bin_storage if nomor_hp in item["phone_number"]]
                    print(tabulate(filtered_database, headers="keys", tablefmt="pipe"))
                    
                    # 3. option restore jika data ada di recycle bin
                    restore = None
                    while restore != "n":
                        restore = input(f"Ingin restore data {nomor_hp}? (y/n) :")

                        if restore == "y":
                            # restore
                            restore_recycle_bin(dict_config, recycle_bin_storage[i]["email"], nomor_hp)
                            # delete restored data on recycle bin
                            delete_permanen(dict_config, recycle_bin_storage[i]["email"], nomor_hp, False)
                            print("Data berhasil di restore!")
                            return
                        elif restore == "n":
                            pass
                        else:
                            print("Input tidak valid!")
                    break
            else:
                print("Nomor HP tidak ditemukan pada Recycle Bin")
            
        elif option == "2":
            return
        else:
            print("Input tidak valid!")

#________________________________________DELETE_____________________________________________________________

def delete_permanen(dict_config, email, nomor_hp, on_main:bool=False):
    """Function untuk delete permanen data pada tabel
    Args:
        dict_config (dict): dictionary configuration untuk login MySQL
        email (str): email contact yang ingin di soft delete
        nomor_hp (str): nomor hp contact yang ingin di soft delete
        on_main (bool, optional): True = Hapus data asli, False = Hapus data Recycle Bin. Defaults to False.
    """
    if on_main == False:
        try: # l2_Profil
            conn = pymysql.connect(**dict_config)
            cursor = conn.cursor()
            sql_query = """
                        DELETE FROM l2_profil
                        WHERE email = %s
                        """
            cursor.execute(query=sql_query, args=(email))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"msg: {e}")   
        try: # l2_contact
            conn = pymysql.connect(**dict_config)
            cursor = conn.cursor()
            sql_query = """
                        DELETE FROM l2_contact
                        WHERE phone_number = %s
                        """
            cursor.execute(query=sql_query, args=(nomor_hp))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"msg: {e}")   
        try: # l2_social_media
            conn = pymysql.connect(**dict_config)
            cursor = conn.cursor()
            sql_query = """
                        DELETE FROM l2_social_media
                        WHERE phone_number = %s
                        """
            cursor.execute(query=sql_query, args=(nomor_hp))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"msg: {e}")
    elif on_main == True:
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
            cursor.execute(query=sql_query, args=(nomor_hp))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"msg: {e}")   
        try: # social_media
            conn = pymysql.connect(**dict_config)
            cursor = conn.cursor()
            sql_query = """
                        DELETE FROM social_media
                        WHERE phone_number = %s
                        """
            cursor.execute(query=sql_query, args=(nomor_hp))
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"msg: {e}")


def soft_delete(dict_config):
    """Function untuk soft delete data dan mengirimnya ke database recycle bin
    """
    print("")

    database = get_database_info(dict_config)
    stop_loop = False # untuk control keluar nested loop
    while True:
            
        # validasi input nomor hp
        while True:
            nomor_hp = input("Masukan nomor HP untuk mencari data yang akan dihapus : ")
            if nomor_hp.isdigit() and (len(nomor_hp) == 12 or len(nomor_hp)== 13) :
                #print("aman")
                break
            else:
                print("Nomor HP tidak valid! (harus 12 atau 13 digit)")
        
        # 2nd loop untuk cari nomor hp
        for i in range(0,len(database)):

            if database[i]["phone_number"] == nomor_hp:
                dict_old_fil_database= show_filtered_database(nomor_hp,dict_config)
                dict_old_fil_database= dict_old_fil_database[0]

                while True:
                    del_option = input(f"Ingin menghapus data {nomor_hp}? (y/n) :")
                    if del_option.lower() == "y":

                        # menyimpan data yang terhapus ke recycle bin
                        send_to_recycle_bin(dict_config,dict_old_fil_database["email"],dict_old_fil_database["phone_number"] )

                        # delete database
                        delete_permanen(dict_config, database[i]["email"], nomor_hp, True)
                        print("Data sukses dihapus dan masuk recycle bin!")
                        return

                    elif del_option.lower() == "n":
                        print(f"Cancel Hapus data {nomor_hp}")
                        break

                stop_loop = True
                break
        else:
            print("Nomor HP tidak ditemukan!")
            # loop untuk cari lagi
            while True:
                cari_lagi = input("Ingin mencari lagi? (y/n) :")
                if cari_lagi.lower() == "y":
                    break
                elif cari_lagi.lower() == "n":
                    stop_loop=True
                    break

        if stop_loop:
            break