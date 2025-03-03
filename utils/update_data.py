import pymysql
import pymysql.cursors
from utils.data_utils import *
import datetime as dt
from tabulate import tabulate

def show_filtered_database(nomor:str,dict_config):
    """Menampilkan data dari satu nomor, nomor harus ada
    """
    database = get_database_info(dict_config)
    filtered_database = [item for item in database if nomor in item["phone_number"]]
    print("No Hp ditemukan : ")
    print(tabulate(filtered_database, headers="keys", tablefmt="pipe"))
    print("")
    return filtered_database
    

def update_profil(dict_config, tuple_value_8):
    try:
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    UPDATE profil p
                    SET 
                        p.email = %s,
                        p.full_name = %s,
                        p.nickname = %s,
                        p.gender = %s,
                        p.state = %s,
                        p.city = %s,
                        p.address = %s
                    WHERE p.email = %s
                    """ 
        cursor.execute(query=sql_query, args=tuple_value_8)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 

def update_contact(dict_config, tuple_value_5):
    try:
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    UPDATE contact c
                    SET 
                        c.email = %s,
                        c.facebook = %s,
                        c.instagram = %s,
                        c.twitter = %s
                    WHERE c.phone_number = %s
                    """ 
        cursor.execute(query=sql_query, args=tuple_value_5)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 

def update_category(dict_config, tuple_value_3):
    try:
        conn = pymysql.connect(**dict_config)
        cursor = conn.cursor()
        sql_query = """
                    UPDATE category c
                    SET 
                        c.category= %s,
                        c.notes= %s,
                        c.last_update= NOW()
                    WHERE phone_number = %s
                    """ 
        cursor.execute(query=sql_query, args=tuple_value_3)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"msg: {e}") 


def update_data(dict_config):
    """Function untuk merubah data pada database
    """
    print("")
    print("Silahkan lengkapi informasi untuk mengubah data!")
    print("")

    database = get_database_info(dict_config)

    stop_loop = False # untuk control keluar nested loop
    while True: # looping untuk cari nomor lagi

        # 1. validasi input nomor hp
        while True:
            nomor_hp = input("Masukan nomor HP data yang ingin diupdate: ")
            if nomor_hp.isdigit() and (len(nomor_hp) == 12 or len(nomor_hp)== 13) :
                #print("aman")
                break
            else:
                print("Nomor HP tidak valid!")
        
        # 2. cari data nomor hp
        for i in range(0,len(database)):

            if database[i]["phone_number"] == nomor_hp:
                # show_filtered_database(nomor_hp,dict_config)
                dict_old_fil_database = show_filtered_database(nomor_hp,dict_config)
                dict_old_fil_database = dict_old_fil_database[0]
                list_profil = [dict_old_fil_database["email"], dict_old_fil_database["full_name"], dict_old_fil_database["nickname"], 
                                dict_old_fil_database["gender"], dict_old_fil_database["state"], dict_old_fil_database["city"], 
                                dict_old_fil_database["address"],dict_old_fil_database["email"]]
                list_contact = [dict_old_fil_database["email"], dict_old_fil_database["contact_category"],
                                 dict_old_fil_database["notes"], dict_old_fil_database["phone_number"]]
                list_sosmed =  [dict_old_fil_database["facebook"], dict_old_fil_database["instagram"],
                                 dict_old_fil_database["twitter"],dict_old_fil_database["phone_number"]]

                print("1. Email")
                print("2. Nama Lengkap")
                print("3. Nickname")
                print("4. Jenis Kelamin")
                print("5. Provinsi")
                print("6. Kota")
                print("7. Alamat")
                print("8. Kategori Kontak")
                print("9. Catatan")
                print("10. Facebook")
                print("11. Instagram")
                print("12. Twitter")
                print("13. Cancel")
                # validasi input
                while True:
                    option = input("Silahkan pilih kolom yang ingin di update: ")
                    try:
                        option = int(option)
                        if option in range(1,14):
                            break
                        else:
                            print("Silahkan masukan angka 1-13")
                            continue
                    except:
                        print("Silahkan masukan angka 1-13")
                
                if option == 1:
                    while True:
                        email = input("Silahkan masukan email: ")
                        if email == "":
                            print("Email masih kosong")
                        else:
                            break
                    list_profil[0]=email
                    list_contact[0]=email

                elif option == 2:
                    while True:
                        nama = input("Silahkan masukan nama: ")
                        if nama == "" or nama[0].isdigit() :
                            print("Input tidak valid")
                        else:
                            break
                    list_profil[1] = nama

                elif option == 3:
                    nickname = input("Silahkan masukan nickname: ")
                    list_profil[2] = nickname

                elif option == 4:
                    while True:
                        print("1. Laki-laki")
                        print("2. Perempuan")
                        jenis_kelamin = input("Silahkan pilih kelamin :")
                        if jenis_kelamin.lower() == "1" or jenis_kelamin == "2":
                            if jenis_kelamin == "1":
                                jenis_kelamin = "Laki-laki"
                            elif jenis_kelamin == "2":
                                jenis_kelamin = "Perempuan"
                            #print("aman")
                            break
                        else:
                            print("Input tidak valid!")
                    list_profil[3] = jenis_kelamin

                elif option == 5:
                    while True:
                        provinsi = input("Silahkan masukan provinsi: ")
                        if provinsi == "":
                            print("provinsi masih kosong")
                        else:
                            break
                    list_profil[4] = provinsi

                elif option == 6:
                    while True:
                        kota = input("Silahkan masukan kota: ")
                        if kota == "":
                            print("kota masih kosong")
                        else:
                            break
                    list_profil[5] = kota

                elif option == 7:
                    alamat = input("Silahkan masukan alamat: ")
                    list_profil[6] = alamat

                elif option == 8:
                    while True:
                        print("Kategori Kontak :")
                        print("1. Keluarga")
                        print("2. Teman Kerja")
                        print("3. Teman Kuliah")
                        print("4. Teman SMA")
                        print("5. Teman SMP")
                        print("6. Teman SD")
                        print("7. Teman Main")
                        print("")
                        list_kategori = ["Keluarga","Teman Kerja","Teman Kuliah","Teman SMA","Teman SMP","Teman SD","Teman Main"]
                        kategori = input("Silahkan pilih kategori : ")
                        try:
                            kategori = int(kategori)
                            if kategori in range(1,8):
                                kategori = list_kategori[kategori-1]
                                break
                            else:
                                print("Silahkan masukan angka 1-7")
                                continue
                        except:
                            print("Silahkan masukan angka 1-7")
                    list_contact[1] = kategori

                elif option == 9:
                    catatan = input("Silahkan masukan catatan: ")
                    list_contact[2] = catatan

                elif option == 10:
                    Facebook = input("Silahkan masukan Facebook: ")
                    list_sosmed[0] = Facebook

                elif option == 11:
                    Instagram = input("Silahkan masukan Instagram: ")
                    list_sosmed[1] = Instagram

                elif option == 12:
                    Twitter = input("Silahkan masukan Twitter: ")
                    list_sosmed[2] = Twitter

                elif option == 13:
                    print("Update Data Canceled!")
                    return

                update_profil(dict_config, tuple(list_profil))
                update_contact(dict_config, tuple(list_contact))
                update_sosmed(dict_config, tuple(list_sosmed))
                print("Data Sukses diupdate")
                stop_loop = True
                break #exit loop cari nomor hp

        else:
            print("Nomor HP tidak ditemukan!")
            # 3. loop untuk cari lagi
            while True:
                cari_lagi = input("Ingin mencari lagi? (y/n) :")
                if cari_lagi.lower() == "y":
                    break
                elif cari_lagi.lower() == "n":
                    stop_loop=True
                    break
        
        if stop_loop:
            break