import pymysql
import pymysql.cursors
from tabulate import tabulate
# from test import dict_config

def input_not_null(prompt:str) -> str:
    """Funtion untuk membuat input box yang tidak boleh kosong

    Args:
        prompt (str): Caption untuk input box

    Returns:
        str: nilai dari input box
    """
    while True:
        user_input = input(prompt)
        if user_input == "" or user_input == None or user_input == " ":
            print("Input box tidak boleh kosong. Silakan masukkan input lagi.")
        else:
            return user_input


def connect_mysql(dict_config):
    """Function untuk login MySQL
    """
    try:
        conn = pymysql.connect(**dict_config) # ( ** ) = Unpacking nilai -> bisa memasukan jumlah custom parameter (*) = unpacking list/tuple, (**) -> Dict
        print("Connection Success !")
    
    except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")

    finally: # code yang selalu dijalankan meskipun error atau tidak
        conn.close()

def get_database_info(dict_config):
   """function untuk mendapatkan Database Yellow Pages

    Args:
        dict_config (dict): dictionary configuration untuk login MySQL

    Returns:
        str: list of dictionary data
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
                        FROM profil p
                        LEFT JOIN contact c
                            ON p.email = c.email
                        LEFT JOIN social_media s
                            ON c.phone_number = s.phone_number
                    """

        cursor.execute(query=sql_query)
        conn.commit() 
        hasil = cursor.fetchall()
        # print(tabulate(hasil, headers="keys", tablefmt="pipe"))
        return hasil
   except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")
   finally: # code yang selalu dijalankan meskipun error atau tidak
        conn.close()

def show_database(dict_config):
   """function untuk menampilkan Database Yellow Pages

    Args:
        dict_config (dict): dictionary configuration untuk login MySQL

    Returns:
        str: list of dictionary data
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
                        FROM profil p
                        LEFT JOIN contact c
                            ON p.email = c.email
                        LEFT JOIN social_media s
                            ON c.phone_number = s.phone_number
                    """

        cursor.execute(query=sql_query)
        conn.commit() 
        print("Commit Sucsess !")
        print("")
        print("Database Yellow Pages: ")
        hasil = cursor.fetchall()
        print(tabulate(hasil, headers="keys", tablefmt="pipe"))
   except Exception as e: # menangkap penyebab error dan menyimpan kedalam variabel e
        print("Error !")
        conn.rollback()
        print(f"msg: {e}")
   finally: # code yang selalu dijalankan meskipun error atau tidak
        conn.close()


def filter_database(dict_config):
   """Filter Database berdasarkan menu pilihan
   """
   database = get_database_info(dict_config)
   option = None
   filtered_database = None

   while option != 6:

      print("")
      print("1. Cari Kontak berdasarkan nomor HP")
      print("2. Cari Kontak berdasarkan nama")
      print("3. Cari Kontak berdasarkan kategori")
      print("4. Cari Kontak berdasarkan provinsi")
      print("5. Cari Kontak berdasarkan kota")
      print("6. Kembali ke menu utama")
      print("")

      # mencegah user memasukan input selain integer
      while True:
         option = input("Masukan pilihan menu: ")
         try:
               option = int(option)
               break
         except:
               print("Silahkan masukan angka!")

      if option == 1:
         # filter berdasarkan string nomor hp
         show_database(dict_config)

         input_no = input("Silahkan masukan nomor HP untuk filter: ")
         filtered_database = [item for item in database if input_no in item["phone_number"]]

         if filtered_database != []:
            print("Hasil Filter: ")
            print(tabulate(filtered_database, headers="keys", tablefmt="pipe"))
            print("Filter Sukses!")
         else:
            print("")
            print("Hasil Filter Kosong!")
            print("")

      elif option == 2:
         # filter berdasarkan string nama
         show_database(dict_config)

         input_nama = input("Silahkan masukan nama untuk filter: ")
         filtered_database = [item for item in database if input_nama.lower() in item["full_name"].lower()]

         if filtered_database != []:
            print("Hasil Filter: ")
            print(tabulate(filtered_database, headers="keys", tablefmt="pipe"))
            print("Filter Sukses!")
         else:
            print("")
            print("Hasil Filter Kosong!")
            print("")

      elif option == 3:
         # filter berdasarkan kategori
         show_database(dict_config)

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
         # mencegah user memasukan input selain integer
         while True:
            kategori = input("Silahkan pilih kategori untuk filter : ")
            try:
                  kategori = int(kategori)
                  if kategori in range(1,8):
                     break
                  else:
                      print("Silahkan masukan angka 1-7")
                      continue
            except:
                  print("Silahkan masukan angka 1-7")
            
         filtered_database = [item for item in database if list_kategori[kategori-1].lower() in item["contact_category"].lower()]
         if filtered_database != []:
            print("Hasil Filter: ")
            print(tabulate(filtered_database, headers="keys", tablefmt="pipe"))
            print("Filter Sukses!")
         else:
            print("")
            print("Hasil Filter Kosong!")
            print("")

      elif option == 4:
         # filter berdasarkan string provinsi
         show_database(dict_config)

         provinsi = input("Silahkan masukan provinsi untuk filter: ")
         filtered_database = [item for item in database if provinsi.lower() in item["state"].lower()]

         if filtered_database != []:
            print("Hasil Filter: ")
            print(tabulate(filtered_database, headers="keys", tablefmt="pipe"))
            print("Filter Sukses!")
         else:
            print("")
            print("Hasil Filter Kosong!")
            print("")

      elif option == 5:
         # filter berdasarkan string kota
         show_database(dict_config)

         kota = input("Silahkan masukan kota untuk filter: ")
         filtered_database = [item for item in database if kota.lower() in item["city"].lower()]

         if filtered_database != []:
            print("Hasil Filter: ")
            print(tabulate(filtered_database, headers="keys", tablefmt="pipe"))
            print("Filter Sukses!")
         else:
            print("")
            print("Hasil Filter Kosong!")
            print("")

      elif option == 6:
          pass
      else:
          print("Input is not valid !")