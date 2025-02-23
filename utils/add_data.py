import pymysql
import pymysql.cursors
from utils.data_utils import *
from utils.update_data import *
import datetime as dt
from tabulate import tabulate

def add_data(dict_config):
    """
    Function untuk add data baru ke database
    Jika data sudah ada maka bisa di update dengan yang baru
    """
    print("")
    print("Silahkan isi Data Kontak untuk dimasukan kedalam Database: ")
    print("")


    while True:
        nomor_hp = input("Silahkan masukan nomor HP: ")
        if nomor_hp.isdigit() and (len(nomor_hp) == 12 or len(nomor_hp)== 13) :
            #print("aman")
            break
        else:
            print("Nomor HP tidak valid!")

    while True:
        email = input("Silahkan masukan email: ")
        if email == "":
            print("Email masih kosong")
        else:
            break
    
    while True:
        nama = input("Silahkan masukan nama: ")
        if nama == "" or nama[0].isdigit() :
            print("Input tidak valid")
        else:
            break

    nickname = input("Tambahkan nickname pada kontak (optional): ")
            
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
    
    while True:
        provinsi = input("Silahkan masukan provinsi: ")
        if provinsi == "":
            print("Provinsi masih kosong")
        else:
            break

    while True:
        kota = input("Silahkan masukan kota: ")
        if kota == "":
            print("Kota masih kosong")
        else:
            break

    alamat = input("Silahkan masukan alamat lengkap (optional): ")

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

    catatan = input("Tambahkan catatan pada kontak(optional): ")
    facebook = input("Tambahkan facebook pada kontak(optional): ")
    instagram = input("Tambahkan instagram pada kontak(optional): ")
    twitter = input("Tambahkan twitter pada kontak(optional): ")

    last_update = dt.datetime.now()

    inputed_data = [{"phone_number": nomor_hp,
                    "email": email,
                    "full_name": nama,
                    "nickname": nickname,
                    "gender": jenis_kelamin,
                    "state":provinsi,
                    "city": kota,
                    "address":alamat,
                    "contact_category":kategori,
                    "notes":catatan,
                    "facebook":facebook,
                    "instagram":instagram,
                    "twitter":twitter,
                    "last_update": last_update.strftime("%Y-%m-%d %H:%M:%S")}]
    print(tabulate(inputed_data, headers="keys", tablefmt="pipe"))

    ask_add = None
    while True:
        ask_add = input("Apakah ingin menyimpannya ke database? (y/n) :")
        if ask_add.lower() == "y":
            break
        elif ask_add.lower() == "n":
            return

    # cek duplikat pada database
    index = 0
    database = get_database_info(dict_config)
    for data in database:
        index += 1

        if data["phone_number"] == nomor_hp:

            print("")
            print("Data dari nomor HP yang anda masukan sudah ada!")
            show_duplikat_database = [item for item in database if nomor_hp in item["phone_number"]]
            print("Data lama :")
            print(tabulate(show_duplikat_database, headers="keys", tablefmt="pipe"))
            print("Data baru yang diinput :")
            print(tabulate(inputed_data, headers="keys", tablefmt="pipe"))

            timpa = None
            while True:
                timpa = input("Apakah anda ingin mengganti data lama dengan data baru? (y/n): ")

                if timpa == "y":
                    # database[index-1] = inputed_data
                    tuple_profil = (email, nama, nickname, jenis_kelamin, provinsi, kota, alamat, show_duplikat_database[0]["email"])
                    tuple_contact = (email, kategori, catatan, nomor_hp)
                    tuple_sosmed = (facebook, instagram, twitter, nomor_hp)

                    update_profil(dict_config, tuple_profil)
                    update_contact(dict_config, tuple_contact)
                    update_sosmed(dict_config, tuple_sosmed)

                    print("Perubahan data berhasil disimpan!")
                    return
                elif timpa == "n":
                    print("Perubahan data tidak disimpan!")
                    return
                else:
                    print("Input invalid!")          
            
    # jika tidak ada data duplikat maka akan add data
    try:
            conn = pymysql.connect(**dict_config) # ( ** ) = Unpacking nilai -> bisa memasukan jumlah custom parameter (*) = unpacking list/tuple, (**) -> Dict
            # print("Connection Success !")
            cursor = conn.cursor() # membuka gerbang akses mysql
            sql_query_profil = """
                        INSERT INTO profil(email, full_name, nickname, gender, state, city, address)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
            cursor.execute(query=sql_query_profil, args=(email, nama, nickname, jenis_kelamin, provinsi, kota, alamat))
            sql_query_contact = """
                        INSERT INTO contact(phone_number, email, contact_category, notes, last_update)
                        VALUES (%s, %s, %s, %s, %s)
                        """
            cursor.execute(query=sql_query_contact, args=(nomor_hp, email, kategori, catatan, last_update))
            sql_query_sosmend = """
                        INSERT INTO social_media(phone_number, facebook, instagram, twitter)
                        VALUES (%s, %s, %s, %s)
                        """
            cursor.execute(query=sql_query_sosmend, args=(nomor_hp, facebook, instagram, twitter))

            conn.commit() 
            # return hasil
            print("Data Sukses masuk database!")
    except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
            print("Error !")
            conn.rollback()
            print(f"msg: {e}")
    finally: # code yang selalu dijalankan meskipun error atau tidak
            conn.close()